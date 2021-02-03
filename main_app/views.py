from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# import uuid
# import boto3
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
# # Create your views here.
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm



def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('profiles_create')
    #   COME BACK AND CHANGE REDIRECT LOCATION
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


def technologies_index(request):
  tech = Technologie.objects.all()
  return render(request, '')

class ProfileCreate(LoginRequiredMixin, CreateView):
  model = Profile
  fields = ['photo', 'bio']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  success_url = '/'

#  class AppList(ListView):
#     model = App

# class AppCreate(CreateView):
#     model = App
#     fields = ['name', 'description', 'technologies']