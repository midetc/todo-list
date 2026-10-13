from django.urls import path

from tasks.views import (
    CreateTagView,
    CreateTaskView,
    DeleteTagView,
    DeleteTaskView,
    ListTagView,
    ListTaskView,
    ToggleTaskView,
    UpdateTagView,
    UpdateTaskView,
)

urlpatterns = [
    path("", ListTaskView.as_view(), name="task-list"),
    path("task/create/", CreateTaskView.as_view(), name="task-create"),
    path("task/<int:pk>/update/", UpdateTaskView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", DeleteTaskView.as_view(), name="task-delete"),
    path("task/<int:pk>/toggle/", ToggleTaskView.as_view(), name="task-toggle"),
    path("tags/", ListTagView.as_view(), name="tag-list"),
    path("tags/create/", CreateTagView.as_view(), name="tag-create"),
    path("tags/<int:pk>/update/", UpdateTagView.as_view(), name="tag-update"),
    path("tags/<int:pk>/delete/", DeleteTagView.as_view(), name="tag-delete"),
]


app_name = "tasks"
