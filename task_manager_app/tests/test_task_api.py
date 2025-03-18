import json
from unittest.mock import patch, MagicMock
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.response import Response
from rest_framework import status

from task_manager_app.controllers.task_controllers import TaskApi, ByUser
from task_manager_app.models.user_models import User
from task_manager_app.models.task_models import Task
from task_manager_app.models.email_notification_models import EmailNotification

class TaskApiTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.dummy_user = MagicMock(spec=User)
        self.dummy_user.id = 1
        self.dummy_user.email = "user@example.com"
        self.dummy_user.__class__ = User

        self.dummy_task = MagicMock(spec=Task)
        self.dummy_task.id = 1
        self.dummy_task.name = "Test Task"
        self.dummy_task.assigner = self.dummy_user
        self.dummy_task.__class__ = Task

        self.permissions_patcher = patch.object(TaskApi, 'get_permissions', return_value=[])
        self.mock_permissions = self.permissions_patcher.start()
        self.addCleanup(self.permissions_patcher.stop)

    def test_get_invalid_token(self):
        request = self.factory.get("/task/")
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=None):
            response = TaskApi.as_view()(request)
            self.assertEqual(response.status_code, 400)

    def test_get_task_detail_success(self):
        request = self.factory.get("/task/1/")
        dummy_result = [self.dummy_task]
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.task_controllers.RolePermissionComponent.handle_action", return_value=dummy_result), \
             patch("task_manager_app.controllers.task_controllers.TaskComponents.get_task_from_tasks", return_value=(
                 {"id": self.dummy_task.id, "name": self.dummy_task.name},
                 {"message": "Task found", "task": {"id": self.dummy_task.id, "name": self.dummy_task.name}, "status": status.HTTP_200_OK},
                 status.HTTP_200_OK
             )):
            response = TaskApi.as_view()(request, pk=self.dummy_task.id)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.get("message"), "Task found")

    def test_get_task_detail_not_found(self):
        request = self.factory.get("/task/999/")
        dummy_result = []
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.task_controllers.RolePermissionComponent.handle_action", return_value=dummy_result), \
             patch("task_manager_app.controllers.task_controllers.TaskComponents.get_task_from_tasks", return_value=(
                 None,
                 {"message": "Task not found", "task": None, "status": status.HTTP_404_NOT_FOUND},
                 status.HTTP_404_NOT_FOUND
             )):
            response = TaskApi.as_view()(request, pk=999)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.get("message"), "Task not found")

    def test_get_tasks_list_success(self):
        request = self.factory.get("/task/")
        dummy_result = [self.dummy_task]
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.task_controllers.RolePermissionComponent.handle_action", return_value=dummy_result), \
             patch("task_manager_app.controllers.task_controllers.TaskComponents.get_tasks_filtered", return_value=(dummy_result, status.HTTP_200_OK)), \
             patch("task_manager_app.controllers.task_controllers.CustomPagination.paginate_queryset", return_value=dummy_result), \
             patch("task_manager_app.controllers.task_controllers.TaskSerializer", return_value=MagicMock(data=[{"id": self.dummy_task.id, "name": self.dummy_task.name}])), \
             patch("task_manager_app.controllers.task_controllers.CustomPagination.get_paginated_response", side_effect=lambda data: Response(data, status=200)):
            response = TaskApi.as_view()(request)
            self.assertEqual(response.status_code, 200)

    def test_get_tasks_list_no_tasks(self):
        request = self.factory.get("/task/")
        dummy_result = [self.dummy_task]
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.task_controllers.RolePermissionComponent.handle_action", return_value=dummy_result), \
             patch("task_manager_app.controllers.task_controllers.TaskComponents.get_tasks_filtered", return_value=(None, None)):
            response = TaskApi.as_view()(request)
            self.assertEqual(response.status_code, 404)

    def test_post_invalid_token(self):
        data = {"name": "Test Task", "description": "A task description"}
        request = self.factory.post("/task/", data, format="json")
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=None):
            response = TaskApi.as_view()(request)
            self.assertEqual(response.status_code, 400)

    def test_post_success(self):
        data = {"name": "Test Task", "description": "A task description"}
        request = self.factory.post("/task/", data, format="json")
        fetched_data = {"name": "Test Task", "description": "A task description"}
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.task_controllers.TaskComponents.fetch_user_data", return_value=fetched_data), \
             patch("task_manager_app.controllers.task_controllers.RolePermissionComponent.handle_action", return_value=(self.dummy_task, {"status": status.HTTP_201_CREATED})), \
             patch("task_manager_app.controllers.task_controllers.EmailNotification.objects.create", return_value=MagicMock()), \
             patch("task_manager_app.controllers.task_controllers.send_task_notification.delay") as mock_delay, \
             patch("task_manager_app.controllers.task_controllers.TaskSerializer", return_value=MagicMock(is_valid=lambda: True, data={"id": self.dummy_task.id, "name": self.dummy_task.name})):
            response = TaskApi.as_view()(request)
            self.assertEqual(response.status_code, 201)
            mock_delay.assert_called_once()

    def test_put_invalid_token(self):
        data = {"name": "Updated Task"}
        request = self.factory.put("/task/1/", data, format="json")
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=None):
            response = TaskApi.as_view()(request, pk=1)
            self.assertEqual(response.status_code, 400)

    def test_put_success(self):
        data = {"name": "Updated Task"}
        request = self.factory.put("/task/1/", data, format="json")
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.task_controllers.RolePermissionComponent.handle_action", return_value=({"dummy": "result"}, 200)):
            response = TaskApi.as_view()(request, pk=1)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, {"dummy": "result"})

    def test_delete_invalid_token(self):
        request = self.factory.delete("/task/1/")
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=None):
            response = TaskApi.as_view()(request, pk=1)
            self.assertEqual(response.status_code, 400)

    def test_delete_success(self):
        request = self.factory.delete("/task/1/")
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.task_controllers.RolePermissionComponent.handle_action", return_value=({"detail": "Task deleted successfully"}, 204)):
            response = TaskApi.as_view()(request, pk=1)
            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.data.get("detail"), "Task deleted successfully")

    def test_patch_invalid_token(self):
        data = {"name": "Patched Task"}
        request = self.factory.patch("/task/1/", data, format="json")
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=None):
            response = TaskApi.as_view()(request, pk=1)
            self.assertEqual(response.status_code, 400)

    def test_patch_success(self):
        data = {"name": "Patched Task"}
        request = self.factory.patch("/task/1/", data, format="json")
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.task_controllers.TaskComponents.partial_update_task", return_value=(
                 {"name": "Patched Task"}, 200
             )):
            response = TaskApi.as_view()(request, pk=1)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, {"name": "Patched Task"})


class ByUserTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.dummy_user = MagicMock(spec=User)
        self.dummy_user.id = 1
        self.dummy_user.email = "user@example.com"
        self.dummy_user.__class__ = User

        self.dummy_task = MagicMock(spec=Task)
        self.dummy_task.id = 1
        self.dummy_task.name = "Test Task"
        self.dummy_task.assigner = self.dummy_user
        self.dummy_task.__class__ = Task

        self.permissions_patcher = patch.object(ByUser, 'get_permissions', return_value=[])
        self.mock_permissions = self.permissions_patcher.start()
        self.addCleanup(self.permissions_patcher.stop)

    def test_get_invalid_token(self):
        request = self.factory.get("/task/byuser/")
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=None):
            response = ByUser.as_view()(request)
            self.assertEqual(response.status_code, 400)

    def test_get_task_detail_success(self):
        request = self.factory.get("/task/byuser/1")
        task_dict = {"id": self.dummy_task.id, "name": self.dummy_task.name}
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.task_controllers.TaskComponents.get_task_response", return_value=(
                 task_dict,
                 {"message": "Task found", "task": task_dict, "status": status.HTTP_200_OK},
                 status.HTTP_200_OK
             )):
            response = ByUser.as_view()(request, pk=1)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.get("message"), "Task found")

    def test_get_task_detail_not_found(self):
        request = self.factory.get("/task/byuser/999")
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.task_controllers.TaskComponents.get_task_response", return_value=(
                 None,
                 {"message": "Task not found", "task": None, "status": status.HTTP_404_NOT_FOUND},
                 status.HTTP_404_NOT_FOUND
             )):
            response = ByUser.as_view()(request, pk=999)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.get("message"), "Task not found")

    def test_get_tasks_list_success(self):
        request = self.factory.get("/task/byuser/")
        dummy_tasks = [self.dummy_task]
        with patch("task_manager_app.controllers.task_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.task_controllers.TaskComponents.get_tasks_assigned_by_user", return_value=dummy_tasks), \
             patch("task_manager_app.controllers.task_controllers.CustomPagination.paginate_queryset", return_value=dummy_tasks), \
             patch("task_manager_app.controllers.task_controllers.TaskSerializer", return_value=MagicMock(data=[{"id": self.dummy_task.id, "name": self.dummy_task.name}])), \
             patch("task_manager_app.controllers.task_controllers.CustomPagination.get_paginated_response", side_effect=lambda data: Response(data, status=200)):
            response = ByUser.as_view()(request)
            self.assertEqual(response.status_code, 200)
