from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.statuses.models import Status


class StatusTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.status = Status.objects.create(name="New")

    def test_statuses_list_access(self):
        # Анонима должно редиректить на логин
        response = self.client.get(reverse("statuses"))
        self.assertEqual(response.status_code, 302)

        # Залогиненный видит список
        self.client.force_login(self.user)
        response = self.client.get(reverse("statuses"))
        self.assertEqual(response.status_code, 200)

    def test_status_create(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("status_create"), {"name": "In progress"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name="In progress").exists())
