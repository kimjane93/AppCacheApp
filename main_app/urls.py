from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    # path('apps/', views.AppList, name='index'),
    # path('apps/create/', views.AppCreate, name='apps_create'),
]