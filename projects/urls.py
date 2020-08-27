from django.urls import path
from . import views

app_name = 'projects'

# admin.site.login = custom.site.login

urlpatterns = [
    path('<workplace>', views.index, name='index'),
    path('<workplace_id>/<slug:slug>', views.project_detail, name="project-detail"),
    path('<workplace_id>/<slug:proj_slug>/<int:pk>/<str:task_name>', views.task_detail, name="task-detail"),
    # path('<workplace_id>/<slug:proj_slug>/<int:pk>/<str:task_name>', views.task_delete, name="task-delete"),
]