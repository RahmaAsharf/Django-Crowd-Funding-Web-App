# from django.contrib.auth.decorators import user_passes_test

# def user_is_admin(user):
#     return user.is_authenticated and user.is_superuser 

# admin_login_required = user_passes_test(user_is_admin)

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect

# def admin_login_required(function=None):
#     actual_decorator = user_passes_test(
#         lambda u: u.is_authenticated and u.is_staff,
#         login_url='/authentication/login/'
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator



def admin_required(view_func):
    """
    Decorator for views that checks whether the user is an admin.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            # User is logged in and is an admin
            return view_func(request, *args, **kwargs)
        else:
            # User is not logged in or is not an admin
            # You can redirect them to a different page or show an error message
            return HttpResponse("You are not authorized to access this page.")
    return _wrapped_view