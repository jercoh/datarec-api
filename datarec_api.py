#!flask/bin/python

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension."""

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest.resources import Resource
from flask.ext.mongorest import operators as ops
from flask.ext.mongorest import methods  
import os
import datarec_dbconfig
from bson.json_util import dumps
import pymongo

app = Flask(__name__, static_url_path = "")
MONGO_URL = os.environ.get('MONGOHQ_URL')
if MONGO_URL:
    app.config.update(
        MONGO_URL = MONGO_URL
    )
else:
    app.config['MONGODB_SETTINGS'] = {'DB': 'test_database'}

db = MongoEngine(app)
api = MongoRest(app)

db_name = datarec_dbconfig.getName()
db_pymongo = pymongo.MongoClient()[db_name]

base_url = '/api/v1.0'

class Content(db.EmbeddedDocument):
    content = db.StringField()
    url = db.URLField()

class ContentResource(Resource):
    document = Content

class User(db.Document):
    name = db.StringField(unique=True, required=True)
    contents = db.ListField(db.EmbeddedDocumentField(Content))

class UserResource(Resource):
    document = User
    filters = {
        'name': [ops.Exact, ops.Startswith]
    }
    related_resources = {
        'contents' : ContentResource
    }

@api.register(name='users', url= base_url+'/users/')
class UserView(ResourceView):
    resource = UserResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]

@app.route(base_url+'/<client_name>/recommendations/', methods = ['GET'])
def get_recommendations(client_name):
    collection_names = db_pymongo.collection_names()
    if client_name in collection_names:
        clientCollection = db_pymongo[client_name]
        recommendations = dumps(list(clientCollection.find({}, {'_id': 0})))
        return recommendations
    else:
        abort(400)

@app.route(base_url+'/<client_name>/recommendations/<content_type>/', methods = ['GET'])
def get_specific_recommendations(client_name, content_type):
    collection_names = db_pymongo.collection_names()
    if client_name in collection_names:
        clientCollection = db_pymongo[client_name]
        recommendations = dumps(list(clientCollection.find({ }, {'user_id':1, 'email':1, content_type+"_recommendation": 1, '_id': 0})))
        return recommendations
    else:
        abort(400)

@app.route(base_url+'/<client_name>/recommendations/users/<int:user_id>/', methods = ['GET'])
def get_recommendations_for_user(client_name, user_id):
    collection_names = db_pymongo.collection_names()
    if client_name in collection_names:
        clientCollection = db_pymongo[client_name]
        recommendations = dumps(list(clientCollection.find({'user_id': user_id }, {'_id': 0})))
        return recommendations
    else:
        abort(400)

@app.route(base_url+'/<client_name>/recommendations/users/<int:user_id>/<content_type>/', methods = ['GET'])
def get_specific_recommendations_for_user(client_name, user_id, content_type):
    collection_names = db_pymongo.collection_names()
    if client_name in collection_names:
        clientCollection = db_pymongo[client_name]
        recommendations = dumps(list(clientCollection.find({'user_id': user_id }, {'user_id':1, 'email':1, content_type+"_recommendation": 1,'_id': 0})))
        return recommendations
    else:
        abort(400)



if __name__ == "__main__":
    app.run(debug = True)