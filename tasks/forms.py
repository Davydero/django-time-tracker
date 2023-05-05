from django import forms
from .models import Task
from django.contrib.admin import widgets
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','job', 'description','init_time','finish_time']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            #'job': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'init_time': AdminTimeWidget(),
            'finish_time': AdminTimeWidget(),
        }