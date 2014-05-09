from django.core.management.base import BaseCommand, CommandError
from list_app.models import ListEntry, ListWarning
from datetime import *
import os

MAILMAN_FILES_DIR = "./test_lists"
FIRST_WARNING_TIME = 30
SECOND_WARNING_TIME = 7


def delete_list(list_name):
    list_dirs = [x[0] for x in os.walk(MAILMAN_FILES_DIR)];
    for list in list_dirs:
        if list == list_name:
            #call a shell script which copies the list to a temporary directory and tars it
            #delete original copy of the list

    print("list deleted ;)")


def date_delta_days(earlier_date, later_date):
    return (later_date - earlier_date).days


def send_second_warning(list_entry):
    print("second warning sent ;)")


def send_first_warning(list_entry):
    print("first warning sent ;)")


class Command(BaseCommand):
    help = """ Manages list expiration.  If lists are expiring soon, sends an email warning the list owners
               If a list has expired, the .pck file associated with that list is deleted
           """

    def handle(self, *args, **options):
        print("hello")
        #grab all lists expiring in a month or less
        month_from_now = datetime.datetime.now() + datetime.timedelta(days=30)
        week_from_now = datetime.datetime.now()
        expiring_lists = ListEntry.objects.filter(expire_date__lt=month_from_now)
        print("hello world!")

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

