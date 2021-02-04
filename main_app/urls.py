from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/addprofile/', views.ProfileCreate.as_view(), name='profiles_create'),
    path('tech/', views.technologies_index, name='tech_index'),
    path('tech/create', views.TechnologieCreate.as_view(), name='tech_create'),
    path('apps/create', views.AppCreate.as_view(), name='apps_create'),
    path('apps/', views.apps_index, name='apps_index'),
    path('apps/<int:app_id>/assoc_user/', views.assoc_user, name='assoc_user'),
    path('apps/<int:app_id>/', views.apps_detail, name='apps_detail'),
    path('apps/<int:app_id>/addnote', views.apps_addnote, name='apps_addnote'),
     path('accounts/users/', views.users_index, name='users_index'),
]