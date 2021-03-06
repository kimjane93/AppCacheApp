from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Technologie, App, User, Note, BuildLink
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, NoteForm, BuildLinkForm, SubscribeForm
from django.db.models import Q
from appcache.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def home(request):
  subscribe_form = SubscribeForm()
  if request.method == 'POST':
    subscribe_form = SubscribeForm(request.POST)
    subject = 'Welcome To The Dev Community at App Cache'
    if request.user.is_authenticated:
      message = f'Hey {request.user.first_name}, thanks for subscribing to the App Cache Flash! We hope you enjoy sharing and comparing with your fellow coders. Create some app ideas here, implement a few ideas there, and be sure to network with each other on Linkedin!'
    else:
      message = f"Hey Friend, thanks for subscribing to the App Cache Flash! If you have already signed on with us, we hope you continue to enjoy sharing and comparing with your fellow coders. Create some app ideas here, implement a few ideas there, and be sure to network with each other on Linkedin! If you haven't decided on making an account yet, THIS is your sign to join the party, as one of my favorite coding instructors would say."
    recipient = str(subscribe_form['email'].value())
    send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently = False)
    return render(request, 'subscribe/success.html', {'recipient': recipient})
  return render(request, 'home.html', {'subscribe_form': subscribe_form})

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

@login_required
def users_index(request):
  users = User.objects.exclude(id=request.user.id)
  return render(request, 'accounts/index.html', {'users': users})

@login_required
def users_detail(request, user_id):
  current_user = User.objects.get(id=user_id)
  apps_you_dont_have = App.objects.exclude(users__exact=request.user)
  return render(request, 'accounts/detail.html', {'current_user': current_user, 'apps_you_dont_have': apps_you_dont_have})

@login_required
def profile(request):
  user = User.objects.get(id=request.user.id)
  return render(request, 'accounts/profile.html', {'user': user})


@login_required
def subscribe(request):
  subscribe_form = SubscribeForm()
  if request.method == 'POST':
    subscribe_form = SubscribeForm(request.POST)
    subject = 'Welcome To The Dev Community at App Cache'
    message = 'Thanks for subscribing to the App Cache Flash! We hope you enjoy sharing and comparing with your fellow coders. Create some app ideas here, implement a few ideas there, and be sure to network with each other on Linkedin!'
    recipient = str(subscribe_form['email'].value())
    send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently = False)
    return render(request, 'subscribe/success.html', {'recipient': recipient})
  return render(request, 'home.html', {'subscribe_form': subscribe_form})

@login_required
def apps_index(request):
  apps = App.objects.all()
  apps_you_dont_have = App.objects.exclude(users__exact=request.user)
  tech = Technologie.objects.all()
  return render(request, 'apps/index.html', {'apps_you_dont_have': apps_you_dont_have, 'apps': apps, 'tech': tech})

@login_required
def apps_detail(request, app_id):
  app = App.objects.get(id=app_id)
  user = User.objects.get(id=request.user.id)
  note_form = NoteForm()
  buildlink_form = BuildLinkForm()
  creator = User.objects.get(id=app.creator)
  return render(request, 'apps/detail.html', {
    'app': app, 'user': user, 'note_form': note_form, 'buildlink_form': buildlink_form, 'creator': creator})

@login_required
def apps_addlink(request, app_id):
  form = BuildLinkForm(request.POST)
  if form.is_valid():
    new_buildlink = form.save(commit=False)
    new_buildlink.app_id = app_id
    new_buildlink.user_id = request.user.id
    new_buildlink.save()
  return redirect('apps_detail', app_id=app_id)

@login_required
def assoc_user(request, app_id):
  App.objects.get(id=app_id).users.add(request.user)
  return redirect('apps_detail', app_id=app_id)

@login_required
def attached_users(request, app_id):
  app = App.objects.get(id=app_id)
  apps_you_dont_have = App.objects.exclude(users__exact=request.user)

  return render(request, 'apps/attached_users.html', {'app': app, 'apps_dont_dont_have': apps_you_dont_have})

@login_required
def apps_addnote(request, app_id):
  form = NoteForm(request.POST)
  if form.is_valid():
    new_note = form.save(commit=False)
    new_note.app_id = app_id
    new_note.user_id = request.user.id
    new_note.save()
  return redirect('apps_detail', app_id=app_id)

@login_required
def disassoc_user(request, app_id):
  app = App.objects.get(id=app_id)
  app.users.remove(request.user.id)
  return redirect('profile')

@login_required
def apps_search(request):
  query = request.GET.get('q')
  apps = App.objects.filter(Q(tech__exact=query))
  tech = Technologie.objects.all()

  return render(request, 'apps/search_results.html', {'apps': apps, 'tech': tech} )

@login_required
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
    self.object = form.save(commit=False)
    self.object.creator = self.request.user.id
    self.object = form.save()
    App.objects.get(id=self.object.id).users.add(self.request.user)
    return redirect('/apps/')