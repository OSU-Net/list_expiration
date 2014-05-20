'''
    1) Parse all .pck files and populate the OwnerTransition table with [owner_email, list_name] entries
    2) Send and email out to all owners linking them to a form where they can authenticate their lists
    3) Mark down all bounced emails
'''
import sys, os
from django.core.management.base import BaseCommand, CommandError
from list_app.models import *
from list_site import settings

class Command(BaseCommand):
    help = """ This command is used to begin the transition process which will migrate list owners
               over to ONID.  Only list owners that possess ONID accounts will be able to manage the
               expiration of the list(s) that they manage.
           """

    def handle(self, *args, **options):
    	#foreach list:
        #	unpickle the pck file

        list_dirs = [x[0] for x in os.walk(settings.MAILMAN_FILES_DIR + '/lists')] #trailing slash needed here?
        print(list_dirs)

        for list_name in list_dirs:
        	pck_file = None
        	try:
        		pck_file = open(settings.MAILMAN_FILES_DIR + '/lists/' + list_name + '/{0}.pck'.format(list_name),'r')
        	except IOERROR as e:
        		print("I/O error({0}): {1}".format(e.errno, e.strerror))
        		print("List {0} files corrupted or missing".format(list_dir))
        		break

        	for key in pck_file:
        		print (key + ':' + pck_file[key] + '\n')

