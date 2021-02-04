from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Note

class UserForm(UserCreationForm):
    class Meta(UserCreationForm): 
        model = User
        fields = ['username', 'first_name', 'email']

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['message']