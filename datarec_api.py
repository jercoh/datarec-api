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
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
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

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })
        
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.objects(id = data['id'])
        return user

class UserResource(Resource):
    document = User
    filters = {
        'name': [ops.Exact, ops.Startswith]
    }
    related_resources = {
        'contents' : ContentResource
    }

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


@app.route(base_url+'/token')
def get_auth_token():
    token = User.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@auth.verify_password
def verify_password(token):
    # first try to authenticate by token
    user = User.verify_auth_token(token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

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
        raise InvalidUsage('This client does not exist. Enter a valid client name', status_code=404)

@app.route(base_url+'/<client_name>/recommendations/<content_type>/', methods = ['GET'])
def get_specific_recommendations(client_name, content_type):
    collection_names = db_pymongo.collection_names()
    if client_name in collection_names:
        clientCollection = db_pymongo[client_name]
        recommendations = dumps(list(clientCollection.find({ }, {'user_id':1, 'email':1, content_type+"_recommendation": 1, '_id': 0})))
        return recommendations
    else:
        raise InvalidUsage('This client does not exist. Enter a valid client name', status_code=404)

@app.route(base_url+'/<client_name>/recommendations/users/<int:user_id>/', methods = ['GET'])
def get_recommendations_for_user(client_name, user_id):
    collection_names = db_pymongo.collection_names()
    if client_name in collection_names:
        clientCollection = db_pymongo[client_name]
        recommendations = dumps(list(clientCollection.find({'user_id': user_id }, {'_id': 0})))
        return recommendations
    else:
        raise InvalidUsage('This client does not exist. Enter a valid client name', status_code=404)

@app.route(base_url+'/<client_name>/recommendations/users/<int:user_id>/<content_type>/', methods = ['GET'])
def get_specific_recommendations_for_user(client_name, user_id, content_type):
    collection_names = db_pymongo.collection_names()
    if client_name in collection_names:
        clientCollection = db_pymongo[client_name]
        recommendations = dumps(list(clientCollection.find({'user_id': user_id }, {'user_id':1, 'email':1, content_type+"_recommendation": 1,'_id': 0})))
        return recommendations
    else:
        raise InvalidUsage('This client does not exist. Enter a valid client name', status_code=404)



if __name__ == "__main__":
    app.run(debug = True)