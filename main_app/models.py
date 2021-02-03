from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.TextField(default='https://t4america.org/wp-content/uploads/2016/10/Blank-User.jpg')
    bio = models.TextField(default='Hitting The Code Hard!')


class Technologie(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse('technologies_detail', kwargs={% 'pk': self.id %})


# class App(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=500)
#     tech = models.ManyToManyField(Technologie)
#     users = models.ManyToManyField(User)

#     def __str__(self):
#         return self.name


