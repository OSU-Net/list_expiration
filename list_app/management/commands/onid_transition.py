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
import random

class Command(BaseCommand):
	help = """ This command is used to begin the transition process which will migrate list owners
	over to ONID.  Only list owners that possess ONID accounts will be able to manage the
	expiration of the list(s) that they manage.
	"""
	def send_transition_email_onid(onid_email):
		print('transition email sent to {0}'.format(onid_email))


	def send_transition_email(email_addr):
		print('Transition email sent with link ...')

	def get_mailman_list_names():

		list_dirs = [x[0] for x in os.walk(settings.MAILMAN_FILES_DIR + '/lists/')]
		list_names = []

		for list_dir in list_dirs:
			strs = list_dir.split('/')
			if strs[len(strs)-1] == '':
				continue
			else:
				list_names.append(strs[len(strs)-1])

		print list_names

		return list_names

	def owner_is_onid(owner_email):

		strs = owner_email.split('@')
		if strs[len(strs) - 1] == 'onid.oregonstate.edu' or strs[len(strs) - 1] == 'onid.orst.edu':
			return True

		return False
	
	def generate_links():
		unique_owners = OwnerTransition.objects.order_by('owner_email').values('owner_email').distinct()
		links = {}

		for owner_email in unique_owners:
			
			while True:
				link_val = random.getrandbits(128)
				if link_val in links.values():
					continue
				else:
					links[owner_email] = link_val
					break

		return links

	def handle(self, *args, **options):
		#foreach list:
		#    unpickle the pck file

		#list_dirs = [x[0] for x in os.walk(settings.MAILMAN_FILES_DIR + '/lists')] #trailing slash needed here?
		list_names = get_mailman_list_names()

		for list_name in list_names:
			pck_dict = None
			
			try:
				pck_file = open(settings.MAILMAN_FILES_DIR + '/lists/' + list_name + '/config.pck','r')
				pck_dict = pickle.load(pck_file)

			except IOError as e:
				print("I/O error({0}): {1}".format(e.errno, e.strerror))
				print("List {0} files corrupted or missing".format(list_name))
				break
			except pickle.PickleError as e:
				print("Pickle error{0}: {1}".format(e.errno, e.strerror))

			for owner_email in pck_dict['owner']:
				transition_entry = OwnerTransition()
				transition_entry.owner_email = owner_email
				transition_entry.list_name = pck_dict['real_name']
				transition_entry.bounced = False

				if owner_is_onid(pck_dict):
					transition_entry.onid_email = transition_entry.owner_email
				else:
					transition_entry.onid_email = ''

				transition_entry.save()

		links = generate_links()
		for owner in links:
			transition_entry = OwnerTransition.objects.filter(owner_email=owner)
			transition_entry.link_code = links[owner]
			transition_entry.save()
			
		#now send out emails
		transition_entries = TransitionEntry.objects.all()
		
		for transition_entry in transition_entries:
			if transition_entry.onid_email != '':
				send_transition_email_onid(transition_entry.onid_email)
			else:
				send_transition_email(transition_entry.owner_email)


		#for every list that has an owner with an ONID account, send out an email to the owner saying that they have been migrated over
		#to the new system and now have control over list expiration (Should they be prompted to choose an expiration date for their lists?)

		#for every list with an owner without an ONID account, send them an email asking them to authenticate through ONID to regain admin access to their list

		