from django.forms import ModelForm
from index.models import Task, Comment
from django import forms

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        fields = ['title', 'status', 'description', 'moreinfo', 'due']
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['user'].widget.attrs['required'] = False

# class CommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['body']