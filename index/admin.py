from django.contrib import admin
from .models import Task, Status, Comment
# Register your models here.

admin.site.register(Task)
# admin.site.register(UserProfile)
admin.site.register(Status)
admin.site.register(Comment)