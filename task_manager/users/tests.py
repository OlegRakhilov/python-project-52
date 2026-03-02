from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserCrudTest(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        # Берем пользователя из фикстуры для тестов R, U, D
        self.user = User.objects.get(pk=1)
        # Данные для теста регистрации (C)
        self.user_data = {
            "first_name": "Oleg",
            "last_name": "Ivanov",
            "username": "new_user",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        }

    # C - Create (Регистрация)
    def test_user_registration(self):
        url = reverse("user_create")
        response = self.client.post(url, self.user_data)

        # Теперь будет 302, так как пароли валидны и совпадают
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="new_user").exists())

    # R - Read (Список)
    def test_users_list(self):
        response = self.client.get(reverse("users"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    # U - Update (Своего профиля)
    def test_user_update_self(self):
        self.client.force_login(self.user)
        url = reverse("user_update", kwargs={"pk": self.user.pk})

        updated_data = {
            "username": "updated_name",
            "first_name": "NewName",
            "last_name": "NewLastName",
        }
        response = self.client.post(url, updated_data)

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updated_name")
        self.assertEqual(self.user.first_name, "NewName")

    # U - Update Protection (Чужого профиля)
    def test_user_update_other_fail(self):
        other_user = User.objects.create_user(username="other", password="123")
        self.client.force_login(self.user)

        url = reverse("user_update", kwargs={"pk": other_user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users"))

    # D - Delete (Себя)
    def test_user_delete_self(self):
        self.client.force_login(self.user)
        url = reverse("user_delete", kwargs={"pk": self.user.pk})

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    # D - Delete Protection (Чужого профиля)
    def test_user_delete_other_fail(self):
        other_user = User.objects.create_user(username="other", password="123")
        self.client.force_login(self.user)

        url = reverse("user_delete", kwargs={"pk": other_user.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(pk=other_user.pk).exists())
