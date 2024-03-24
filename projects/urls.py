from django.urls import path
from projects.views import create_project,view_projects, add_commentorrate

urlpatterns = [
    # path('try', try1)
    path('add', create_project, name="create_project"),
    path('view', view_projects, name="view_projects"),
    path('rate/<int:id>', add_commentorrate, name="add_commentorrate"),

]