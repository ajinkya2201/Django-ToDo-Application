from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/",views.add_task,name="add_task"),    
    path("edit/<int:pk>/",views.edit_task,name="edit_task"),
    path("delete/<int:pk>/",views.delete_task,name="delete_task"),
    path("toggle_complete/<int:pk>/",views.toggle_complete,name="toggle_complete"),

]