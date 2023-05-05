from django.forms import ModelForm
from .models import Task
from django.contrib.admin import widgets
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title','job', 'description','init_time','finish_time']
        widgets = {
            'init_time': AdminTimeWidget(),
            'finish_time': AdminTimeWidget(),
        }