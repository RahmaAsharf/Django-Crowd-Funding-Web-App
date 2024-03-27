from django.urls import path
from projects.views import create_project,view_projects, add_commentorrate,donate, delete_project,project_page,top_projects

urlpatterns = [
    # path('try', try1)
    path('add', create_project, name="create_project"),
    path('view', view_projects, name="view_projects"),
    path('rate/<int:id>', add_commentorrate, name="add_commentorrate"),
    path('donate/<int:id>', donate , name="donate"),
    path('delete/<int:id>', delete_project, name='delete_project'),
    path('view/<int:id>', project_page, name="project_page"),
    path('home', top_projects, name="top_projects"),


]