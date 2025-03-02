from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models.task_models import Task

User = get_user_model()

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.task = Task.objects.create(title="Sample Task", assigned_to=self.user, status="Pending")

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Sample Task")
        self.assertEqual(self.task.status, "Pending")
        self.assertEqual(self.task.assigned_to, self.user)

    def test_task_status_update(self):
        self.task.status = "Completed"
        self.task.save()
        self.assertEqual(self.task.status, "Completed")

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class TaskRoleAccessTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="admin123")
        self.user = User.objects.create_user(username="user", password="user123")
        self.client.force_authenticate(user=self.admin)
        self.task = Task.objects.create(title="Admin Task", assigned_to=self.user)

    def test_admin_can_create_task(self):
        url = reverse("task-list")
        data = {"title": "New Task", "assigned_to": self.user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_create_task(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("task-list")
        data = {"title": "User Task", "assigned_to": self.user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskFilteringPaginationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="password")
        self.client.force_authenticate(user=self.user)

        for i in range(10):
            Task.objects.create(title=f"Task {i}", status="Pending" if i % 2 == 0 else "Completed")

    def test_filter_tasks_by_status(self):
        url = reverse("task-list") + "?status=Pending"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(task["status"] == "Pending" for task in response.data["results"]))

    def test_pagination(self):
        url = reverse("task-list") + "?page=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("next" in response.data or "previous" in response.data)
