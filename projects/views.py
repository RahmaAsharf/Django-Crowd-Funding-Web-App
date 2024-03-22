from django.shortcuts import render, redirect
from django.http import HttpResponse
from projects.models import Project, Image, Tag, Category
from projects.forms import ProjectForm, ImageForm

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        files = request.FILES.getlist("image")
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            for file in files:
                Image.objects.create(project=project, image=file)
            form.save_m2m()  # Save many-to-many relationships
            return HttpResponse("Project added successfully")
    else:
        form = ProjectForm()
        image_form = ImageForm()
    
    tags = Tag.objects.all()
    categories = Category.objects.all()

    return render(request, "projects/create_project.html", {"form": form, "imageform": image_form, "tags": tags, "categories": categories})

# def create_project(request):

#     if request.method == "POST":
#         form = ProjectForm(request.POST)
#         files = request.FILES.getlist("image")
#         if form.is_valid():
#             f = form.save(commit=False)
#             f.user = request.user
#             f.save()
#             for i in files:
#                 Image.objects.create(project=f, image=i)
#             return HttpResponse("added")#-----------
#         else:
#             print(form.errors)
#     else:
#         form = ProjectForm()
#         imageform = ImageForm()

#     return render(request, "projects/create_project.html", {"form": form, "imageform": imageform})


# def try1(request):
#     return HttpResponse('hello')

# def create_project(request):
#     if request.method == "POST":
#         form = ProjectForm(request.POST)
#         files = request.FILES.getlist("image")
#         if form.is_valid():
#             f = form.save(commit=False)
#             f.user = request.user
#             f.save()
            
#             # Process and save tags
#             tag_names = request.POST.getlist("tags")  # Assuming the tags are submitted as a list
#             for tag_name in tag_names:
#                 tag, created = Tag.objects.get_or_create(name=tag_name)
#                 f.tags.add(tag)
            
#             # Save images
#             for i in files:
#                 Image.objects.create(project=f, image=i)
            
#             return HttpResponse("added")
#         else:
#             print(form.errors)
#     else:
#         form = ProjectForm()
#         imageform = ImageForm()
#         tags = Tag.objects.all()
#         return render(request, "projects/create_project.html", {"form": form, "imageform": imageform, "tags": tags})

#     tags = Tag.objects.all()
#     return render(request, "projects/create_project.html", {"form": form, "imageform": imageform, "tags": tags})

