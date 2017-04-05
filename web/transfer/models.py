from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    content = models.CharField(max_length=200,default='not provided')
    style = models.CharField(max_length=200,default='not provided')
    output = models.CharField(max_length=200,default='nothing')
    finished = models.BooleanField(default=False)
    sub_time = models.TimeField('time submitted')
    fin_time = models.TimeField('time finished',null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Slave(models.Model):
    addr = models.CharField(max_length=200)
    busy = models.BooleanField(default=False)
    task = models.ForeignKey(Task,on_delete=models.DO_NOTHING)