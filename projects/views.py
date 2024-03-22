from django.shortcuts import render, redirect
from django.http import HttpResponse
from projects.models import Project, Image, Tag, Category
from projects.forms import ProjectForm, ImageForm

def create_project(request):

    if request.method == "POST":
        form = ProjectForm(request.POST)
        files = request.FILES.getlist("image")
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            for i in files:
                Image.objects.create(project=f, image=i)
            return HttpResponse("added")#-----------
        else:
            print(form.errors)
    else:
        form = ProjectForm()
        imageform = ImageForm()

    return render(request, "projects/create_project.html", {"form": form, "imageform": imageform})


# def try1(request):
#     return HttpResponse('hello')
