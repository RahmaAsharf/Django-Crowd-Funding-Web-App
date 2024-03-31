from django.urls import path
from my_admin.views import *

urlpatterns = [

    path('categories', category_list, name="category_list"),
    path('category', create_category, name="create_category"),
    path('category/<int:id>/update/', update_category, name='update_category'),
    path('category/<int:id>/delete/', delete_category, name='delete_category'),
    path('projects', project_list, name="project_list"),
    path('feture_projects', feture_projects, name="feture_projects"),
]