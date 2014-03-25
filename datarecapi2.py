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

class Content(db.EmbeddedDocument):
    content = db.StringField()
    url = db.URLField()

class User(db.Document):
    name = db.StringField(unique=True, required=True)
    contents = db.ListField(db.EmbeddedDocumentField(Content))

class UserResource(Resource):
    document = User

@api.register(name='users', url='/users/')
class UserView(ResourceView):
    resource = UserResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]

if __name__ == "__main__":
    app.run(debug = True)