from django.urls import path
from projects.views import *

urlpatterns = [
    # path('try', try1)
    path('add', create_project, name="create_project"),
    path('view', view_projects, name="view_projects"),
    path('delete/<int:id>', delete_project, name='delete_project'),
    path('view/<int:id>', project_page, name="project_page"),
    path('add_rate/<int:project_id>/', add_rate, name='add_rate'),
    path('add_comment/<int:project_id>/', add_comment, name='add_comment'),
    path('donate/<int:id>', donate , name="donate"),
    path('home', top_projects, name="home"),
    path('report/<int:id>', report_project, name="report_project"),
    path('reportview/<int:id>', view_all_reports, name="view_reports"),
    path('projects/', view_user_projects, name='view_user_projects'),
    path('donations/', view_user_donations, name='view_user_donations'),
    path('reportcomment<int:project_id>/<int:comment_id>/', report_comment, name='report_comments'),
    
]