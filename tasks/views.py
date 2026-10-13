from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from tasks.forms import TaskForm
from tasks.models import Task


class ListTaskView(ListView):
    model = Task
    queryset = Task.objects.prefetch_related("tags").order_by("done", "-datetime")


class CreateTaskView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")