from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import get_messages
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class TaskCrudTest(TestCase):
    fixtures = []

    def setUp(self):
        # Создаем пользователей
        self.user1 = User.objects.create_user(username='author', password='password123')
        self.user2 = User.objects.create_user(username='executor', password='password123')
        
        # Создаем статус
        self.status = Status.objects.create(name='New')
        
        # Создаем метку
        self.label = Label.objects.create(name='Bug')
        
        # Создаем задачу для тестов (автор — user1)
        self.task = Task.objects.create(
            name='Test Task',
            author=self.user1,
            status=self.status,
            executor=self.user2
        )
        self.task.labels.add(self.label)

    def test_tasks_list(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)


    def test_create_task(self):
        self.client.force_login(self.user1)
        data = {
            'name': 'New Task',
            'status': self.status.id,
            'executor': self.user2.id,
            'labels': [self.label.id]
        }
        response = self.client.post(reverse('task_create'), data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), _("Task successfully created"))
        self.assertEqual(response.status_code, 302)
        new_task = Task.objects.get(name='New Task')
        self.assertEqual(new_task.author, self.user1)
        self.assertEqual(new_task.executor, self.user2)
        self.assertEqual(new_task.status, self.status)
        self.assertIn(self.label, new_task.labels.all())

    def test_update_task(self):
        self.client.force_login(self.user1)
        url = reverse('task_update', kwargs={'pk': self.task.pk})
        data = {'name': 'Updated Task', 'status': self.status.id}
        self.client.post(url, data)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_delete_task_by_author(self):
        self.client.force_login(self.user1)
        url = reverse('task_delete', kwargs={'pk': self.task.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_delete_task_by_non_author(self):
        # Логинимся под другим пользователем
        self.client.force_login(self.user2)
        url = reverse('task_delete', kwargs={'pk': self.task.pk})
        response = self.client.post(url)
        # Должен быть редирект с ошибкой, а задача остаться в базе
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_filter_tasks(self):
        self.client.force_login(self.user1)
        # Фильтр по статусу
        url = f"{reverse('tasks')}?status={self.status.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Фильтр "Только свои задачи"
        url_self = f"{reverse('tasks')}?self_tasks=on"
        response_self = self.client.get(url_self)
        self.assertContains(response_self, self.task.name)