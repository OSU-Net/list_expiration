import pickle
import MySQLdb as mdb
import sys

MAILMAN_LISTS_DIRECTORY = "/var/lib/mailman/lists/"
connection = None

try:
	connection = mdb.connect('db.nws.oregonstate.edu', 'wasingej', '12Tyugjk', 'maillist')
	# db = mdb.select_db('lists_test')

	cursor = connection.cursor()
	cursor.execute("""SELECT * FROM lists_test
					  WHERE admin='wasingej' """)
	entry = cursor.fetchone()
	while entry is not None:
		print(entry)
		entry = cursor.fetchone()

	# cursor = connection.cursor()
	# cursor.execute("SELECT VERSION()")

	# version = cursor.fetchone()
	# print("Database version is: {0}".format(version));

except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

# f = open("config.pck", "rb")
# pck = pickle.load(f)

# for key in pck:
# 	print key, ':', pck[key], '\n'
