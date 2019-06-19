import os
from app import app
from flask import render_template, request, redirect, session, url_for
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from passlib.hash import sha256_crypt

## secret key for sessions
app.secret_key = b'HO\xf8\xff+\n\x1e\\~/;}'


# # name of database
app.config['MONGO_DBNAME'] = 'database' 

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
    
##User Signup

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name':request.form['username']})
        
        if existing_user is None:
            users.insert(   {'name':request.form['username'],
                            'password':sha256_crypt.encrypt(request.form['password'])
            })
            session['username'] = request.form['username']
            
            return redirect(url_for('index'))
        
        return 'That username already exists. Try logging in'
        
    return render_template('register.html')

## Log In
@app.route('/login',methods=['POST'])

def login():
    users = mongo.db.users
    login_user = users.find_one({'name':request.form['username']})
    
    if login_user:
        if sha256_crypt.verify(request.form['password'], login_user['password']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    
    return 'Invalid username/password combination'

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/') 

## Record New Message

@app.route('/newmessage',methods=['POST'])
def new_message():
    if request.method == 'POST':
        print(request.form)
        if session['username']:
            messages = mongo.db.messages
            messages.insert({   'sender':session['username'],
                                'recipient':request.form.get('recipient'),
                                'message':request.form.get('message')
                                })
        return redirect(url_for('yourmessages'))
    else:
      return redirect('/')

@app.route('/yourmessages', methods=['GET'])
def yourmessages():
    if session['username']:
        messages = mongo.db.messages
        inbox = messages.find({'recipient':session['username']}) 
        outbox = messages.find({'sender':session['username']})
        
        users = mongo.db.users
        users = users.find({})

        return render_template('yourmessages.html', inbox=inbox, outbox=outbox, users=users)