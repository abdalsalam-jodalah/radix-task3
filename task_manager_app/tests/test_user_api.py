import json
from unittest.mock import patch, MagicMock
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.response import Response

from task_manager_app.controllers.user_controllers import UserApi
from task_manager_app.models.user_models import User

class UserApiTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory() #simulating requests
        
        self.dummy_user = MagicMock(spec=User)
        self.dummy_user.id = 1
        self.dummy_user.email = "user@example.com"
        self.dummy_user.__class__ = User

        self.permissions_patcher = patch.object(UserApi, 'get_permissions', return_value=[])
        self.mock_permissions = self.permissions_patcher.start()
        self.addCleanup(self.permissions_patcher.stop)
        
    # ---------- GET Tests ----------
    def test_get_invalid_token(self):
        request = self.factory.get("/user/")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=None):
            response = UserApi.as_view()(request)
            self.assertEqual(response.status_code, 400)
            

    def test_get_users_list_success(self): 
        request = self.factory.get("/user/")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.user_controllers.RolePermissionComponent.handle_action", return_value=[self.dummy_user]), \
             patch("task_manager_app.controllers.user_controllers.CustomPagination.paginate_queryset", return_value=[self.dummy_user]), \
             patch("task_manager_app.controllers.user_controllers.CustomPagination.get_paginated_response", side_effect=lambda data: Response(data)):
            response = UserApi.as_view()(request)
            self.assertEqual(response.status_code, 200)

    def test_get_user_detail_success(self): 
        request = self.factory.get("/user/1/")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.user_controllers.RolePermissionComponent.handle_action", return_value=[self.dummy_user]), \
             patch("task_manager_app.controllers.user_controllers.UserComponents.get_user_form_users", return_value=self.dummy_user):
            response = UserApi.as_view()(request, id=1)
            self.assertEqual(response.status_code, 200)

    def test_get_user_detail_not_found(self):
        request = self.factory.get("/user/999/")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.user_controllers.RolePermissionComponent.handle_action", return_value=[self.dummy_user]), \
             patch("task_manager_app.controllers.user_controllers.UserComponents.get_user_form_users", return_value=None):
            response = UserApi.as_view()(request, id=999)
            self.assertEqual(response.status_code, 404)

    # ---------- POST Tests ----------
    def test_post_invalid_token(self):
        data = {"full_name": "Test User", "email": "test@example.com", "password": "Password1", "role": 4}
        request = self.factory.post("/user/", data, format="json")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=None):
            response = UserApi.as_view()(request)
            self.assertEqual(response.status_code, 400)

    def test_post_invalid_data(self): 
        data = {"full_name": "Test User", "email": "invalid", "password": "short", "role": 4}
        request = self.factory.post("/user/", data, format="json")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=self.dummy_user):
            response = UserApi.as_view()(request)
            self.assertEqual(response.status_code, 400)

    def test_post_success(self):
        data = {"full_name": "Test User", "email": "test@example.com", "password": "Password1", "role": 4}
        request = self.factory.post("/user/", data, format="json")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.user_controllers.RolePermissionComponent.handle_action", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.user_controllers.UserSerializer") as mock_serializer_cls:
            instance = mock_serializer_cls.return_value
            instance.is_valid.return_value = True
            instance.data = {"id": self.dummy_user.id, "full_name": "Test User", "email": "test@example.com"}
            response = UserApi.as_view()(request)
            self.assertEqual(response.status_code, 201)

    # ---------- PUT Tests ----------
    def test_put_missing_id(self):
        data = {"full_name": "Updated"}
        request = self.factory.put("/user/", data, format="json")
        response = UserApi.as_view()(request, id=None)
        self.assertEqual(response.status_code, 400)

    def test_put_invalid_token(self):
        data = {"full_name": "Updated"}
        request = self.factory.put("/user/1/", data, format="json")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=None):
            response = UserApi.as_view()(request, id=1)
            self.assertEqual(response.status_code, 400)

    def test_put_user_not_found(self):
        data = {"full_name": "Updated"}
        request = self.factory.put("/user/1/", data, format="json")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.user_controllers.RolePermissionComponent.handle_action", return_value="User not found!"):
            response = UserApi.as_view()(request, id=1)
            self.assertEqual(response.status_code, 404)

    def test_put_success(self):
        data = {"full_name": "Updated"}
        request = self.factory.put("/user/1/", data, format="json")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.user_controllers.RolePermissionComponent.handle_action", return_value={"dummy": "result"}):
            response = UserApi.as_view()(request, id=1)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, data)

    # ---------- PATCH Tests ----------
    def test_patch_invalid_token(self):
        data = {"full_name": "Patched"}
        request = self.factory.patch("/user/1/", data, format="json")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=None):
            response = UserApi.as_view()(request, user_id=1)
            self.assertEqual(response.status_code, 400)

    def test_patch_user_not_found(self):
        data = {"full_name": "Patched"}
        request = self.factory.patch("/user/1/", data, format="json")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.user_controllers.UserComponents.get_user_by_id", return_value=None):
            response = UserApi.as_view()(request, user_id=1)
            self.assertEqual(response.status_code, 404)

    def test_patch_success(self):
        data = {"full_name": "Patched"}
        request = self.factory.patch("/user/1/", data, format="json")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.user_controllers.UserComponents.get_user_by_id", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.user_controllers.UserComponents.update_user", return_value=True), \
             patch("task_manager_app.controllers.user_controllers.UserSerializer") as mock_serializer:
            instance = mock_serializer.return_value
            instance.is_valid.return_value = True
            instance.data = data
            response = UserApi.as_view()(request, user_id=1)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, data)

    def test_patch_invalid_data(self):
        data = {"full_name": ""}
        request = self.factory.patch("/user/1/", data, format="json")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.user_controllers.UserComponents.get_user_by_id", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.user_controllers.UserSerializer") as mock_serializer:
            instance = mock_serializer.return_value
            instance.is_valid.return_value = False
            instance.errors = {"error": "Invalid"}
            response = UserApi.as_view()(request, user_id=1)
            self.assertEqual(response.status_code, 400)

    # ---------- DELETE Tests ----------
    def test_delete_invalid_token(self):
        request = self.factory.delete("/user/1/")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=None):
            response = UserApi.as_view()(request, user_id=1)
            self.assertEqual(response.status_code, 400)

    def test_delete_user_not_found(self):
        request = self.factory.delete("/user/1/")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.user_controllers.UserComponents.get_user_by_id", return_value=None):
            response = UserApi.as_view()(request, user_id=1)
            self.assertEqual(response.status_code, 404)

    def test_delete_success(self):
        request = self.factory.delete("/user/1/")
        with patch("task_manager_app.controllers.user_controllers.AC.get_user", return_value=self.dummy_user), \
             patch("task_manager_app.controllers.user_controllers.UserComponents.get_user_by_id", return_value=self.dummy_user):
            self.dummy_user.delete = MagicMock()
            response = UserApi.as_view()(request, user_id=1)
            self.assertEqual(response.status_code, 204)
            self.dummy_user.delete.assert_called_once()
