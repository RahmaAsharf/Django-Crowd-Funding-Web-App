from django.urls import path
from projects.views import create_project, view_projects, donate, delete_project, project_page, add_rate, add_comment

urlpatterns = [
    # path('try', try1)
    path('add', create_project, name="create_project"),
    path('view', view_projects, name="view_projects"),
    path('add_rate/<int:project_id>/', add_rate, name='add_rate'),
    path('add_comment/<int:project_id>/', add_comment, name='add_comment'),
    path('donate/<int:id>', donate , name="donate"),
    path('delete/<int:id>', delete_project, name='delete_project'),
    path('view/<int:id>', project_page, name="project_page"),



]