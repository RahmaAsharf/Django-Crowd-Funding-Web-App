from django.shortcuts import render, redirect
from django.http import HttpResponse
from projects.models import Project, Image, Tag, Category, Rating
from projects.forms import ProjectForm, ImageForm, RatingForm

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
            return redirect(form.instance.show_url)
    else:
        form = ProjectForm()
        image_form = ImageForm()
    
    tags = Tag.objects.all()
    categories = Category.objects.all()

    return render(request, "projects/create_project.html", {"form": form, "imageform": image_form, "tags": tags, "categories": categories})

def view_projects(request):
    all_projects = Project.objects.all()
    print (all_projects)
    return render(request, 'projects/view_project.html', context={"Projects": all_projects})


def add_commentorrate(request, id):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.project_id = id
            data.user_id = 1
            #data.user_id = request.user.id
            data.save()
            return redirect('view_projects')  
    else:
        form = RatingForm()
    return render(request, 'projects/rate.html', {'form': form})
   


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

