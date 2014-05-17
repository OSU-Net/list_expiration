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


class Command(BaseCommand):
    help = """ Manages list expiration.  If lists are expiring soon, sends an email warning the list owners
               If a list has expired, the .pck file associated with that list is deleted
           """

    def handle(self, *args, **options):
        expired_lists = check_lists()
        
        for listEntry in expired_lists:
        	#delete the list on file 
            subprocess.call(["./remove_list {0}".format(listEntry.list_name)])

            #delete the list from the database
            listEntry.delete()
            owners = OwnerEntry.objects.filter(list_id=listEntry.id)
            owners.delete()



