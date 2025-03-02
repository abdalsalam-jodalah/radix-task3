import datetime
from unittest.mock import patch
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager_app.models.email_notification_model import EmailNotification
from task_manager_app.models.task_models import Task

User = get_user_model()

class AuthApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.auth_url = '/authApi/'  # Adjust if needed
        # Create a test user
        self.user = User.objects.create_user(email='test@example.com', password='pass123')
    
    def test_login_missing_fields(self):
        response = self.client.post(self.auth_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_invalid_credentials(self):
        payload = {
            "email": "test@example.com",
            "password": "wrongpassword",
            "device_name": "TestDevice",
            "device_type": "mobile",
            "user_agent": "TestAgent"
        }
        response = self.client.post(self.auth_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        payload = {
            "email": "test@example.com",
            "password": "pass123",
            "device_name": "TestDevice",
            "device_type": "mobile",
            "user_agent": "TestAgent"
        }
        response = self.client.post(self.auth_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

    def test_logout_missing_fields(self):
        # Force authenticate the user and try logout with missing fields
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.auth_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @patch('task_manager_app.components.auth_comopnents.AuthComponents.extract_token', return_value='dummy-token')
    @patch('task_manager_app.components.user_device_components.UserDeviceComponents.generate_device_id', return_value='dummy-device')
    @patch('task_manager_app.components.user_device_components.UserDeviceComponents.logout_device_basedon_token')
    @patch('task_manager_app.components.auth_comopnents.AuthComponents.logout_token')
    def test_logout_success(self, mock_logout_token, mock_logout_device, mock_generate_device_id, mock_extract_token):
        self.client.force_authenticate(user=self.user)
        payload = {
            "device_name": "TestDevice",
            "device_type": "mobile",
            "user_agent": "TestAgent",
            "auth_header": "Bearer dummy-token"
        }
        response = self.client.put(self.auth_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Logout successful!")


class RoleApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.role_url = '/roleApi/'  # Adjust URL as needed
        # Create a user with an admin role for role management
        self.user = User.objects.create_user(email='admin@example.com', password='adminpass', role='admin')
        self.client.force_authenticate(user=self.user)
    
    def test_get_roles(self):
        response = self.client.get(self.role_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_role_invalid_data(self):
        payload = {"invalid_field": "value"}
        response = self.client.post(self.role_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_nonexistent_role(self):
        url = f"{self.role_url}999/"  # Assuming 999 does not exist
        payload = {"name": "Updated Role"}
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_role(self):
        url = f"{self.role_url}999/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TaskApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.task_url = '/taskApi/'  # Update to your URL pattern
        # Create a manager user who has permission to create tasks
        self.user = User.objects.create_user(email='manager@example.com', password='managerpass', role='manager')
        self.client.force_authenticate(user=self.user)
    
    @patch('task_manager_app.components.task_notification.send_task_notification.delay')
    def test_create_task_success(self, mock_send_notification):
        payload = {
            "name": "New Task",
            "due_date": (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z",
            "priority": "high",
            "status": "new",
            "category": 1  # Ensure a valid category exists
        }
        response = self.client.post(self.task_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(mock_send_notification.called)
    
    def test_get_tasks(self):
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_task_without_permission(self):
        # Create a task as manager, then try to update as a sub-user who lacks permission
        self.client.force_authenticate(user=self.user)
        payload = {
            "name": "Manager Task",
            "due_date": (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z",
            "priority": "medium",
            "status": "new",
            "category": 1
        }
        create_response = self.client.post(self.task_url, payload, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        task_id = create_response.data.get("task", {}).get("id")
        
        # Now switch to a sub-user role
        sub_user = User.objects.create_user(email='subuser@example.com', password='subpass', role='sub-user')
        self.client.force_authenticate(user=sub_user)
        update_payload = {"name": "Updated Task Name"}
        url = f"{self.task_url}{task_id}/"
        response = self.client.put(url, update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
    
    def test_delete_task_without_permission(self):
        # Create a task and attempt to delete as a sub-user
        self.client.force_authenticate(user=self.user)
        payload = {
            "name": "Task to Delete",
            "due_date": (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z",
            "priority": "low",
            "status": "new",
            "category": 1
        }
        create_response = self.client.post(self.task_url, payload, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        task_id = create_response.data.get("task", {}).get("id")
        
        sub_user = User.objects.create_user(email='subuser2@example.com', password='subpass', role='sub-user')
        self.client.force_authenticate(user=sub_user)
        url = f"{self.task_url}{task_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
    
    def test_patch_task_success(self):
        # Test partial update by a permitted manager user
        payload = {
            "name": "Task to Patch",
            "due_date": (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z",
            "priority": "medium",
            "status": "new",
            "category": 1
        }
        create_response = self.client.post(self.task_url, payload, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        task_id = create_response.data.get("task", {}).get("id")
        patch_payload = {"status": "in-progress"}
        url = f"{self.task_url}{task_id}/"
        response = self.client.patch(url, patch_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_url = '/userApi/'  # Adjust URL as needed
        self.user = User.objects.create_user(email='user@example.com', password='userpass')
        self.client.force_authenticate(user=self.user)
    
    def test_get_user_list(self):
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_single_user(self):
        url = f"{self.user_url}{self.user.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("email"), self.user.email)
    
    def test_create_user(self):
        payload = {
            "email": "newuser@example.com",
            "password": "newpass123"
            # Include other required fields if any
        }
        response = self.client.post(self.user_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_user(self):
        url = f"{self.user_url}{self.user.id}/"
        update_payload = {"email": "updated@example.com"}
        response = self.client.put(url, update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("email"), "updated@example.com")
    
    def test_partial_update_user(self):
        url = f"{self.user_url}{self.user.id}/"
        update_payload = {"email": "partialupdate@example.com"}
        response = self.client.patch(url, update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("email"), "partialupdate@example.com")
    
    def test_delete_user(self):
        new_user = User.objects.create_user(email='delete@example.com', password='deletepass')
        url = f"{self.user_url}{new_user.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class IntegrationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a manager user for a full integration workflow
        self.user = User.objects.create_user(email='integration@example.com', password='integratepass', role='manager')
        self.client.force_authenticate(user=self.user)
        self.auth_url = '/authApi/'
        self.user_url = '/userApi/'
        self.task_url = '/taskApi/'

    @patch('task_manager_app.components.task_notification.send_task_notification.delay')
    def test_full_workflow_task_reminder(self, mock_send_notification):
        # Step 1: Login and retrieve token (if your flow depends on it)
        login_payload = {
            "email": "integration@example.com",
            "password": "integratepass",
            "device_name": "IntegrationDevice",
            "device_type": "web",
            "user_agent": "IntegrationAgent"
        }
        login_response = self.client.post(self.auth_url, login_payload)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token = login_response.data.get("access_token")
        
        # Step 2: Create a task with a due_date in the past (simulate overdue)
        past_due_date = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).isoformat() + "Z"
        task_payload = {
            "name": "Overdue Task",
            "due_date": past_due_date,
            "priority": "high",
            "status": "new",
            "category": 1
        }
        task_response = self.client.post(self.task_url, task_payload, format='json')
        self.assertEqual(task_response.status_code, status.HTTP_201_CREATED)
        task_id = task_response.data.get("task", {}).get("id")
        
        # Step 3: Simulate triggering the reminder process.
        # Here we check that the Celery task (or reminder function) is queued.
        self.assertTrue(mock_send_notification.called)
        
        # Optionally, check that an EmailNotification record was created.
        notification_exists = EmailNotification.objects.filter(task__id=task_id).exists()
        self.assertTrue(notification_exists)
