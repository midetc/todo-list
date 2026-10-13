from django.urls import path

from tasks.views import ListTaskView, CreateTaskView

urlpatterns = [
    path("", ListTaskView.as_view(), name="task-list"),
    path("task/create/", CreateTaskView.as_view(), name="task-create"),
]



app_name = "tasks"