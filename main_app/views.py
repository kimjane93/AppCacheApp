from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# import uuid
# import boto3
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
# # Create your views here.
from .models import Profile, Technologie, App, User, Note
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, NoteForm
# from django.contrib.auth.models import User
from django.http import HttpResponseRedirect



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

def users_index(request):
  users = User.objects.exclude(id=request.user.id)
  return render(request, 'accounts/index.html', {'users': users})

def users_detail(request, user_id):
  current_user = User.objects.get(id=user_id)
  apps_you_dont_have = App.objects.exclude(users__exact=request.user)
  return render(request, 'accounts/detail.html', {'current_user': current_user, 'apps_you_dont_have': apps_you_dont_have})

def technologies_index(request):
  tech = Technologie.objects.all()
  return render(request, 'technologies/index.html', {'tech': tech})

class ProfileCreate(LoginRequiredMixin, CreateView):
  model = Profile
  fields = ['photo', 'bio', 'linkedin', 'github']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  success_url = '/accounts/profile/'

class ProfileUpdate(LoginRequiredMixin, UpdateView):
  model = Profile
  fields = ['photo', 'bio', 'github', 'linkedin']
  success_url='/accounts/profile/'


class TechnologieCreate(LoginRequiredMixin, CreateView):
  model = Technologie
  fields = '__all__'
  success_url = '/tech/'

class AppCreate(LoginRequiredMixin, CreateView):
  model = App
  fields = ['name', 'description', 'tech']

  def form_valid(self, form):
    self.object = form.save()
    App.objects.get(id=self.object.id).users.add(self.request.user)
  
    return redirect('/apps/')

def apps_index(request):
  apps = App.objects.exclude(users__exact=request.user)
  print(apps)
  return render(request, 'apps/index.html', {'apps': apps})

def assoc_user(request, app_id):
  App.objects.get(id=app_id).users.add(request.user)
  return redirect('apps_detail', app_id=app_id)

def apps_detail(request, app_id):
  app = App.objects.get(id=app_id)
  note_form = NoteForm()
  return render(request, 'apps/detail.html', {
    'app': app, 'note_form': note_form})

def apps_addnote(request, app_id):
  form = NoteForm(request.POST)
  if form.is_valid():
    new_note = form.save(commit=False)
    new_note.app_id = app_id
    new_note.user_id = request.user.id
    new_note.save()
  return redirect('apps_detail', app_id=app_id)

def profile(request):
  user = User.objects.get(id=request.user.id)
  return render(request, 'accounts/profile.html', {'user': user})

def disassoc_user(request, app_id):
  app = App.objects.get(id=app_id)
  app.users.remove(request.user.id)
  return redirect('profile')

