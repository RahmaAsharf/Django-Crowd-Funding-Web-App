from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from projects.models import Project,Image, Tag, Category, Rating, Report, Donation , Comment
from projects.forms import DonationForm, ProjectForm, RatingForm, CommentForm, RatingForm , ReportForm
from decimal import Decimal
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Avg
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required(login_url='/authentication/login/')
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        files = request.FILES.getlist("files")
        file_urls = []

        if form.is_valid():
            project = form.save(commit=False)
            project.user_id = request.user.id
            project.save()  # Save the project before adding tags

            new_tags_str = request.POST.get('new_tags', '')
            if new_tags_str:
                new_tags = [tag.strip() for tag in new_tags_str.split(',') if tag.strip()]
                for tag_name in new_tags:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    project.tags.add(tag)  # Associate the tag with the project

            for file in files:
                new_file = Image(project=project, file=file)
                new_file.save()
                file_urls.append(new_file.file.url)

            form.save_m2m()  # Save many-to-many relationships after saving the project
            return redirect('view_projects')
    else:
        form = ProjectForm()
    
    tags = Tag.objects.all()
    categories = Category.objects.all()

    return render(request, "projects/create_project.html", {"form": form, "tags": tags, "categories": categories})



def view_projects(request):
    all_projects = Project.objects.all()
    print (all_projects)
    return render(request, 'projects/view_project.html', context={"Projects": all_projects , })

def project_page(request, id):
    project = Project.objects.get(id=id)
    projects = Project.objects.all()
    report_elements= Report.objects.filter(project_id=id)
    report_count =0
    for report in report_elements:
        if report.comment_id is None :
            report_count += 1 

    
    projectOwner= request.user.id 

    can_delete = False
    
    # Check if the current user is the creator of the project
    if project.user_id == projectOwner:
        # Convert 0.25 to Decimal and then perform multiplication
        quarter_total = project.total * Decimal('0.25')
        
        # Check if donations are less than 25% of the total value
        if project.totalDonate() < quarter_total:
            can_delete = True

    matching_projects = []
    unique_project_ids = set()

    for mytag in project.tags.all():
        for pro in projects:
            flag = False
            for tag in pro.tags.all():
                if flag == False:
                    if pro.id != project.id and mytag.name == tag.name:
                        flag = True
                        if pro.id not in unique_project_ids:
                            matching_projects.append(pro)
                            unique_project_ids.add(pro.id)
                        
                        break  # Break out of the inner loop
            
    return render(request, 'projects/project_page.html', {'project': project, 'can_delete': can_delete , 'matching_projects': matching_projects , 'report_count':report_count, 'projectOwner':projectOwner})

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

@login_required(login_url='/authentication/login/')
def delete_project(request, id):
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        project.delete()
        return redirect("view_projects") 
       
    return render(request, 'projects/delete.html', {'project': project})
@login_required(login_url='/authentication/login/')
def delete_comment(request,comment_id):
        
        comment = Comment.objects.get(id=comment_id)
        if request.method == 'POST':
            project_id = comment.project_id
            comment.delete()
            return redirect('project_page', id=project_id)
       
        return render(request, 'projects/delete_comment.html', {'comment': comment})

@login_required(login_url='/authentication/login/')
def add_rate(request, project_id):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.project_id = project_id
            data.user_id = request.user.id
            data.save()
            return redirect('project_page', id=project_id)
        else:
            # Handle form validation errors
            print("Form errors:", form.errors)
            return render(request, 'projects/errors.html', {'errors': form.errors})
            # Render the errors.html template with form errors
    return redirect('project_page', id=project_id)

