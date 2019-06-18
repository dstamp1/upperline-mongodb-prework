import os
from app import app
from flask import render_template, request, redirect, session, url_for
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

## secret key for sessions
app.secret_key = b'HO\xf8\xff+\n\x1e\\~/;}'


# # name of database
app.config['MONGO_DBNAME'] = 'upperline-prework' 

# # URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:l2UwFnHShONYpVLE@cluster0-qjkuk.mongodb.net/database?retryWrites=true&w=majority' 

mongo = PyMongo(app)


# INDEX

@app.route('/')
@app.route('/index')

def index():
    ## connect to DB
    collection = mongo.db.users
    ## find all data use empty brakets
    ## sort function can take list of properties to sort by (1 is descending and -1 is ascending)
    users = collection.find({})
    ## return
    return render_template('index.html', users = users)