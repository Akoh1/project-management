from django.contrib import admin
from .models import Project, Status, Logs, Tasks
# Register your models here.
admin.site.register(Project)
admin.site.register(Status)
admin.site.register(Logs)
admin.site.register(Tasks)