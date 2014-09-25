from django.test import TestCase
from datetime import *
from list_app.models import * 
from list_app.management.commands.check_lists import *

import subprocess

import pdb


class ListTestCase(TestCase):

    le1 = None
    le2 = None
    le3 = None

    def setUp(self):
        now = datetime.now()
        create = now + timedelta(-30)
        expired_date = now
        warning_date_1 = now + timedelta(29)
        warning_date_2 = now + timedelta(6)

        le1 = List.objects.create(name='PH_211', create_date=create, expire_date=expired_date)

        le2 = List.objects.create(name='PH_212', create_date=create, expire_date=warning_date_1)

        le3 = List.objects.create(name='ST_314', create_date=create, expire_date=warning_date_2)

        oe1 = Owner.objects.create(name='wasingej')
        oe1.lists.add(le1)
        oe1.lists.add(le2)
        oe1.lists.add(le3)
        
        oe2 = Owner.objects.create(name='doej')
        oe2.lists.add(le2)
        oe2.lists.add(le1)

    def test(self):
        expired_lists = check_lists()
        for listEntry in expired_lists:
            
            #(Owner.objects.get(lists__in=listEntry)).delete() 
            (ListWarning.objects.get(mailing_list=listEntry)).delete()
            
            #only delete owners if they no longer refer to lists other than this one
            owners = listEntry.owner_set.all()
            for owner in owners:
                if owner.lists.count() == 1:
                    owner.delete()

            listEntry.delete()

        warning_deleted = False
        list_deleted = False
        no_hanging_refs = False
        
        #ensure list records have been deleted for the expired list
        try:
            List.objects.get(name='PH_211')
        except List.DoesNotExist:
            list_deleted = True

        owners = Owner.objects.filter(lists__name='PH_211')
        if owners.count() == 0:
            no_hanging_refs = True

        try:
            ListWarning.objects.get(mailing_list__name='PH_211')
        except ListWarning.DoesNotExist:
            warning_deleted = True

        self.assertEqual(list_deleted and no_hanging_refs and warning_deleted, True)

        #ensure records of warnings have been filled out accordingly
        self.assertEqual(
            ListWarning.objects.get(mailing_list__name='ST_314', first_warning=True, last_warning=True) is None,
            False)
        self.assertEqual(
            ListWarning.objects.get(mailing_list__name='PH_212', first_warning=True, last_warning=False) is None,
            False)

        # warnings = ListWarning.objects.all()
        # for listWarning in warnings:
        #     print(listWarning.mailing_list.name)
        #     print("Has first warning {0}".format(listWarning.first_warning))
        #     print("Has second warning {0}".format(listWarning.last_warning))
        #
        # for listEntry in expired_lists:
        #     print("{0} has been deleted.".format(listEntry.name))
