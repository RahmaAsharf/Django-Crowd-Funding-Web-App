from django.urls import path
from authentication.views import landing,register

urlpatterns = [
    path('land', landing, name='landing'),
    path('register', register, name='register')
    
]