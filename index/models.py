from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.shortcuts import render, reverse, redirect, get_object_or_404


# User._meta.get_field('email')._unique = True

class Status(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=25)



class Task(models.Model):
    def __str__(self) :
        return self.title

    title = models.CharField(max_length=50, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=False, default=1)
    status = models.ForeignKey(Status, on_delete=models.SET_DEFAULT, default=5, blank=False)
    # status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL)

    description = models.CharField(max_length=200, blank=False)
    moreinfo = models.TextField(blank=True)
    due = models.DateField(default=datetime.datetime.now, blank=False)
    added = models.DateTimeField(default=datetime.datetime.now, blank=True)

class Notification(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    notification =  models.CharField(max_length=50)
    read = models.BooleanField(default=False)

class Comment(models.Model):
    class Meta:
        ordering = ['-date_added']
    def __str__(self):
        return '%s /%s' % (self.title, self.user)
    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    title = models.CharField(max_length=50, blank=True, default="")
    date_added = models.DateTimeField(auto_now_add=True)


def create_task(sender, instance, created, **kwargs):
    
    if created:
        task = Task.objects.get(title=instance)
        user = User.objects.get(username=task.user)
        noti = Notification(user=user, notification="You have a new task", task=task)
        noti.save()
        print(noti)


post_save.connect(create_task, sender=Task)


def update_task(sender, instance, created, **kwargs):
    if created == False:
        task = Task.objects.get(title=instance)
        user = User.objects.get(username=task.user)
        noti = Notification(user=user, notification="You have a new task", task=task)
        noti.save()
        print(noti)

post_save.connect(update_task, sender=Task)
