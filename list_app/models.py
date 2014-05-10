from django.db import models
#from datetime.datetime import *
from datetime import *

class ListEntry(models.Model):
    name = models.CharField(max_length=64)
    # active_date = models.DateTimeField('date of last list activity')
    expire_date = models.DateField('date of expiration')
    create_date = models.DateField('date created')

class ListWarning(models.Model):
    list = models.ForeignKey(ListEntry)
    first_warning = models.BooleanField()
    last_warning = models.BooleanField()

    class Meta:
        ordering = ('list_id',)

class OwnerEntry(models.Model):
    name = models.CharField(max_length=32)
    list_id = models.ForeignKey(ListEntry)

    class Meta:
        ordering = ('name',)

# class ListEntry(models.Model):
#     name = models.CharField(max_length=64)
#     owners = models.CharField(max_length=256)
#     create_date = models.DateTimeField('date created')
#     active_date = models.DateTimeField('date of last list activity')
#     expire_date = models.DateTimeField('date of expiration')
#     creator = models.CharField(max_length=64)
#     descr = models.CharField(max_length=256)
#     notes = models.CharField(max_length=2048)
#     automated = models.IntegerField(max_length=11)
#     server = models.CharField(max_length=64)
#     data1 = models.CharField(max_length=256)
#     data2 = models.CharField(max_length=256)
#
#     testKeys = models.ManyToManyField('TestEntry')
#
#     def HasOwner(self, name):
#         owner_list = self.owners.split(', ', len(owners))
#         for owner in owner_list:
#             if owner == name:
#                 return True
#
#         return False

# Create your models here.
