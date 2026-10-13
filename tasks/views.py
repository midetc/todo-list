from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from tasks.models import Task


# Create your views here.

class ListTasksView(ListView):
    model = Task
