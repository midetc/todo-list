from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from tasks.forms import TagForm, TaskForm
from tasks.models import Tag, Task


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


class ListTagView(ListView):
    model = Tag
    queryset = Tag.objects.order_by("name")


class CreateTagView(CreateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("tasks:tag-list")


class UpdateTagView(UpdateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("tasks:tag-list")


class DeleteTagView(DeleteView):
    model = Tag
    success_url = reverse_lazy("tasks:tag-list")


class ToggleTaskView(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.done = not task.done
        task.save(update_fields=["done"])
        return redirect("tasks:task-list")
