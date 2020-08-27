from django.db import models
from account.models import AccountUser, WorkPlace
from django.urls import reverse
from django.template.defaultfilters import slugify

status = (
    ('ass', 'Assigned'),
    ('prog', 'In Progress'),
    ('comp', 'Completed'),
    ('test', 'Testing'),
    ('rev', 'Review'),
    ('appr', 'Approved'),
    ('rel', 'Released')
)

# Create your models here.

class Project(models.Model):
    workplace_id = models.ForeignKey(WorkPlace, on_delete=models.CASCADE)
    project_manager = models.ForeignKey(AccountUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(verbose_name='date created', auto_now_add=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name

    def assigned(self):
        var = Status.objects.get(status='ass')
        return self.tasks_set.filter(status_id_id=var)

    def progress(self):
        var = Status.objects.get(status='prog')
        return self.tasks_set.filter(status_id_id=var)

    def completed(self):
        var = Status.objects.get(status='comp')
        return self.tasks_set.filter(status_id_id=var)

    def testing(self):
        var = Status.objects.get(status='test')
        return self.tasks_set.filter(status_id_id=var)

    def review(self):
        var = Status.objects.get(status='rev')
        return self.tasks_set.filter(status_id_id=var)

    def approved(self):
        var = Status.objects.get(status='appr')
        return self.tasks_set.filter(status_id_id=var)

    def released(self):
        var = Status.objects.get(status='rel')
        return self.tasks_set.filter(status_id_id=var)

    def get_absolute_url(self):
        return reverse('projects:project-detail', kwargs={'workplace_id': self.workplace_id, 'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Status(models.Model):
    status = models.CharField(max_length=15, choices=status, null=True, blank=True)

    def __str__(self):
        return self.status


class Tasks(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(AccountUser, on_delete=models.SET_NULL, null=True)
    status_id = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=256)
    date_created = models.DateTimeField(verbose_name='date created', auto_now_add=True)

    def __str__(self):
        return self.name


class Logs(models.Model):
    task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    messages = models.TextField()
    date_created = models.DateTimeField(verbose_name='date created', auto_now_add=True)

    def __str__(self):
        return self.messages
