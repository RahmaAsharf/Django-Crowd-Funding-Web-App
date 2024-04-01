from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from DjangoProject import settings
from authentication.models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

User = get_user_model()

class UserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model  = CustomUser
        fields= ('first_name', 'last_name', 'email', 'username', 'password','confirm_password','mobile_phone','profile_picture')
    
         
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password
        
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password
    
    def clean_email(self):
        email = self.cleaned_data['email']
        validate_email(email)
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("User already exists")
        return email

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        if not mobile_phone.startswith('01') or len(mobile_phone) != 11:
            raise forms.ValidationError("Please enter a valid Egyptian phone number")
        return mobile_phone
    
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        user.confirm_password = make_password(self.cleaned_data["confirm_password"])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model  = CustomUser
        fields= ('first_name', 'last_name', 'mobile_phone', 'profile_picture', 'birthdate', 'facebook_profile', 'country')
        
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        if not mobile_phone.startswith('01') or len(mobile_phone) != 11:
            raise forms.ValidationError("Please enter a valid Egyptian phone number")
        return mobile_phone

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user 
    
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Passwords do not match.")
        return new_password2



class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _("Please enter a correct username and password. Note that your account has to be activated to be able to login."),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
                # Authenticate user
                user = authenticate(username=username, password=password)
                if user is not None:
                    if not user.is_active:
                        raise self.get_inactive_error()
                else:
                    # Handle invalid login
                    raise self.get_invalid_login_error()

        return super().clean()

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )

    def get_inactive_error(self):
        return forms.ValidationError(
            self.error_messages['inactive'],
            code='inactive',
        )