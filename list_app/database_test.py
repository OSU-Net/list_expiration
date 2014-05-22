from datetime import *
from list_app.models import * 

now = datetime.now()
create = now + timedelta(-30)
expired_date = now
warning_date_1 = now + timedelta(29)
warning_date_2 = now + timedelta(6)

le1 = ListEntry(name='ph_211', create_date=create, expire_date=expired_date)
le1.save()

le2 = ListEntry(name='ph_212', create_date=create, expire_date=warning_date_1)
le2.save()

le3 = ListEntry(name='ph_314', create_date=create, expire_date=warning_date_2)
le3.save()

oe1 = OwnerEntry(name='wasingej', mailing_list=le1)
oe1.save()

oe2 = OwnerEntry(name='wasingej', mailing_list=le2)
oe2.save()

oe3 = OwnerEntry(name='doej', mailing_list=le2)
oe3.save()

exit()