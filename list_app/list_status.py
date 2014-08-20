from list_app import models
import pdb

class ListStatus:
    
    name = None
    owners = []

    def __init__(self, name, owners):
        self.name = name
        self.owners = owners

class OwnerStatus:
    
    email = None
    status = None
    is_onid = False

    def __init__(self, email, status):
        self.email = email
        self.status = status
        self.is_onid = is_owner_onid(email)

#three onid endings
#onid.orst.edu
#oregonstate.edu
#onid.oregonstate.edu
#TODO: handle tooltips and account for more types of onid addresses
def is_owner_onid(email):
    strs = email.split('@')
    if strs[1] == 'onid.orst.edu' or strs[1] == 'oregonstate.edu' or strs[1] == 'onid.oregonstate.edu':
        return True

    return False

def calc_owner_status(owner):
    if owner.bounced:
        return "bounced"

    if owner.onid_email == "":
        return "no_response"

    return "claimed"