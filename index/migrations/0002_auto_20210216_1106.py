# Generated by Django 3.1.4 on 2021-02-16 11:06

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0014_auto_20210214_1705'),
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='added',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='task',
            name='group',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='task',
            name='due',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