# def add_rate(request, project_id):
#     url = request.META.get('HTTP_REFERER')
#     if request.method == 'POST':
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             data = form.save(commit=False)
#             data.project_id = project_id
#             data.user_id = request.user.id  
#             data.save()
#             return redirect(url)
#         # error retuen
#     return redirect(url)
@login_required(login_url='/authentication/login/')
def add_comment(request, project_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.project_id = project_id
            data.user_id = request.user.id
            data.save()
            return redirect('project_page', id=project_id)
        # error retuen
    return redirect('project_page', id=project_id)


@login_required(login_url='/authentication/login/')
def donate(request, id):
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        donation_form = DonationForm(request.POST,project_id=id)
        if donation_form.is_valid():
            donation = donation_form.save(commit=False)
            donation.project_id = id
            donation.user_id = request.user.id
            donation.save()
            return redirect('project_page', id=id)
        else:
            # Form validation failed, re-render context with errors
            context = {
                'project': project,
                'donation_form': donation_form,
            }
            return render(request, 'projects/project_page.html', context)
    else:
        donation_form = DonationForm()
    context = {
        'project': project,
        'donation_form': donation_form,
    }
    return render(request, 'projects/project_page.html', context)   
      
@login_required(login_url='/authentication/login/')
def report_project(request, id):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.project_id = id
            report.user = request.user 
            report.save()
            return redirect('project_page', id=id)  # Redirect to the project detail page
    else:
        form = ReportForm()
    
    return render(request, 'projects/report.html', {'form': form})  

#////////////////////////////////////////////////////////////////////////
def view_all_reports(request, id):

    all_reports = Report.objects.filter(project_id=id)
    return render(request, 'projects/view_reports.html', {'all_reports': all_reports , "id":id })

###############Report Comment############
@login_required(login_url='/authentication/login/')
def report_comment(request, project_id, comment_id):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.project_id = project_id
            report.user = request.user 

            # Associate the report with the comment
            report.comment_id = comment_id

            report.save()

            return redirect('project_page', id=project_id)  # Redirect to the project detail page
    else:
        form = ReportForm()
    
    return render(request, 'projects/reportcomment.html', {'form': form})
################################################################################
def top_projects(request):
    today = timezone.now()
    running_projects = Project.objects.filter(endDate__gte=today)
    sorted_projects = sorted(running_projects, key=lambda x: x.averageReview(), reverse=True)[:5]
    latest_projects = Project.objects.order_by('-created_at')[:5]
    categories = Category.objects.all()
    return render(request, 'projects/home.html', {'top_projects': sorted_projects,'latest_projects': latest_projects,'categories': categories})

def category_projects(request, category_id):
    category = Category.objects.get(pk=category_id)
    catprojects = Project.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request,'projects/catproject.html',  {'catprojects': catprojects, 'categories': categories , 'cat_name':category.name})

def tag_projects(request, tag_name):
    tag = Tag.objects.filter(name=tag_name).first()
    tagprojects = Project.objects.filter(tags=tag) if tag else Project.objects.none()
    return render(request, 'projects/tagproject.html', {'tagprojects': tagprojects, 'tag_name': tag_name})

# *************************\ View Pojects & Donations for only Logged in User /*************************
@login_required(login_url='/authentication/login/')
def view_user_projects(request):
    user_projects = Project.objects.filter(user=request.user)
    return render(request, 'projects/view_user_projects.html', {'user_projects': user_projects})

@login_required(login_url='/authentication/login/')
def view_user_donations(request):
    user_donations = Donation.objects.filter(user=request.user)
    return render(request, 'projects/view_user_donations.html', {'user_donations': user_donations})
@login_required(login_url='/authentication/login/')
def user_projects(request,id):

    user_projects = Project.objects.filter(user=id)
    return render(request, 'projects/user_same_projects.html', {'user_projects': user_projects })

# *************************\ Search projects by title or tag /*************************
from django.contrib import messages

def search_projects(request):
    query = request.GET.get('search_query')
    if not query:
        messages.warning(request, 'Please enter a search query.')
        return render(request, 'projects/search.html')

    projects = Project.objects.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).distinct()
    return render(request, 'projects/search.html', {'projects': projects, 'query': query})







