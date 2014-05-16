from django.db import models
#from datetime.datetime import *
from datetime import *

class ListEntry(models.Model):
    name = models.CharField(max_length=64)
    # active_date = models.DateTimeField('date of last list activity')
    expire_date = models.DateField('date of expiration')
    create_date = models.DateField('date created')

class ListWarning(models.Model):
    mailing_list = models.ForeignKey(ListEntry)
    first_warning = models.BooleanField()
    last_warning = models.BooleanField()

    class Meta:
        ordering = ('email_list',)

class OwnerEntry(models.Model):
    name = models.CharField(max_length=32)
    mailing_list = models.ForeignKey(ListEntry)

    class Meta:
        ordering = ('name',)

#Return a list containing all expired lists.  Send warnings via email to list owners whose lists are expiring in 7 or 30 days.
def check_lists():

    month_from_now = datetime.datetime.now() + datetime.timedelta(days=30)
    week_from_now = datetime.datetime.now()
    expired_lists = ListEntry.objects.filter(expire_date__lt=month_from_now)

    for listEntry in expiring_lists:

        list_warning = ListWarning.objects.get(listEntry.id)
        if not list_warning:
            new_warning = ListWarning(list_id=listEntry.id, first_warning=True, last_warning=False)
            new_warning.save()
            send_first_warning(listEntry)

        if listEntry.expire_date <= week_from_now:
            list_warning = ListWarning(list_id=listEntry.id)
            list_warning.second_warning = True
            send_second_warning(listEntry)

        if listEntry.expire_date <= datetime.now():
            expired_lists.append(listEntry)

    return expired_lists
