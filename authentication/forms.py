from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from authentication.models import CustomUser

class UserModelForm(forms.ModelForm):
    class Meta:
        model  = CustomUser
        # fields = '__all__'
        # Retreive all form data except email field 
        exclude = ['email']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    # called when creating an instance of form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if the form is used to edit an existing user (instance has a primary key)
        if self.instance.pk:
            self.fields['password'].required = False # password is not required
        else:
            self.fields['password'].required = True # password is required

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User already exists")
        return email

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        if not mobile_phone.startswith('01') or len(mobile_phone) != 11:
            raise forms.ValidationError("Please enter a valid Egyptian phone number")
        return mobile_phone
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Check if the instance is an existing user or not
        if self.instance.pk:
            old_password = CustomUser.objects.get(pk=self.instance.pk).password
            if check_password(password, old_password):
                raise forms.ValidationError("New password can't be same as old password")
        return password
    
    def save(self, commit=True):
        self.instance.password = make_password(password=self.instance.password)
        super().save()
        return self.instance
