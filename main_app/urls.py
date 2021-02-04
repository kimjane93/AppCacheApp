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
    path('apps/<int:pk>/', views.AppDetail.as_view(), name='apps_detail')
]