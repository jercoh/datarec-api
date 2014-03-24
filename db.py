from urlparse import urlparse
from mongoengine import *
 
MONGO_URL = os.environ.get('MONGOHQ_URL')
connection = None

def get_connection():
	global connection
	if MONGO_URL:
	  # Get a connection
	  connection = connect(MONGO_URL)
	  # Get the database
	  #db = connection[urlparse(MONGO_URL).path[1:]]
	else:
	  # Not on an app with the MongoHQ add-on, do some localhost action
	  connect('test-database')
	return connection