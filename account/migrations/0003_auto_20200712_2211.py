# Generated by Django 3.0.7 on 2020-07-12 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_accountuser_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountuser',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
