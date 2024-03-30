# from django.contrib.auth.decorators import user_passes_test

# def user_is_admin(user):
#     return user.is_authenticated and user.is_superuser 

# admin_login_required = user_passes_test(user_is_admin)

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def admin_login_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='/authentication/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator