from django.urls import path
from projects.views import create_project,view_projects,donate, delete_project,project_page,top_projects, project_page, add_rate, add_comment, report_project, view_all_reports
from projects.views import top_projects
urlpatterns = [
    # path('try', try1)
    path('add', create_project, name="create_project"),
    path('view', view_projects, name="view_projects"),
    path('delete/<int:id>', delete_project, name='delete_project'),
    path('view/<int:id>', project_page, name="project_page"),
    path('add_rate/<int:project_id>/', add_rate, name='add_rate'),
    path('add_comment/<int:project_id>/', add_comment, name='add_comment'),
    path('donate/<int:id>', donate , name="donate"),
    path('home', top_projects, name="top_projects"),
    path('report/<int:id>', report_project, name="report_project"),
    path('reportview/<int:id>', view_all_reports, name="view_reports"),
]