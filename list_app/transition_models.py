from django.db import models

class OldList(models.Model):
    list_name = models.CharField(max_length=32, blank=False)

class OldOwner(models.Model):
    owner_email = models.CharField(max_length=32, blank=False)
    onid_email = models.CharField(max_length=32, blank=True)
    link_code = models.CharField(max_length=32, blank=True)
    bounced = models.BooleanField(blank=True)
    lists = models.ManyToManyField(OldList)


