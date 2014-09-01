'''
     1) Parse all .pck files and populate the OwnerTransition table with [owner_email, list_name] entries
     2) Send and email out to all owners linking them to a form where they can authenticate their lists
     3) Mark down all bounced emails
'''
import sys, os
from django.core.management.base import BaseCommand, CommandError
from list_app.models import *
from list_site import settings
import cPickle as pickle  
import os, binascii
import hashlib
import datetime

import pdb

class Command(BaseCommand):
    help = """ This command is used to begin the transition process which will migrate list owners
    over to ONID.  Only list owners that possess ONID accounts will be able to manage the
    expiration of the list(s) that they manage.
    """
    def send_transition_email_onid(self, onid_email):
        print('transition email sent to {0}'.format(onid_email))

    def send_transition_email(self, email_addr): 
        link_code = OldOwner.objects.get(owner_email=email_addr).link_code;
        link = 'localhost:8000/lists/onid_transition/?id={0}'.format(link_code)

        print('link for {0} is: {1}'.format(email_addr, link))


    def get_mailman_list_names(self):

        list_dirs = [x[0] for x in os.walk(settings.MAILMAN_LISTS_DIR + '/lists/')]
        list_names = []

        for list_dir in list_dirs:
            strs = list_dir.split('/')
            if strs[len(strs)-1] == '':
                continue
            else:
                list_names.append(strs[len(strs)-1])

        return list_names

    def owner_is_onid(self, owner_email):

        strs = owner_email.split('@')
        if strs[len(strs) - 1] == 'onid.oregonstate.edu' or strs[len(strs) - 1] == 'onid.orst.edu':
            return True

        return False

    def generate_link_codes(self):
        unique_owners = OldOwner.objects.order_by('owner_email').values('owner_email').distinct()
        
        links = {}

        for owner in unique_owners:

            while True:
                link_val = binascii.b2a_hex(os.urandom(15)) # each owner is uniquely identified by a 15 bit hex string

                if link_val in links.values():
                    continue
                else:
                    links[owner['owner_email']] = link_val
                    break

        return links

    def handle(self, *args, **options):
        #foreach list:
        #    unpickle the pck file

        #list_dirs = [x[0] for x in os.walk(settings.MAILMAN_FILES_DIR + '/lists')] #trailing slash needed here?
        list_names = self.get_mailman_list_names()

        for list_name in list_names:
            if list_name == "mailman":
                continue #ignore the default Mailman list

            pck_dict = None
            
            try:
                pck_file = open(settings.MAILMAN_LISTS_DIR + '/lists/' + list_name + '/config.pck','r')
                pck_dict = pickle.load(pck_file)

            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
                print("List {0} files corrupted or missing".format(list_name))
                break
            except pickle.PickleError as e:
                print("Pickle error{0}: {1}".format(e.errno, e.strerror))
            
            pdb.set_trace()
            
            list_create_date = datetime.date.fromtimestamp(pck_dict['created_at'])
            old_list = OldList(name=list_name, create_date=list_create_date)
            old_list.save()

            for owner_email in pck_dict['owner']:
                # transition_entry = OldOwner()
                # transition_entry.owner_email = owner_email
                # transition_entry.list_name = pck_dict['real_name']
                # transition_entry.bounced = False

                try:
                    owner = OldOwner.objects.get(owner_email=owner_email)

                except OldOwner.DoesNotExist:
                                        
                    owner = OldOwner(owner_email=owner_email)
                    owner.owner_email = owner_email
                    owner.save()

                    if self.owner_is_onid(owner_email):
                        owner.onid_email = owner.owner_email
                    else:
                        owner.onid_email = ''

                owner.lists.add(old_list)
                owner.save()

                old_list.oldowner_set.add(owner)
                old_list.save()
        
        links = self.generate_link_codes()
        
        for owner_email in links:
            owner = OldOwner.objects.get(owner_email=owner_email)
            owner.link_code = links[owner.owner_email]
            owner.save()

        #now send out emails
        

        owner_entries = OldOwner.objects.all()
        for owner in owner_entries:

            if owner.onid_email != '':

                self.send_transition_email_onid(owner.onid_email)

                oe = OwnerEntry(name=owner.get_onid_username())
                oe.save()

                owner_lists = owner.lists.all()
                
                for old_list in owner_lists:
                    #see if the list already exists
                    try:
                        ls = ListEntry.objects.get(name=old_list.name)
                    except ListEntry.DoesNotExist:
                        #if not create it and add a relation to the owner
                        ls = ListEntry(name=old_list.name, 
                                       create_date=old_list.create_date, 
                                       expire_date=old_list.create_date + datetime.timedelta(365 * 2))
                        ls.save()

                    oe.lists.add(ls)
                    oe.save()
            else:
                self.send_transition_email(owner.owner_email)

        # old_lists = OldList.objects.all()
        # for ls in old_lists:

        #for every list that has an owner with an ONID account, send out an email to the owner saying that they have been migrated over
        #to the new system and now have control over list expiration (Should they be prompted to choose an expiration date for their lists?)

        #for every list with an owner without an ONID account, send them an email asking them to authenticate through ONID to regain admin access to their list

                
