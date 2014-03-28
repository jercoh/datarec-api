#!flask/bin/python

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension."""

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest.resources import Resource
from flask.ext.mongorest import operators as ops
from flask.ext.mongorest import methods  
from flask.ext.mongorest.authentication import AuthenticationBase
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
import os
import datarec_dbconfig
from bson.json_util import dumps
import pymongo
from mongoengine import connect

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

app.config.from_object('app_config.DevelopmentConfig')

db = MongoEngine(app)
api = MongoRest(app)

db_pymongo = db.connection

base_url = '/api/v1.0'

@auth.verify_password
def authorized(username, token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False # valid token, but expired
    except BadSignature:
        return False # invalid token
    return True

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

class Content(db.EmbeddedDocument):
    content = db.StringField()
    url = db.URLField()

class ContentResource(Resource):
    document = Content

class Client(db.Document):
    name = db.StringField(unique=True, required=True)
    contents = db.ListField(db.EmbeddedDocumentField(Content))

class ClientResource(Resource):
    document = Client
    filters = {
        'name': [ops.Exact, ops.Startswith]
    }
    related_resources = {
        'contents' : ContentResource
    }


@api.register(name='clients', url= base_url+'/clients/')
class ClientView(ResourceView):
    resource = ClientResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]

@app.route(base_url+'/<client_name>/recommendations/', methods = ['GET'])
@auth.login_required
def get_recommendations(client_name):
    collection_names = db_pymongo.collection_names()
    if client_name in collection_names:
        clientCollection = db_pymongo[client_name]
        recommendations = dumps(list(clientCollection.find({}, {'_id': 0})))
        if recommendations == '[]':
            raise InvalidUsage('You have not generated any recommendation yet.', status_code=404)
        else:
            return recommendations
    else:
        raise InvalidUsage('This client does not exist. Enter a valid client name', status_code=404)

@app.route(base_url+'/<client_name>/recommendations/<content_type>/', methods = ['GET'])
@auth.login_required
def get_specific_recommendations(client_name, content_type):
    collection_names = db_pymongo.collection_names()
    if client_name in collection_names:
        clientCollection = db_pymongo[client_name]
        recommendations = dumps(list(clientCollection.find({ content_type+"_recommendation": {'$exists': 'true'}}, {'user_id':1, 'email':1, content_type+"_recommendation": 1, '_id': 0})))
        if recommendations == '[]':
            raise InvalidUsage('No '+content_type+' recommendations have been generated yet.', status_code=404)
        else:
            return recommendations
    else:
        raise InvalidUsage('This client does not exist. Enter a valid client name', status_code=404)

@app.route(base_url+'/<client_name>/recommendations/users/<int:user_id>/', methods = ['GET'])
@auth.login_required
def get_recommendations_for_user(client_name, user_id):
    collection_names = db_pymongo.collection_names()
    if client_name in collection_names:
        clientCollection = db_pymongo[client_name]
        recommendations = dumps(list(clientCollection.find({'user_id': user_id }, {'_id': 0})))
        if recommendations == '[]':
            raise InvalidUsage('No recommendation have been generated for user '+str(user_id)+' yet.', status_code=404)
        else:
            return recommendations
    else:
        raise InvalidUsage('This client does not exist. Enter a valid client name', status_code=404)

@app.route(base_url+'/<client_name>/recommendations/users/<int:user_id>/<content_type>/', methods = ['GET'])
@auth.login_required
def get_specific_recommendations_for_user(client_name, user_id, content_type):
    collection_names = db_pymongo.collection_names()
    if client_name in collection_names:
        clientCollection = db_pymongo[client_name]
        recommendations = dumps(list(clientCollection.find({'user_id': user_id, content_type+"_recommendation": {'$exists': 'true'}}, {'user_id':1, 'email':1, content_type+"_recommendation": 1,'_id': 0})))
        if recommendations == '[]':
            raise InvalidUsage('No '+content_type+' recommendation have been generated for user '+str(user_id)+' yet.', status_code=404)
        else:
            return recommendations
    else:
        raise InvalidUsage('This client does not exist. Enter a valid client name', status_code=404)



if __name__ == "__main__":
    app.run(debug = True)