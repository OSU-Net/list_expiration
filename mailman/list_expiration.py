import pickle
import datetime 
import MySQLdb as mdb
import sys

FIRST_WARNING_TIME = 30
SECOND_WARNING_TIME = 7
MAILMAN_LISTS_DIRECTORY = "/var/lib/mailman/lists/"

connection = None

def has_first_warning(list_name):
	cursor = connection.cursor()

	cursor.execute(""" SELECT FROM list_warnings
					   WHERE name=""".concat(list_name))

	list_warning = cursor.fetchone()
	if list_warning.first_warning:
		return True
	else:
		return False

def time_delta_days(earlier_date, later_date):
	return (later_date - earlier_date).total_days()

#check to see if the lists in list_entries have reached 'warning_time'.  If they have, notify the list admin via email
def warn_first(list_entries):
	now = datetime.now()

	for list in list_entries:
		if now - list.expire_date <= FIRST_WARNING_TIME:
			if not has_first_warning(list.name):

				#send warning email

#open the database, select all lists expiring within 'x' time
#send email warnings to the administrators of these lists, and mark the lists as being 'warned'
#go through all warned lists that have expired and remove their records (from the database and .pck)
try:
    connection = mdb.connect('db.nws.oregonstate.edu', 'wasingej', '12Tyugjk', 'maillist')

    #perform checks for the first warning before expiration
	cursor = connection.cursor()
	cursor.execute(""" SELECT * FROM lists_test
					   WHERE DATEDIFF(expire_date, CURDATE()) <= """.concat(FIRST_WARNING_TIME))


    entry = cursor.fetchone()
	while entry is not None:
		print(entry)
		entry = cursor.fetchone()

    #perform checks for the second warning before expiration
	cursor.execute(""" SELECT * FROM lists_test
					   WHERE DATEDIFF(expire_date, CURDATE()) <= """.concat(SECOND_WARNING_TIME))

	entry = cursor.fetchone()
	#while entry is not None:

	# cursor = connection.cursor()
	# cursor.execute("SELECT VERSION()")

	# version = cursor.fetchone()
	# print("Database version is: {0}".format(version));

except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

connection.close()

# f = open("config.pck", "rb")
# pck = pickle.load(f)

# for key in pck:
# 	print key, ':', pck[key], '\n'
