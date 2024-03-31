from django.urls import include, path
from authentication.views import *
from django.contrib.auth.views import LoginView
from authentication.forms import CustomAuthenticationForm

urlpatterns = [
    path('land', landing, name='landing'),
    path('register', register, name='register'),
    path('activate/<uuid:activation_key>/', activate_account, name='activate_account'),
    path('', include('django.contrib.auth.urls')),
    path('profile/<int:id>/', view_profile, name='view.profile'),
    path('profile/<int:id>/edit/', edit_profile, name='edit.profile'),
    path('profile/<int:id>/delete/', delete_account, name='delete.account'),
    path('change-password/', change_password, name='change_password'),
    path('accounts/login/', LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
]