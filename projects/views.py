from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from projects.models import Project, Image, Tag, Category, Rating
from projects.forms import DonationForm, ProjectForm, ImageForm, RatingForm
from decimal import Decimal

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        files = request.FILES.getlist("image")
        if form.is_valid():
            project = form.save(commit=False)
            # project.user = request.user
            project.user_id = 1
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
    return render(request, 'projects/view_project.html', context={"Projects": all_projects , })

def project_page(request, id):
    project = Project.objects.get(id=id)
    can_delete = False
    
    # Check if the current user is the creator of the project
    if project.user_id == 1 :
        # Convert 0.25 to Decimal and then perform multiplication
        quarter_total = project.total * Decimal('0.25')
        
        # Check if donations are less than 25% of the total value
        if project.totalDonate() < quarter_total:
            can_delete = True
            
    return render(request, 'projects/project_page.html', {'project': project, 'can_delete': can_delete})

# def delete_conditions(request, id):
#     project = Project.objects.get(id=id)
#     can_delete = False
    
#     # Check if the current user is the creator of the project
#     # if request.user == project.user:
#     if project.user_id == 1 :
#         # Calculate 25% of the total value
#         quarter_total = project.total * 0.25
        
#         # Check if donations are less than 25% of the total value
#         if project.totalDonate() < quarter_total:
#             can_delete = True
#     return render(request, 'projects/view_project.html', {'project': project, 'can_delete': can_delete}

def delete_project(request, id):
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        project.delete()
        return redirect("view_projects") 
       
    return render(request, 'projects/delete.html', {'project': project})




def add_commentorrate(request, id):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.project_id = id
            data.user_id = 1
            #data.user_id = request.user.id
            data.save()
            return redirect('project_page', id=id) 
    else:
        form = RatingForm()
    return render(request, 'projects/rate.html', {'form': form})
   
def donate(request, id):
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        donation_form = DonationForm(request.POST,project_id=id)
        if donation_form.is_valid():
            donation = donation_form.save(commit=False)
            donation.project_id = id
            donation.user_id = 1
            donation.save()
            return redirect('project_page', id=id)
    else:
        donation_form = DonationForm()
    context = {
        'project': project,
        'donation_form': donation_form,
    }
    return render(request, 'projects/project_page.html', context)            

# def donate(request, id):
#     if request.method == 'POST':
#         form = DonationForm(request.POST)
#         if form.is_valid():
#             data = form.save(commit=False)
#             data.project_id = id
#             data.user_id = 1  # Assuming user_id is hardcoded for testing
#             data.save()
#             return redirect('project_page', id=id)
#     else:
#         form = DonationForm()
#         return render(request, 'projects/donate.html', {'form': form}) 


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

