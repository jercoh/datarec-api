class User(Document):
    email = StringField(required=True)
    recommendations = List