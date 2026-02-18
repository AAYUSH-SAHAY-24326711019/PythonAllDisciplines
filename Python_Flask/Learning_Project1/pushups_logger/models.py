from datetime import datetime
from . import db
from flask_login import UserMixin

#----------------model : User start------------------
class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))
    name=db.Column(db.String(100))
    workouts = db.relationship('Workout',backref='author',lazy=True)

#----------------model : User end------------------

#----------------model : Workout start------------------
class Workout(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    pushups = db.Column(db.Integer,nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    comment=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)


#----------------model : Workout end------------------