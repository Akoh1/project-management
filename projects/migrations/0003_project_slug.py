# Generated by Django 3.0.7 on 2020-07-12 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20200712_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
