from django.shortcuts import render
from django.http import HttpResponse
from projects.models import Category, Project, Tag
from projects.forms import CategoryForm , TagForm
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import admin_login_required



@admin_login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin/categories.html', {'categories': categories})

@admin_login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'admin/create_category.html', {'form': form})

@admin_login_required
def update_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        # Prepopulate the form field with the existing category name
        form = CategoryForm(instance=category, initial={'name': category.name})
    return render(request, 'admin/create_category.html', {'form': form})

@admin_login_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'delete_category.html', {'category': category})

@admin_login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'admin/projects.html', {'projects': projects})

@admin_login_required
def feture_projects(request):
    if request.method == 'POST':
        project_ids = request.POST.getlist('projects')
        Project.objects.filter(id__in=project_ids).update(isFeatured=True)
        return redirect('home')
    
    return redirect('project_list')