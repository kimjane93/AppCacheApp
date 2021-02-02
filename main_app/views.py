from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# import uuid
# import boto3
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
# # Create your views here.
from .models import App, Profile, Note, Build_stat, Technologie


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class AppList(ListView):
    model = App

class AppCreate(CreateView):
    model = App
    fields = ['name', 'description', 'technologies']