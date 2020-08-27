from django import forms
from .models import Project, Tasks

class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('name', 'status_id')