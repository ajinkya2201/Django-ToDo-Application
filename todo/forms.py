from django import forms
from .models import Task
from django.utils import timezone

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
        "due_date": forms.DateInput(attrs={"type": "date"}),
    }

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")

        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError("Due date cannot be in the past.")

        return due_date

