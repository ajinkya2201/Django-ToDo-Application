from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    path("tasks/", views.all_tasks, name="all_tasks"),

    path("tasks/pending/", views.pending_tasks, name="pending_tasks"),

    path("tasks/completed/", views.completed_tasks, name="completed_tasks"),

    path("tasks/overdue/", views.overdue_tasks, name="overdue_tasks"),

    path("add/", views.add_task, name="add_task"),

    path("edit/<int:pk>/", views.edit_task, name="edit_task"),

    path("delete/<int:pk>/", views.delete_task, name="delete_task"),

    path("toggle/<int:pk>/", views.toggle_complete, name="toggle_complete"),
]