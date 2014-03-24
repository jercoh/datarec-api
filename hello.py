import os
from flask import Flask
import db as db

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

def mongo():
	mongo = db.get_connection()
	return mongo