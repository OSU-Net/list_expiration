from datetime import *
from list_app.models import *

now = datetime.now()
exp_date = datetime(now.year, now.month + 1, now.day)

le1 = ListEntry(name='physics 211 mailing list', create_date=datetime.now(), expire_date=exp_date)
le1.save()
le2 = ListEntry(name='physics 212 mailing list', create_date=datetime.now(), expire_date=exp_date)
le2.save()
oe1 = OwnerEntry(name='wasingej', list=le1)
oe1.save()
oe2 = OwnerEntry(name='wasingej', list=le2)
oe2.save()
oe3 = OwnerEntry(name='doej', list=le2)
oe3.save()
