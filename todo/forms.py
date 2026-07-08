from django import forms
from django.utils import timezone
from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            "title",
            "description",
            "priority",
            "due_date",
            "completed",
        ]

        widgets = {

            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter task title"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter task description"
            }),

            "priority": forms.Select(attrs={
                "class": "form-select"
            }),

            "due_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "completed": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")

        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError(
                "Due date cannot be in the past."
            )

        return due_date