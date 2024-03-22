from django import forms
from projects.models import Project, Image
from .models import Tag, Category
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
        fields = '__all__'

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