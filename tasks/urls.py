from django.urls import path

from tasks.views import (
    CreateTaskView,
    DeleteTaskView,
    ListTaskView,
    UpdateTaskView,
)

urlpatterns = [
    path("", ListTaskView.as_view(), name="task-list"),
    path("task/create/", CreateTaskView.as_view(), name="task-create"),
    path("task/<int:pk>/update/", UpdateTaskView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", DeleteTaskView.as_view(), name="task-delete"),
]



app_name = "tasks"