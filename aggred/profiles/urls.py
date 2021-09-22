from django.urls import path
from . import views


urlpatterns = [
    path('settings', views.settings, name='settings'),
    path('settings/change_email', views.change_email, name='change_email'),
    path('settings/change_password', views.change_password, name='change_password'),
    path('settings/change_title', views.change_title, name='change_title'),
    path('settings/delete_confirmation', views.delete_confirmation, name='delete_confirmation'),
    path('settings/change_name', views.change_name, name='change_name')

]