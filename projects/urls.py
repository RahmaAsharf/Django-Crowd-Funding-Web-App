from django.urls import path
from projects.views import create_project

urlpatterns = [
    # path('try', try1)
    path('add', create_project, name="create_project")

]