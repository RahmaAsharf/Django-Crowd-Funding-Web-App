from django.urls import path
from authentication.views import *

urlpatterns = [
    path('land', landing, name='landing'),
    path('register', register, name='register'),
    path('profile/<int:id>/', view_profile, name='view.profile'),
    path('profile/<int:id>/edit/', edit_profile, name='edit.profile'),
    path('profile/<int:id>/delete/', delete_account, name='delete.account'),
    
]