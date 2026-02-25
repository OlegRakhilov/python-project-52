from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from labels.models import Label
from tasks.models import Task
from statuses.models import Status

class LabelCrudTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.label = Label.objects.create(name='Bug')
        self.status = Status.objects.create(name='New')

    def test_labels_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label.name)

    def test_create_label(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('label_create'), {'name': 'Feature'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Feature').exists())

    def test_update_label(self):
        self.client.force_login(self.user)
        url = reverse('label_update', kwargs={'pk': self.label.pk})
        self.client.post(url, {'name': 'Updated Bug'})
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Bug')

    def test_delete_label_unused(self):
        """Проверка удаления метки, которая не привязана к задачам."""
        self.client.force_login(self.user)
        url = reverse('label_delete', kwargs={'pk': self.label.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

    def test_delete_label_in_use_fail(self):
        """Проверка ЗАПРЕТА удаления метки, если она привязана к задаче."""
        # Создаем задачу и привязываем к ней метку
        task = Task.objects.create(
            name='Test Task',
            author=self.user,
            status=self.status
        )
        task.labels.add(self.label)

        self.client.force_login(self.user)
        url = reverse('label_delete', kwargs={'pk': self.label.pk})
        response = self.client.post(url)
        
        # Должен быть редирект обратно на список с ошибкой, а метка остаться
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())