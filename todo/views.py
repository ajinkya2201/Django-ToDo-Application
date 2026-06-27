from pyexpat.errors import messages
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import get_object_or_404, render,redirect
from .models import Task
from .forms import  TaskForm



from django.utils import timezone

def home(request):

    pending_tasks = Task.objects.filter(
        completed=False
    ).order_by("-created_at")

    completed_tasks = Task.objects.filter(
        completed=True
    ).order_by("-created_at")

    total_tasks = Task.objects.count()

    pending_count = pending_tasks.count()

    completed_count = completed_tasks.count()

    overdue_count = Task.objects.filter(
        completed=False,
        due_date__lt=timezone.now().date()
    ).count()

    context = {
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,

        "total_tasks": total_tasks,
        "pending_count": pending_count,
        "completed_count": completed_count,
        "overdue_count": overdue_count,
    }

    return render(request, "todo/index.html", context)




def add_task(request):

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            title = form.cleaned_data["title"]

            if Task.objects.filter(
                title__iexact=title,
                completed=False
            ).exists():

                messages.error(
                    request,
                    "A pending task with this title already exists."
                )

            else:

                form.save()

                messages.success(
                    request,
                    "Task added successfully."
                )

                return redirect("home")

    else:

        form = TaskForm()

    return render(
        request,
        "todo/add_task.html",
        {"form": form}
    )


def edit_task(request,pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:

        form = TaskForm(instance=task)

    return render(request,"todo/edit_task.html",{"form": form})


def delete_task(request,pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
            task.delete()
        
            return redirect("home")

    return render(request,"todo/delete_task.html",{"task": task})


def toggle_complete(request,pk):
     task = get_object_or_404(Task,pk=pk)

     task.completed = not task.completed
     task.save()
     return redirect("home")
