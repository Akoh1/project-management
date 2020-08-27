from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Tasks, Status, Logs
from account.models import WorkPlace, AccountUser
from .forms import TasksForm
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request, workplace):
    workplace_id = get_object_or_404(WorkPlace, name=workplace)
    users = AccountUser.objects.filter(workplace_id=workplace_id, role='PR')
    projects = Project.objects.filter(workplace_id=workplace_id)
    context = {'projects': projects,
               'users': users
        }

    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        project_manager = request.POST.get('project_manager')
        print(project_manager)
        print("here")
        # manager_id = AccountUser.objects.get(id=project_manager)
        # print(manager_id)
        if project_name and project_manager:
            Project.objects.create(workplace_id=workplace_id, 
                                name=project_name,
                                project_manager_id=project_manager)
            return redirect('projects:index', workplace=workplace)
        else:
            messages.error(request, "Fill in the project name and project manager")
            return redirect('projects:index', workplace=workplace)

        # return redirect('projects:index', workplace=workplace)
    return render(request, 'project/project_index.html', context)

@login_required
def project_detail(request, workplace_id, slug):
    workplace_id = get_object_or_404(WorkPlace, name=workplace_id)
    project_id = get_object_or_404(Project, workplace_id=workplace_id, slug=slug)
    projects = Project.objects.filter(workplace_id=workplace_id, slug=slug)
    tasks = Tasks.objects.filter(project_id=project_id)
    status_id = get_object_or_404(Status, status='ass')
    user_id = get_object_or_404(AccountUser, pk=request.user.pk)

    if request.method == 'POST':
        if request.POST.get('task'):
            task_name = request.POST.get('task')
            with transaction.atomic():
                task_obj = Tasks.objects.create(
                    project_id=project_id,
                    user_id=user_id,
                    status_id=status_id,
                    name=task_name
                )
                mssg = "Task created on {0}\n assigned to {1}"
                date_field_to_date = task_obj.date_created.date()
                get_date = date_field_to_date.strftime("%Y-%m-%d")
                get_mssg = mssg.format(get_date, task_obj.user_id.full_name())
                Logs.objects.create(task_id=task_obj, messages=get_mssg)
                messages.success(request, "Your task has been created!")
                return redirect('projects:project-detail', workplace_id=workplace_id, slug=slug)

    context = {
        'tasks': tasks,
        'projects': projects
    }
    return render(request, 'project/project_detail.html', context)

@login_required
def task_detail(request, workplace_id, proj_slug, pk, task_name):
    # status = 
    if request.user.is_authenticated:
        workplace_id = get_object_or_404(WorkPlace, name=workplace_id)
        users = AccountUser.objects.filter(workplace_id=workplace_id)
        proj_detail = get_object_or_404(Project, workplace_id=workplace_id, slug=proj_slug)
        task_detail = get_object_or_404(Tasks, project_id=proj_detail,
                                        pk=pk, name=task_name)
        logs = Logs.objects.filter(task_id=task_detail).order_by('-date_created')
        curr_user_group = request.user.role
        mssg = ""

        if request.method == 'POST':
            if request.POST.get('task_name') or request.POST.get('assign_to') or \
               request.POST.get('status'):
                # status_obj = get_object_or_404(Status, status=request.POST.get('status'))
                # user_obj = get_object_or_404(AccountUser, pk=request.POST.get('pk'))
                    with transaction.atomic():
                        if request.POST.get('task_name'):
                            task_detail.name = request.POST.get('task_name')
                            mssg = "You Have changed this task name"
                        if request.POST.get('assign_to'):
                            user_obj = get_object_or_404(AccountUser, pk=request.POST.get('assign_to'))
                            task_detail.user_id = user_obj
                            mssg = "You have assigned this task to \n ----> {}".format(task_detail.user_id.full_name())
                        if request.POST.get('status'):
                            print(request.POST.get('status'))
                            status_obj = get_object_or_404(Status, status=request.POST.get('status'))
                            print(status_obj)
                            task_detail.status_id = status_obj
                            if task_detail.status_id.status == 'ass':
                                mssg = "Assigned"
                            elif task_detail.status_id.status == 'prog':
                                mssg = "in Progress"
                            elif task_detail.status_id.status == 'comp':
                                mssg = "Completed"
                            elif task_detail.status_id.status == 'test':
                                mssg = "in Testing"
                            elif task_detail.status_id.status == 'rev':
                                mssg = "in Review"
                            elif task_detail.status_id.status == 'appr':
                                mssg = "Approved"
                            elif task_detail.status_id.status == 'rel':
                                mssg = "Released Congratulations!"
                        get_mssg = "This task is now \n   -------> {}".format(mssg)
                        Logs.objects.create(task_id=task_detail, messages=get_mssg)
                        task_detail.save()
                        messages.success(request, "Your task has been Updated!")
                        return redirect('projects:task-detail',
                                        workplace_id=workplace_id.name, 
                                        proj_slug=proj_slug,
                                        pk=pk, task_name=task_name)

            if request.POST.get('message'):
                message = request.POST.get('message')
                Logs.objects.create(task_id=task_detail, messages=message)
                return redirect('projects:task-detail',
                                        workplace_id=workplace_id.name, 
                                        proj_slug=proj_slug,
                                        pk=pk, task_name=task_name)
            
            if request.POST.get('delete-task') == 'delete':
                task_detail.delete()
                messages.success(request, "Your task has been Deleted!")
                return redirect('projects:project-detail', workplace_id=workplace_id, slug=proj_slug)
    else:
        return redirect('account:home')

    
    context = {
        'task_detail': task_detail,
        'users': users,
        'logs': logs
    }
    return render(request, 'project/task_detail.html', context)

    