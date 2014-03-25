from urlparse import urlparse
import os
from mongoengine import *
 
MONGO_URL = os.environ.get('MONGOHQ_URL')

def mongo_connect():
	if MONGO_URL:
	  # Get a connection
	  connect(MONGO_URL)
	  # Get the database
	  #db = connection[urlparse(MONGO_URL).path[1:]]
	else:
	  # Not on an app with the MongoHQ add-on, do some localhost action
	  connect('test_database')