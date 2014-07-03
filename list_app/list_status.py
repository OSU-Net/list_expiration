from list_app import models

class ListStatus:
	
	name = None
	owners = []

	def __init__(self, name, owners):
		self.name = name
		self.owners = owners

class OwnerStatus:
	
	email = None
	status = None

	def __init__(self, email, status):
		self.email = email
		self.status = status

def calc_owner_status(owner):
	if owner.bounced:
		return "bounced"

	if owner.onid_email == "":
		return "no_response"

	return "claimed"