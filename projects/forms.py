from django import forms
from projects.models import Project, Image
from .models import Donation, Tag, Category, Rating
from django.core.exceptions import ValidationError

# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model= Project
#         fields='__all__'
class ProjectForm(forms.ModelForm):
    # Add category field
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label='Category')
    # Add tags field
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, label='Tags')

    class Meta:
        model = Project
        # fields = '__all__'
        fields = ['title', 'details', 'category', 'total', 'startDate', 'endDate', 'tags']
        
        
    # def clean_totalDonated(self):
    #     total= self.cleaned_data.get('total')
    #     if self.instance and self.instance.totalDonate > total:
    #         raise forms.ValidationError("this exceed total donatetd")

        
    # def clean_totalDonated(self):
    #     total= self.cleaned_data.get('total')
    #     if self.instance and self.instance.totalDonate > total:
    #         raise forms.ValidationError("this exceed total donatetd")

        
class MultipleClearableFileInput(forms.ClearableFileInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['multiple'] = True

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image",)
        widgets = {
            'image': MultipleClearableFileInput()
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['comment', 'rating']
        
class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']
    def clean_amount(self):
        amount= self.cleaned_data['amount']
        if amount < 0:
             raise forms.ValidationError("amount must be an integer number")
        return amount

    # def clean(self):
    #     cleaned_data = super().clean()
    #     start_date = cleaned_data.get('startDate')
    #     end_date = cleaned_data.get('endDate')
    #     total = cleaned_data.get('total')
    #     print("Total:", total)
    #     if total and total <= 0:
    #         self.add_error('total', 'Total must be greater than zero.')


    #     if start_date and end_date and start_date >= end_date:
    #         self.add_error('endDate', 'End date must be greater than start date.')

    #     return cleaned_data

# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         fields = ("image",)
#         widgets = {
#             'image': forms.ClearableFileInput(attrs={'allow_multiple_selected': True})
#         }