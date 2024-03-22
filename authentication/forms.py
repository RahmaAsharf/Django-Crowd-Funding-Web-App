from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from authentication.models import CustomUser

class UserModelForm(forms.ModelForm):
    class Meta:
        model  = CustomUser
        fields = '__all__'

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
    
    def save(self, commit=True):
        self.instance.password = make_password(password=self.instance.password)
        super().save()
        return self.instance
