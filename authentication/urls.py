from django.urls import include, path
from authentication.views import landing,register,activate_account

urlpatterns = [
    path('land', landing, name='landing'),
    path('register', register, name='register'),
    path('activate/<uuid:activation_key>/', activate_account, name='activate_account'),
    path('', include('django.contrib.auth.urls')),
    
]