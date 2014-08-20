from django.core.management.base import BaseCommand, CommandError
from list_app.models import *
from datetime import *
from list_site import settings
import os
import subprocess


# def delete_list(list_name):
#     list_dirs = [x[0] for x in os.walk(MAILMAN_FILES_DIR)];
#     for list in list_dirs:
#         if list == list_name:
#             #call a shell script which copies the list to a temporary directory and tars it
#             #delete original copy of the list

#     print("list deleted ;)")


def date_delta_days(earlier_date, later_date):
    return (later_date - earlier_date).days


def send_second_warning(list_entry):
    print("second warning sent ;)")


def send_first_warning(list_entry):
    print("first warning sent ;)")


#Return a list containing all expired lists.  Send warnings via email to list owners whose lists are expiring in 7 or 30 days.
def check_lists():

    now = datetime.now()
    month_from_now = datetime.now() + timedelta(days=30)
    week_from_now = datetime.now() + timedelta(days=7)

    expiring_lists = ListEntry.objects.filter(expire_date__lt=month_from_now)
    expired_lists = []
    
    for listEntry in expiring_lists:

        list_warning = ListWarning.objects.filter(mailing_list=listEntry.id)
        
        if list_warning.count() == 0:
            new_warning = ListWarning(mailing_list=listEntry, first_warning=True, last_warning=False)
            new_warning.save()
            send_first_warning(listEntry)

        # if listEntry.expire_date <= datetime.date(month_from_now):

        #     list_warning = ListWarning.objects.filter(mailing_list=listEntry.id)
        #     if not list_warning:
        #         list_warning = ListWarning(mailing_list=listEntry, first_warning=True, last_warning=False)
        #         list_warning.save()
        #         send_first_warning()

        if listEntry.expire_date <= datetime.date(week_from_now):

            list_warning = ListWarning.objects.get(mailing_list=listEntry)

            if not list_warning.last_warning:
                list_warning.last_warning = True
                list_warning.save()
                send_last_warning(listEntry)

        if listEntry.expire_date <= datetime.date(datetime.now()):
            expired_lists.append(listEntry)

    return expired_lists


class Command(BaseCommand):
    help = """ Manages list expiration.  If lists are expiring soon, sends an email warning the list owners
               If a list has expired, the .pck file associated with that list is deleted
           """

    def handle(self, *args, **options):
        expired_lists = check_lists()
        
        for listEntry in expired_lists:

            print(__file__)
            print(listEntry.name)
            print(settings.MAILMAN_FILES_DIR)

            #delete the list on file
            cmd_str = './remove_list {0} {1} {2}'.format(listEntry.name, settings.MAILMAN_LISTS_DIR, settings.MAILMAN_SCRIPTS_DIR)
            subprocess.call(cmd_str, shell=True)

            #delete the list from the database
            (OwnerEntry.objects.get(lists__in=listEntry)).delete() 
            (ListWarning.objects.get(mailing_list=listEntry)).delete()
            listEntry.delete()



