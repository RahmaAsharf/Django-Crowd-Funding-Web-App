from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from projects.models import Project,Image, Tag, Category, Rating, Report
from projects.forms import DonationForm, ProjectForm, RatingForm, CommentForm, RatingForm , ReportForm
from decimal import Decimal
from django.utils import timezone

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        files = request.FILES.getlist("files")
        file_urls = []

        if form.is_valid():
            project = form.save(commit=False)
            # project.user_id = 1  # Assuming user_id needs to be set to 1
            project.user_id = request.user.id
            project.save()

            for file in files:
                new_file = Image(project=project, file=file)
                new_file.save()
                file_urls.append(new_file.file.url)

            form.save_m2m()
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
    report_count = Report.objects.filter(project_id=id).count()
    

    can_delete = False
    
    # Check if the current user is the creator of the project
    if project.user_id == 1 :
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
            
    return render(request, 'projects/project_page.html', {'project': project, 'can_delete': can_delete , 'matching_projects': matching_projects , 'report_count':report_count })

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

        
def add_rate(request, project_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.project_id = project_id
            #data.user_id = request.user.id
            data.user_id = 1  
            data.save()
            return redirect(url)
        # error retuen
    return redirect(url)

def add_comment(request, project_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.project_id = project_id
            #data.user_id = request.user.id
            data.user_id = 1  
            data.save()
            return redirect(url)
        # error retuen
    return redirect(url)

def donate(request, id):
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        donation_form = DonationForm(request.POST,project_id=id)
        if donation_form.is_valid():
            donation = donation_form.save(commit=False)
            donation.project_id = id
            #data.user_id = request.user.id
            donation.user_id = 1
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
def top_projects(request):

    today = timezone.now().date()
    running_projects = Project.objects.filter(startDate__lte=today,endDate__gte=today)
    print(running_projects)
    sorted_projects = sorted(running_projects, key=lambda x: x.averageReview(), reverse=True)[:2]
    return render(request, 'projects/home.html', {'top_projects': sorted_projects})
      

def report_project(request, id):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.project_id = id
            # report.user = request.user  # Assuming the user is logged in
            report.user_id = 1
            report.save()
            return redirect('project_page', id=id)  # Redirect to the project detail page
    else:
        form = ReportForm()
    
    return render(request, 'projects/report.html', {'form': form})  

def view_all_reports(request, id):
    # Retrieve all reports for the specified project ID
    
    all_reports = Report.objects.filter(project_id=id)
    return render(request, 'projects/view_reports.html', {'all_reports': all_reports , "id":id })

def top_projects(request):

    today = timezone.now().date()
    running_projects = Project.objects.filter(startDate__lte=today,endDate__gte=today)
    print(running_projects)
    sorted_projects = sorted(running_projects, key=lambda x: x.averageReview(), reverse=True)[:2]
    return render(request, 'projects/home.html', {'top_projects': sorted_projects})







