from django.urls import path
from projects.views import create_project,view_projects

urlpatterns = [
    # path('try', try1)
    path('add', create_project, name="create_project"),
    path('view', view_projects, name="view_projects")

]