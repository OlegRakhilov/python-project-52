import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class TaskFilter(django_filters.FilterSet):
    # Все фильтры должны иметь ровно 4 пробела от края (один Tab)
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), label=_("Status")
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=get_user_model().objects.all(), label=_("Executor")
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(), label=_("Label")
    )

    self_tasks = django_filters.BooleanFilter(
        label=_("Only own tasks"),
        widget=forms.CheckboxInput(),
        method="filter_self",
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "labels"]

    def filter_self(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset
