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
        ordering = ('mailing_list',)

class OwnerEntry(models.Model):
    name = models.CharField(max_length=32)
    mailing_list = models.ForeignKey(ListEntry)

    class Meta:
        ordering = ('name',)


def send_first_warning(listEntry):
    print("First warning sent for {0} ".format(listEntry.name))


def send_last_warning(listEntry):
    print("Second warning sent for {0} ".format(listEntry.name))


#Return a list containing all expired lists.  Send warnings via email to list owners whose lists are expiring in 7 or 30 days.
def check_lists():

    month_from_now = datetime.now() + timedelta(days=30)
    week_from_now = datetime.now() + timedelta(days=7)

    expiring_lists = ListEntry.objects.filter(expire_date__lt=month_from_now)
    expired_lists = []

    for listEntry in expiring_lists:
        time_until_expire = listEntry.expire_date - 
        list_warning = ListWarning.objects.filter(mailing_list=listEntry.id)
        if list_warning.count() == 0:
            new_warning = ListWarning(mailing_list=listEntry, first_warning=True, last_warning=False)
            new_warning.save()
            send_first_warning(listEntry)

        if listEntry.expire_date <= datetime.date(month_from_now):

            list_warning = ListWarning.objects.filter(mailing_list=listEntry.id)
            if not list_warning:
                list_warning = ListWarning(mailing_list=listEntry, first_warning=True, last_warning=False)
                list_warning.save()
                send_first_warning()

        if listEntry.expire_date <= datetime.date(week_from_now):

            list_warning = ListWarning(mailing_list=listEntry)
            if list_warning.last_warning == False:
                list_warning.last_warning = True
                send_second_warning(listEntry)

        if listEntry.expire_date <= datetime.date(datetime.now()):
            expired_lists.append(listEntry)

    return expired_lists
