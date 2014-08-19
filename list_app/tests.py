from django.test import TestCase
from datetime import *
from list_app.models import * 
import subprocess

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

        le1 = ListEntry(name='PH_211', create_date=create, expire_date=expired_date)
        le1.save()

        le2 = ListEntry(name='PH_212', create_date=create, expire_date=warning_date_1)
        le2.save()

        le3 = ListEntry(name='ST_314', create_date=create, expire_date=warning_date_2)
        le3.save()

        oe1 = OwnerEntry(name='wasingej', lists=[le1,le2, le3])
        oe1.save()

        oe2 = OwnerEntry(name='doej', lists=[le2])
        oe2.save()

    def test(self):
        expired_lists = check_lists()
        for listEntry in expired_lists:

            (OwnerEntry.objects.get(lists__in=listEntry)).delete() 
            (ListWarning.objects.get(mailing_list=listEntry)).delete()

            listEntry.delete()

        warning_deleted = False
        list_deleted = False
        owner_deleted = False

        #ensure list records have been deleted for the expired list
        try:
            ListEntry.objects.get(name='PH_211')
        except ListEntry.DoesNotExist:
            list_deleted = True

        try:
            OwnerEntry.objects.get(mailing_list__name='PH_211')
        except OwnerEntry.DoesNotExist:
            owner_deleted = True

        try:
            ListWarning.objects.get(mailing_list__name='PH_211')
        except ListWarning.DoesNotExist:
            warning_deleted = True

        self.assertEqual(list_deleted and owner_deleted and warning_deleted, True)

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
