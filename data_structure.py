from mongoengine import *

class Content(EmbeddedDocument):
    content = StringField()
    url = StringField()

class User(DynamicDocument):
    name = StringField(required=True)
    contents = ListField(EmbeddedDocumentField(Content))