import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from tasks.models import Task
from labels.models import Label

class TaskFilter(django_filters.FilterSet):
    # Добавляем чекбокс для фильтрации "Только свои задачи"
    self_tasks = django_filters.BooleanFilter(
        label=_("Only own tasks"),
        widget=forms.CheckboxInput,
        method='filter_self'
    )
    
    # Фильтр по меткам (Label сущность следующего шага, подготовь место)
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_("Label")
    )

    def filter_self(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']