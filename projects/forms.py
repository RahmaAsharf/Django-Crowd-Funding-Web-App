from django import forms
from projects.models import Project
from .models import Donation, Tag, Category, Rating , Report , Comment

from django.core.exceptions import ValidationError
from datetime import datetime
from django.shortcuts import get_object_or_404

class ProjectForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label='Category')
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, label='Tags')


    class Meta:
        model = Project
        fields = ['title', 'details', 'total', 'category', 'startDate', 'endDate', 'tags']
        widgets = {
            'startDate': forms.DateInput(attrs={'type': 'date'}),
            'endDate': forms.DateInput(attrs={'type': 'date'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'total': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total <= 0:
            raise ValidationError("Target amount must be greater than 0.")
        return total

    def clean_startDate(self):
        start_date = self.cleaned_data.get('startDate')
        if start_date and datetime.now().date() > start_date:
            raise ValidationError("Start date shouldn't be less than today.")
        return start_date

    def clean_endDate(self):
        start_date = self.cleaned_data.get('startDate')
        end_date = self.cleaned_data.get('endDate')

        if start_date and end_date:
            if end_date <= start_date:
                raise ValidationError("End date should be greater than start date.")
        
        return end_date


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = [ 'rating']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        self.project_id = kwargs.pop('project_id', None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0.")
        if self.project_id:
            project = get_object_or_404(Project, pk=self.project_id)
            total_donated = project.totalDonate()
            if amount+total_donated > project.total:
                raise forms.ValidationError("Donation amount exceeds project's funding goal.")
        return amount
    


class ReportForm(forms.ModelForm):
    status_ = (('Hateful Speech','Hateful Speech'),('Profanity', 'Profanity'),
                ('Abuse', 'Abuse'),('Violence','Violence'),
                ('Irrelevant','Irrelevant'))

    status = forms.ChoiceField(choices=status_)

    class Meta:
        model = Report
        fields = ['reason','status']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError("Category with this name already exists.")
        return name

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name']
        if Tag.objects.filter(name=name).exists():
            raise forms.ValidationError("Tag with this name already exists.")
        return name


  