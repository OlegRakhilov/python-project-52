from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_("Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    # Автор устанавливается автоматически (текущий юзер)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_tasks",
        verbose_name=_("Author"),
    )

    # Статус обязателен
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="tasks",
        verbose_name=_("Status"),
    )

    # Исполнитель может быть не назначен
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="tasks",
        null=True,
        blank=True,
        verbose_name=_("Executor"),
    )

    labels = models.ManyToManyField(
        Label, blank=True, related_name="tasks", verbose_name=_("Labels")
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
