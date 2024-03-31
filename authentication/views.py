from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from DjangoProject.settings import DOMAIN
from authentication.forms import  UserModelForm, UserProfileForm
from authentication.models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.contrib import messages


# Create your views here.
def landing(request):
    return render(request,"authentication/landing.html")
def profile(request):
    url = reverse('landing')
    return redirect(url)

User = get_user_model()

def register(request):

    if request.method == 'POST':
        form = UserModelForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User is not active until activated via email
            user.save()
            # Send activation email
            activation_link = request.build_absolute_uri(reverse('activate_account', args=[user.activation_key]))
            send_activation_email(user.first_name,user.email, activation_link)
            return HttpResponse("Please check your email to activate your account.")
    else:
        form = UserModelForm()
    
    return render(request, 'authentication/register.html', {'form': form})


def send_activation_email(first_name, email, activation_link):
    timestamp = timezone.now().timestamp()
    subject = 'Activate your account'
    message = f'Hello {first_name},\n\nPlease click the following link to activate your account: {activation_link}'
    send_mail(subject, message, 'guihadyosry@gmail.com', [email])
    

def activate_account(request, activation_key):
    user = get_object_or_404(CustomUser, activation_key=activation_key)

    # Check if timestamp is provided in the activation link
    timestamp = request.GET.get('timestamp')
    if timestamp:
        # Calculate the difference between the current time and the timestamp
        current_time = timezone.now().timestamp()
        time_difference = current_time - float(timestamp)

        # If more than 24 hours have passed, show activation link expired message
        if time_difference > 24 * 60 * 60:  # 24 hours in seconds
            return render(request, 'authentication/activation_link_expired.html')

    user.is_active = True
    user.save()
    return redirect('landing')

@login_required
def view_profile(request, id):
    user = get_object_or_404(CustomUser, pk=id)
    return render(request, 'authentication/profile.html', {'user': user})

@login_required
def edit_profile(request, id):
    user = get_object_or_404(CustomUser, pk=id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('view.profile', id=id)
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'authentication/edit_profile.html', {'form': form, 'id': id})

@login_required
def delete_account(request, id):
    user = get_object_or_404(CustomUser, pk=id)
    if request.method == 'POST':
        user.delete()
        return redirect('landing') 
    return render(request, 'authentication/delete_account.html', {'user': user})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password1 = form.cleaned_data.get('new_password1')
            if old_password == new_password1:
                form.add_error('new_password1', "New password can't be same as the old password!")
            else:
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('view.profile', id=request.user.id)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'authentication/change_password.html', {'form': form})


# def password_reset(request):
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             # Check if the provided email exists in the database
#             email = form.cleaned_data['email']
#             if User.objects.filter(email=email).exists():
#                 # If the email exists, proceed with sending the reset password email
#                 user = User.objects.get(email=email)
#                 uid = urlsafe_base64_encode(force_bytes(user.pk))
#                 token = default_token_generator.make_token(user)
#                 reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
#                 reset_url = request.build_absolute_uri(reset_url)
#                 email_subject = 'Password Reset Request'
#                 email_body = render_to_string('registration/password_reset_email.html', {
#                     'user': user,
#                     'reset_url': reset_url,
#                 })
#                 send_mail(email_subject, email_body, None, [email])
#                 messages.success(request, 'Password reset email has been sent.')
#                 return HttpResponseRedirect(reverse('password_reset_done'))
#             else:
#                 # If the email does not exist, display an error message
#                 messages.error(request, 'This email is not registered. Please try again.')
#     else:
#         form = PasswordResetForm()
#     return render(request, 'registration/password_reset_form.html', {'form': form})