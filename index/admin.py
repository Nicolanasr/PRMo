from django.contrib import admin
from .models import Task, Status, Comment, Notification
# Register your models here.

admin.site.register(Task)
# admin.site.register(UserProfile)
admin.site.register(Status)
admin.site.register(Comment)
admin.site.register(Notification)