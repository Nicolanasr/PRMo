from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# User._meta.get_field('email')._unique = True

class Status(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=25)

class Task(models.Model):
    def __str__(self) :
        return self.title

    title = models.CharField(max_length=50, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, default=2)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=False, default=1)
    status = models.ForeignKey(Status, on_delete=models.SET_DEFAULT, default=5, blank=False)
    # status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL)

    description = models.CharField(max_length=200, blank=False)
    moreinfo = models.TextField(blank=True)
    due = models.DateField(default=datetime.datetime.now, blank=False)
    added = models.DateTimeField(default=datetime.datetime.now, blank=True)
