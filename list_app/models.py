from django.db import models
import pdb

class List(models.Model):
    name = models.CharField(max_length=64)
    # active_date = models.DateTimeField('date of last list activity')
    expire_date = models.DateField('date of expiration')
    create_date = models.DateField('date created')


class ListWarning(models.Model):
    mailing_list = models.ForeignKey(List)
    first_warning = models.BooleanField()
    last_warning = models.BooleanField()

    class Meta:
        ordering = ('mailing_list__name', 'first_warning', 'last_warning')


class Owner(models.Model):
    name = models.CharField(max_length=32)
    lists = models.ManyToManyField(List)
    preferred_email = models.CharField(max_length=32, blank=True)

    class Meta:
        ordering = ('name',)

class PreferredEmail(models.Model):
    onid_email = models.CharField(max_length=32)
    pref_email = models.CharField(max_length=32)

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
    preferred_email = models.CharField(max_length=32, blank=True)
    lists = models.ManyToManyField(OldList, blank=True)
    
    #get the ONID username without '@onid.oregonstate.edu' appended 
    def get_onid_username(self):
        if not self.onid_email:
            raise Exception('The owner {0} does not have an ONID email'.format(self))

        strs = self.onid_email.split('@')
        return strs[0]

    class Meta:
        ordering = ('owner_email',)


