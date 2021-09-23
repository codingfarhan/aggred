from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('verify/<auth_token>', views.verify_email, name='very_email'),
    path('settings_', views.settings_, name='settings_'),
    path('settings_/change_email', views.change_email, name='change_email'),
    path('settings_/change_password', views.change_password, name='change_password'),
    path('settings_/change_title', views.change_title, name='change_title'),
    path('settings_/delete_confirmation', views.delete_confirmation, name='delete_confirmation'),
    path('settings_/change_name', views.change_name, name='change_name')

]