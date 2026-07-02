from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .models import Task
from .forms import TaskForm

from django.db.models import Q
from datetime import datetime



# ---------------------------
# Home Dashboard
# ---------------------------

from django.db.models import Q
from django.utils import timezone

def home(request):

    filter_type = request.GET.get("filter")
    task_name = request.GET.get("task_name", "").strip()
    created_date = request.GET.get("created_date")
    due_date = request.GET.get("due_date")

    total_tasks = Task.objects.count()
    pending_count = Task.objects.filter(completed=False).count()
    completed_count = Task.objects.filter(completed=True).count()
    overdue_count = Task.objects.filter(
        completed=False,
        due_date__lt=timezone.now().date()
    ).count()

    overdue_tasks = Task.objects.filter(
        completed=False,
        due_date__lt=timezone.now().date()
    ).order_by("due_date")[:5]

    # Base queryset according to selected card
    if filter_type == "all":
        filtered_tasks = Task.objects.all().order_by("-created_at")
        page_title = "All Tasks"

    elif filter_type == "pending":
        filtered_tasks = Task.objects.filter(
            completed=False
        ).order_by("-created_at")
        page_title = "Pending Tasks"

    elif filter_type == "completed":
        filtered_tasks = Task.objects.filter(
            completed=True
        ).order_by("-created_at")
        page_title = "Completed Tasks"

    elif filter_type == "overdue":
        filtered_tasks = Task.objects.filter(
            completed=False,
            due_date__lt=timezone.now().date()
        ).order_by("due_date")
        page_title = "Overdue Tasks"

    else:
        filtered_tasks = Task.objects.all().order_by("-created_at")
        page_title = "Search Results"

    # Search by Task Name
    if task_name:
        filtered_tasks = filtered_tasks.filter(
            Q(title__icontains=task_name) |
            Q(description__icontains=task_name)
        )

    # Search by Created Date
    if created_date:
        filtered_tasks = filtered_tasks.filter(
            created_at__date=created_date
        )

    # Search by Due Date
    if due_date:
        filtered_tasks = filtered_tasks.filter(
            due_date=due_date
        )

    print("Filter:", filter_type)
    print("Task Name:", task_name)
    print("Created Date:", created_date)
    print("Due Date:", due_date)
    print("Count:", filtered_tasks.count())

    context = {
        "total_tasks": total_tasks,
        "pending_count": pending_count,
        "completed_count": completed_count,
        "overdue_count": overdue_count,
        "overdue_tasks": overdue_tasks,
        "filtered_tasks": filtered_tasks,
        "page_title": page_title,
    }

    return render(request, "todo/home.html", context)

# ---------------------------
# All Tasks
# ---------------------------

def all_tasks(request):

    tasks = Task.objects.all().order_by("-created_at")

    context = {
        "title": "All Tasks",
        "tasks": tasks,
    }

    return render(request, "todo/task_list.html", context)


# ---------------------------
# Pending Tasks
# ---------------------------

def pending_tasks(request):

    tasks = Task.objects.filter(completed=False).order_by("-created_at")

    context = {
        "title": "Pending Tasks",
        "tasks": tasks,
    }

    return render(request, "todo/task_list.html", context)


# ---------------------------
# Completed Tasks
# ---------------------------

def completed_tasks(request):

    tasks = Task.objects.filter(completed=True).order_by("-created_at")

    context = {
        "title": "Completed Tasks",
        "tasks": tasks,
    }

    return render(request, "todo/task_list.html", context)


# ---------------------------
# Overdue Tasks
# ---------------------------

def overdue_tasks(request):

    tasks = Task.objects.filter(completed=False,due_date__lt=timezone.now().date()).order_by("due_date")

    context = {
        "title": "Overdue Tasks",
        "tasks": tasks,
    }

    return render(request, "todo/task_list.html", context)


# ---------------------------
# Add Task
# ---------------------------

def add_task(request):

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            title = form.cleaned_data["title"]

            if Task.objects.filter(title__iexact=title,completed=False).exists():

                messages.error(
                    request,
                    "A pending task with this title already exists."
                )

            else:

                form.save()
                messages.success(request,"Task added successfully.")

                return redirect("home")

    else:

        form = TaskForm()

    return render(request,"todo/add_task.html",{"form": form})


# ---------------------------
# Edit Task
# ---------------------------

def edit_task(request, pk):

    task = get_object_or_404(Task, pk=pk)

    filter_type = request.GET.get("filter")

    if request.method == "POST":

        form = TaskForm(request.POST, instance=task)

        if form.is_valid():

            form.save()

            if filter_type:
                return redirect(f"/?filter={filter_type}")

            return redirect("home")

    else:

        form = TaskForm(instance=task)

    return render(
        request,
        "todo/edit_task.html",
        {
            "form": form,
            "filter": filter_type,
        }
    )

# ---------------------------
# Delete Task
# ---------------------------

def delete_task(request, pk):

    task = get_object_or_404(Task, pk=pk)

    filter_type = request.GET.get("filter")

    if request.method == "POST":

        task.delete()

        messages.success(
            request,
            "Task deleted successfully."
        )

        if filter_type:
            return redirect(f"/?filter={filter_type}")

        return redirect("home")

    return render(
        request,
        "todo/delete_task.html",
        {
            "task": task,
            "filter": filter_type,
        }
    )


# ---------------------------
# Complete / Undo
# ---------------------------

def toggle_complete(request, pk):

    task = get_object_or_404(Task, pk=pk)

    task.completed = not task.completed
    task.save()

    filter_type = request.GET.get("filter")

    if filter_type:
        return redirect(f"/?filter={filter_type}")

    return redirect("home")