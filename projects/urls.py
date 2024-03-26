from django.urls import path
from projects.views import create_project, view_projects, donate, delete_project, project_page, submit_review 

urlpatterns = [
    # path('try', try1)
    path('add', create_project, name="create_project"),
    path('view', view_projects, name="view_projects"),
    path('submit_review/<int:project_id>/',submit_review, name='submit_review'),
    path('donate/<int:id>', donate , name="donate"),
    path('delete/<int:id>', delete_project, name='delete_project'),
    path('view/<int:id>', project_page, name="project_page"),



]