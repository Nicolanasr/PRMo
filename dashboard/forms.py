from django.forms import ModelForm
from index.models import Task
from django import forms

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        # fields = ['title', 'group', 'status', 'description', 'moreinfo', 'due']
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['user'].widget.attrs['required'] = False