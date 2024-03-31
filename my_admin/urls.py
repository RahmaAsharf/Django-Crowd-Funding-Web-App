from django.urls import path
from my_admin.views import *

urlpatterns = [
    path('categories', category_list, name="category_list"),
    path('category', create_category, name="create_category"),
    path('category/<int:id>/update/', update_category, name='update_category'),
    path('category/<int:id>/delete/', delete_category, name='delete_category'),
    path('tags', tag_list, name="tag_list"),
    path('tag', create_tag, name="create_tag"),
    path('tag/<int:id>/update/', update_tag, name='update_tag'),
    path('tag/<int:id>/delete/', delete_tag, name='delete_tag'),
    path('projects', project_list, name="project_list"),
    path('feature_projects', feature_projects, name="feature_projects"),
]