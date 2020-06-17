from pymongo import MongoClient
from flask import jsonify,abort,make_response,render_template,url_for,flash,g, redirect,session,request,make_response
from app import app
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from datetime import datetime
# from views import collection
from flask_paginate import Pagination,get_page_parameter
bcrypt = Bcrypt(app)




client = MongoClient()
db = client.Matcha
users = db.users
post = db.post

def notification_update(username,notification):
    user = db.users.update_one({"username":username},{'$set': {"notification":notification}})
    return user

def find_email(form):
    user = db.users.find_one({"email":form.email.data})
    return user

def find_user(post_id):
    user = db.users.find_one({"username":post_id})
    return user

def find_username(form):
    name = db.users.find_one({"username":form.username.data})
    return name
def age_update(form,id):
    db.users.update_one({"_id":ObjectId(id)},{'$set': {"age" : form.age.data }})


def interest_update(form,id):
    db.users.update_one({"_id":ObjectId(id)},{'$push': {"Interest" : form.interest.data }})

def insert_notification(id,notification_numb):
    db.users.update_one({'_id':ObjectId(id)},{'$set':{"notification_numb":notification_numb}})

def existing_user(id):
    user = db.users.find_one({"_id":ObjectId(id)})
    return user

def users_pagination():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(),type=int,default=1)

    users =  all_existing_users()
    pagination = Pagination(page=page,page_parameter=2, total=users.count(), search=search, record_name='users')


    return pagination

# def existing_blog_post(id):
#     user = db.users.find_one({"author":ObjectId(id)})
#     return user

def upload_profile_pic(user,filename):
    db.users.update_one({'username':user},{'$set':{'profile_pic':filename}})

def bio_update(form,id):
    db.users.update_one({"_id":ObjectId(id)},{'$set': {"bio" : form.bio.data }})

def gender_update(form,id):
    db.users.update_one({"_id":ObjectId(id)},{'$set': {"gender" : form.gender.data }})

def sexualPreference_update(form,id):
    db.users.update_one({"_id":ObjectId(id)},{'$set': {"sexualPreference" : form.sexualPreference.data }})

def registered_update(id):
    db.users.update_one({"_id":ObjectId(id)},{'$set': {"registered" : True }})

def coordinates_update(existing_user,req):
    db.users.update_one({"username":existing_user['username']},{'$set': {"coordinates" :req }})
    
def username_update(form,existing_user):
    db.users.update_one({"username":existing_user['username'] },{'$set': {"username": form.username.data }})

def firstname_update(form,existing_user):
    db.users.update_one({"firstname":existing_user['firstname'] },{'$set': {"firstname": form.firstname.data }})

def lastname(form,existing_user):
    db.users.update_one({"lastname":existing_user['lastname'] },{'$set': {"lastname": form.lastname.data }})

def email_update(form,existing_user):
    db.users.update_one({"username":existing_user['username'] },{'$set': {"email": form.email.data }})



def find_id(id):
    user =db.users.find_one({"_id":ObjectId(id)})
    return user

def find_id_for_session(user):
    user =db.users.find_one({"_id":ObjectId(user)})
    return user

def find_blog_post(id):
    user =db.post.find_one({"author":ObjectId(id)})
    return user

def push_pictures_blog_post(id,pictures_fn):
    user =db.post.update_one({"author":ObjectId(id)},{'$push':{'pictures':pictures_fn}})
    return user

# @socketio.on('my event')
def push_user_messages(id,messages):
    user =db.users.update_one({"_id":ObjectId(id)},{'$push':{'messages':messages}})


def push_owner_messages(username,messages):
    user =db.users.update_one({"username":username},{'$push':{'messages':messages}})


def push_user_likes(username,data):
    db.users.update_one({"username":username},{'$push':{'likes':data}})

def push_user_liked_you(post_id,data):
    db.users.update_one({"username":post_id},{'$push':{'liked':data}})

def push_user_open_your_profile(post_id,data):
    db.users.update_one({"username":post_id},{'$push':{'profile_open':data}})
    

def push_number_of_messages(id,prev_number):
    user =db.users.update_one({"_id":ObjectId(id)},{'$set':{'prev_number':prev_number}})

def create_users(form):
    
    if find_username(form) is not None:
        flash('Sorry the username already exist, please try another one','danger')
        return redirect(request.url)
    else:
        username =form.username.data 
    
    if find_email(form) is not None:
            
        flash('Sorry the email already exist, please try another one','danger')
        return redirect(request.url)
    else:
        email = form.email.data 
    firstname = form.firstname.data
    lastname = form.lastname.data
    password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

    user_id =users.insert({
        "profile_pic":'user.png',
        "username":username,
        "firstname":firstname,
        "lastname":lastname,
        "email":email,
        "password":password,
        "age":"",
        "bio":"",
        "categories":"",
        "registered":False,
        # "date_create":datetime.utcnow,
        "gender":"",
        "sexualPreference":"",
        "AccountVerification":0,
        "coordinates":[],
        'pictures':[],
        "messages":[],
        "likes":[],
        "liked":[],
        "profile_open":[],
        "Interest":[],
        "notification":0,
        "notification_numb":0
    })
    return user_id

def create_post(form):
    exist = find_email(form)
    posts = post.insert({
        "author":exist['_id'],
        "pictures":[]
    })
    return posts

#for all post collection

def all_existing_post():
    posts = db.post.find({})
    return posts

def delete_existing_post(id,picture):
    # db.post.delete_one({"author":ObjectId(id)})
    db.post.update({'author':ObjectId(id)},{'$pull':{'pictures':picture }})


def all_existing_users():
    users = db.users.find({})
    return users

def find_post(post_id):
    users = db.post.find_one({'pictures':post_id})
    return users