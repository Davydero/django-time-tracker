from django.db import models
from django.contrib.auth.models import User #user es una tabla predefinida de django

job_type = [
    (1, 'Meeting'),
    (2, 'Visit to a client'),
    (3, 'Quotation elaboration'),
    (4, 'Engineering work'),
    (5, 'Other')
]
# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=50)
    job = models.IntegerField(null=True, blank=False, choices=job_type)
    description = models.CharField(max_length =100)
    month = models.CharField(max_length=50, null=True)
    day = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    #init_time = models.DateTimeField(null=True)
    #finish_time = models.DateTimeField(null=True, blank=True)
    init_time = models.TimeField(null=True)
    finish_time = models.TimeField(null=True, blank=True)
    durationH = models.IntegerField(null=True)
    durationm = models.IntegerField(null=True)
    #datecompleted = models.DateTimeField(null=True, blank=True)
    #important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) #Relaciona la tabla de tareas con la de usuarios. ademas si se borra un usuario se borran sus tareas asociadas

    def __str__(self):
        return self.title + '- by '+ self.user.username