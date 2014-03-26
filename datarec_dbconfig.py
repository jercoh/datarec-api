from urlparse import urlparse
import os
from mongoengine import *
 
MONGO_URL = os.environ.get('MONGOHQ_URL')

def getName():
	if MONGO_URL:
	  # Get a connection
	  return MONGO_URL
	  # Get the database
	  #db = connection[urlparse(MONGO_URL).path[1:]]
	else:
	  # Not on an app with the MongoHQ add-on, do some localhost action
	  return 'test_database'