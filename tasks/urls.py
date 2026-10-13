from django.urls import path

from tasks.views import ListTasksView

urlpatterns = [
    path("", ListTasksView.as_view(), name="task-list"),

]



app_name = "tasks"