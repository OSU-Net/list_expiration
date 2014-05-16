from django.test import TestCase
from datetime import *
from timedelta import * 
from list_app.models import * 
from list_app.management.commands import check_lists

class ListTestCase(TestCase):
	
	le1 = None
	le2 = None
	le3 = None

	def setUp(self):
		now = datetime.now()
		create = now + timedelta(-30)
		expired_date = now
		warning_date_1 = now + timedelta(30) 
		warning_date_2 = now + timedelta(7)

		le1 = ListEntry(name='PH_211', create_date=create, expire_date=exp_date_1)
		le1.save()
		
		le2 = ListEntry(name='PH_212', create_date=create, expire_date=warning_date_1)
		le2.save()

		le3 = ListEntry(name = 'ST_314', create_date=create, expire_date=warning_date_2)
		le3.save()
		
		oe1 = OwnerEntry(name='wasingej', mailing_list=le1)
		oe1.save()
		
		oe2 = OwnerEntry(name='wasingej', mailing_list=le2)
		oe2.save()
		
		oe3 = OwnerEntry(name='doej', mailing_list=le2)
		oe3.save()

		oe4 = OwnerEntry(name='wasingej', mailing_list=le3)
		oe4.save()

	def test(self):
		expired_lists = check_lists()
		self.assertEqual(ListWarning.objects.filter(mailing_list=le1))
