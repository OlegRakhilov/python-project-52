from django import forms
from tasks.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # Автор (author) исключен, он будет подставляться во View
        fields = ('name', 'description', 'status', 'executor', 'labels')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'labels': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }