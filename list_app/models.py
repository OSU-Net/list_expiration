from django.db import models
import pdb

class ListEntry(models.Model):
    name = models.CharField(max_length=64)
    # active_date = models.DateTimeField('date of last list activity')
    expire_date = models.DateField('date of expiration')
    create_date = models.DateField('date created')


class ListWarning(models.Model):
    mailing_list = models.ForeignKey(ListEntry)
    first_warning = models.BooleanField()
    last_warning = models.BooleanField()

    class Meta:
        ordering = ('mailing_list__name', 'first_warning', 'last_warning')


class OwnerEntry(models.Model):
    name = models.CharField(max_length=32)
    lists = models.ManyToManyField(ListEntry)

    class Meta:
        ordering = ('name',)

#
#these models are used for the transition to ONID:
#

class OldList(models.Model):
    name = models.CharField(max_length=32, blank=False)
    create_date = models.DateField(blank=False)

    class Meta:
        ordering = ('name',)

class OldOwner(models.Model):
    owner_email = models.CharField(max_length=32, blank=False, )
    onid_email = models.CharField(max_length=32, blank=True)
    link_code = models.CharField(max_length=32, blank=True)
    bounced = models.NullBooleanField(blank=True,null=True)
    lists = models.ManyToManyField(OldList, blank=True)

    #get the ONID username without '@onid.oregonstate.edu' appended 
    def get_onid_username(self):
        if not self.onid_email:
            raise Exception('The owner {0} does not have an ONID email'.format(self))

        strs = self.onid_email.split('@')
        return strs[0]

    class Meta:
        ordering = ('owner_email',)
