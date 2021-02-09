from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Note, BuildLink, Subscribe

class UserForm(UserCreationForm):
    class Meta(UserCreationForm): 
        model = User
        fields = ['username', 'first_name', 'email']

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['message']

class BuildLinkForm(ModelForm):
    class Meta:
        model = BuildLink
        fields = ['name', 'link']

class SubscribeForm(ModelForm):
    class Meta:
        model = Subscribe
        fields = '__all__'
    
    