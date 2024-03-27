from django.urls import include, path
from authentication.views import *

urlpatterns = [
    path('land', landing, name='landing'),
    path('register', register, name='register'),
    path('activate/<uuid:activation_key>/', activate_account, name='activate_account'),
    path('', include('django.contrib.auth.urls')),
    path('profile/<int:id>/', view_profile, name='view.profile'),
    path('profile/<int:id>/edit/', edit_profile, name='edit.profile'),
    path('profile/<int:id>/delete/', delete_account, name='delete.account'),
    
]