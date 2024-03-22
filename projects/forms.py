from django import forms
from projects.models import Project, Image

class ProjectForm(forms.ModelForm):
    class Meta:
        model= Project
        fields='__all__'


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