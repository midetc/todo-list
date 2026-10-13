from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from tasks.forms import TaskForm
from tasks.models import Task


class ListTaskView(ListView):
    model = Task
    queryset = Task.objects.prefetch_related("tags").order_by("done", "-datetime")


class CreateTaskView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")

class UpdateTaskView(UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class DeleteTaskView(DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")



