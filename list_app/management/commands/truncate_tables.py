from list_site import settings
from list_app.models import *
from django.core.management.base import BaseCommand, CommandError
import sys, os, shutil, pdb, subprocess

class Command(BaseCommand):
    
    def truncate_all_tables(self):
        List.objects.all().delete()
        ListWarning.objects.all().delete()
        Owner.objects.all().delete()
        OldList.objects.all().delete()
        OldOwner.objects.all().delete()


    def handle(self, *args, **options):
        print("WARNING:  this command will delete all table entries for this application.  It is not intended to be used outside of a testing environment.  Only use it if you are entirely sure of what you are doing!")

        decision = raw_input("continue? [y/N]")
        if decision == 'y':
            self.truncate_all_tables()
        elif decision is not 'n' and decision is not 'N' and decision is not None:
            print("Invalid input: please enter y, n or N!")

