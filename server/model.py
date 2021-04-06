from user import User
from db import init_db_command
from flask import Flask, jsonify, redirect, url_for, request, json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView

from sqlalchemy import *
from flask_ngrok import run_with_ngrok
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base

import sqlite3
import os
import requests
import random
import graphene
from graphene import Field,String,Int
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField


app = Flask(__name__)
    
# Configs
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

Base = declarative_base()

# Modules
db = SQLAlchemy(app)
# Naive database setup
try:
    init_db_command()
    db.create_all()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

class Room(db.Model):
    __tablename__ = 'room'
    roomid = db.Column(db.Integer, primary_key=True, unique=True)
    profid = db.Column(db.Integer, index=True, unique=True)

    questions = db.relationship('Question', backref='room') # backeref establishes a .room attribute on Question, which will refer to the parent Room object 
    
    def __repr__(self):
        return '< %r>' % self.profid

class Question(db.Model):
    __tablename__ = 'question'
    questionid = db.Column(db.Integer, primary_key=True, unique=True)
    question = db.Column(db.String(256), index=True)
    choices = db.Column(db.String(256), index=True)    
    roomid = db.Column(db.Integer, ForeignKey('room.roomid'))
    
    def __repr__(self):
        return '<Question %r>' % self.question

# Schema Objects 
''' 
show what kind of type of object will be shown in the graph. 
'''

# -------------------- GQL Schemas ------------------
class QuestionObject(SQLAlchemyObjectType):
    class Meta:
        model = Question
        interfaces = (graphene.relay.Node,)

class RoomObject(SQLAlchemyObjectType):
    class Meta:
        model = Room 
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_questions = SQLAlchemyConnectionField(QuestionObject)
    all_rooms = SQLAlchemyConnectionField(RoomObject)
    roomid = graphene.Field(RoomObject,rid=graphene.Int()) # find room by id
    def resolve_roomid(self, args,rid):
        room = Room.query.filter_by(roomid=rid).first()
        return room

# noinspection PyTypeChecker
schema_query = graphene.Schema(query=Query)


# Mutation Objects Schema
class CreateRoom(graphene.Mutation):
    class Arguments:
        roomid = graphene.Int(required=True)
        profid = graphene.Int(required=True) 

    room = graphene.Field(lambda: RoomObject)

    def mutate(self, info, roomid, profid):
        room = Room(roomid=roomid, profid=profid)
        db.session.add(room)
        db.session.commit()
        return CreateRoom(room=room)

class CreateQuestion(graphene.Mutation):
    class Arguments:
        questionid = graphene.Int(required=True)
        question = graphene.String(required=True)
        choices = graphene.String(required=True)
        roomid = graphene.Int(required=True)
    
    question = graphene.Field(lambda: QuestionObject)

    def mutate(self, info, questionid, question, choices, roomid):
        room = Room.query.filter_by(roomid=roomid).first() #lookup which room 
        question = Question(questionid=questionid, question=question, choices=choices, roomid=roomid)
        if room is not None:
            question.room = room
        db.session.add(question)
        db.session.commit()
        return CreateQuestion(question=question)

class Mutation(graphene.ObjectType):
    create_room = CreateRoom.Field()
    create_question = CreateQuestion.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# Routes 
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)
# /endpoint for query
app.add_url_rule('/graphql-query', view_func=GraphQLView.as_view(
    'graphql-query',
    schema=schema_query, graphiql=True
))

# /endpoint for mutation
app.add_url_rule('/graphql-mutation', view_func=GraphQLView.as_view(
    'graphql-mutation',
    schema=schema, graphiql=True
))

if __name__ == '__main__':
    app.run(port=5003)