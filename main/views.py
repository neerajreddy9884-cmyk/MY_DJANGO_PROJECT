from django.shortcuts import render, redirect
from .models import Task

def home(request):
    if request.method == "POST":
        action = request.POST.get("action")
        task_id = request.POST.get("task_id")

        # 1. CREATE ACTION
        if action == "add":
            title_from_form = request.POST.get("task_title")
            if title_from_form:
                Task.objects.create(title=title_from_form)

        # 2. COMPLETE ACTION
        elif action == "complete" and task_id:
            try:
                task = Task.objects.get(id=task_id)
                task.completed = True
                task.save()
            except Task.DoesNotExist:
                pass

        # 3. DELETE ACTION
        elif action == "delete" and task_id:
            try:
                task = Task.objects.get(id=task_id)
                task.delete()
            except Task.DoesNotExist:
                pass

        return redirect('home')  # Refresh the page cleanly

    all_tasks = Task.objects.all() 
    return render(request, 'home.html', {'tasks': all_tasks})
