# Generated by Django 3.2.12 on 2022-02-06 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('processes', '0002_initial'),
        ('tasks', '0002_task_configuration'),
        ('tools', '0001_initial'),
        ('targets', '0001_initial'),
        ('resources', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='process',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='processes.process'),
        ),
        migrations.AddField(
            model_name='task',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='targets.target'),
        ),
        migrations.AddField(
            model_name='task',
            name='tool',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tools.tool'),
        ),
        migrations.AddField(
            model_name='task',
            name='wordlists',
            field=models.ManyToManyField(blank=True, related_name='wordlists', to='resources.Wordlist'),
        ),
    ]
