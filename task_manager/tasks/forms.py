from django import forms
from task_manager.tasks.models import Task
from django.utils.translation import gettext_lazy as _


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Эта магия заставляет выпадающий список показывать "Имя Фамилия"
        # вместо стандартного "username", что критично для Playwright
        self.fields['executor'].label_from_instance = lambda obj:(
            obj.get_full_name() if obj.get_full_name() else obj.username
        )

    class Meta:
        model = Task  # ПРОВЕРЬТЕ: эта строка должна быть здесь!
        fields = ('name', 'description', 'status', 'executor', 'labels')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'labels': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
        # Добавляем человекочитаемые лейблы, если они не подтянулись из модели
        labels = {
            'name': _("Name"),
            'status': _("Status"),
            'executor': _("Executor"),
            'labels': _("Labels"),
        }