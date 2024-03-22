from django.contrib import admin
from projects.models import Project, Category, Image, Tag

admin.site.register([Project, Category, Image, Tag])
