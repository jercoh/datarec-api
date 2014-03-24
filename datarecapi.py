#!flask/bin/python

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension."""

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.views import MethodView
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
import datarec
import db
import data_structure as struct
from data_structure import *
 
app = Flask(__name__, static_url_path = "")
api = Api(app)
auth = HTTPBasicAuth()
db.mongo_connect()
 
@auth.get_password
def get_password(username):
    if username == 'jercoh':
        return 'jercoh'
    return None
 
@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'message': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
 
user_fields = {
    'name': fields.String,
    'content': fields.List,
    'content_url': fields.List
}

content_fields = {
    'content': fields.String,
    'url': fields.String
}

class ClientsAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, required = True, help = 'No client name provided', location = 'json')
        self.reqparse.add_argument('contents', default = [], location = 'json')
        super(ClientsAPI, self).__init__()
        
    def get(self):
        return struct.User.objects.all().to_json()

    def post(self):
        args = self.reqparse.parse_args()
        user = struct.User(name = args['name'])
        contents = []
        for obj in marshal(args['contents'], content_fields):
            content = struct.Content(content = obj['content'], url = obj['url'])
            contents.push(content)
        user.contents = contents
        user.save()
        return { 'user': user.to_json() }, 201

class ClientAPI(Resource):
    decorators = [auth.login_required]
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('done', type = bool, location = 'json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        task = filter(lambda t: t['id'] == id, tasks)
        if len(task) == 0:
            abort(404)
        return { 'task': marshal(task[0], task_fields) }
        
    def put(self, id):
        task = filter(lambda t: t['id'] == id, tasks)
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v != None:
                task[k] = v
        return { 'task': marshal(task, task_fields) }

    def delete(self, id):
        task = filter(lambda t: t['id'] == id, tasks)
        if len(task) == 0:
            abort(404)
        tasks.remove(task[0])
        return { 'result': True }

api.add_resource(ClientsAPI, '/todo/api/v1.0/users', endpoint = 'users')
api.add_resource(ClientAPI, '/todo/api/v1.0/users/<int:id>', endpoint = 'user')
    
if __name__ == '__main__':
    app.run(debug = True)