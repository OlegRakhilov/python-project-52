from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


class LabelCrudTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.label = Label.objects.create(name="Bug")
        self.status = Status.objects.create(name="New")

    def test_labels_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("labels"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label.name)

    def test_create_label(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("label_create"), {"name": "Feature"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name="Feature").exists())

    def test_update_label(self):
        self.client.force_login(self.user)
        url = reverse("label_update", kwargs={"pk": self.label.pk})
        self.client.post(url, {"name": "Updated Bug"})
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Updated Bug")

    def test_delete_unused_label(self):
        self.client.force_login(self.user)
        url = reverse("label_delete", kwargs={"pk": self.label.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse("labels"))
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

    def test_delete_label_in_use(self):
        # Привязываем метку к задаче
        self.task = Task.objects.create(
            name="Test Task", author=self.user, status=self.status
        )
        self.task.labels.add(self.label)
        self.client.force_login(self.user)

        url = reverse("label_delete", kwargs={"pk": self.label.pk})
        response = self.client.post(url)

        # Метка должна остаться в базе
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
        # Должен быть редирект на список с ошибкой
        self.assertRedirects(response, reverse("labels"))
