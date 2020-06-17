from flask import jsonify,abort,make_response,render_template,url_for,flash,g, redirect,session,request,make_response
from app import app
# from flask_bcrypt import Bcrypt
import pyproj
import csv
from geopy import distance
from PIL import Image
from operator import itemgetter
import datetime

from flask_login import LoginManager
from app.forms import RegistrationForm,PostForm, LoginForm, UpdateAccountForm, UploadsForm, MessageForm
from app.database import *
import secrets
import os
import json
import bson
import random
from bson import json_util,ObjectId
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO,send,emit,join_room, leave_room
import time
from time import localtime,strftime
# from flask_socketio import SocketIO


geod = pyproj.Geod(ellps='WGS84')

#Initialize the Flask-SocketIO
socketio = SocketIO(app)

ROOMS = ["lounge","news","games","coding"]

# print("What is happning")





# @app.template_filter("clean_date")
# def clean_date(dt):
#     return dt.strftime("%d %b %Y")


# app.config['IMAGE_UPLOADS'] = '~/Documents/app/app/static/img'
# @app.route('/admin')
# def admin():

    #accessing the blogpost
    # users = User.objects(username='lunga').get()
    # posts = BlogPost.objects(author=users)


    # for post in posts:
    #     print(post.author.username,post.author.bio)
    # print('Done')

    #Query operators

    #less than & greater than

    # young_users = User.objects(age__lt=33)
    # for user in young_users:
    #     print(user.username,user.age)


    # older_users = User.objects(age__gte=30)
    # for user in older_users:
    #     print(user.username,user.age)

    #Query a list
    #we enter the name of the list that we're quering and then
    # we throw in the string that we're quering for if you 
    #are quering for a single value
    # post_tagged_python = BlogPost.objects(tags='MongoDB')

    # for post in post_tagged_python:
    #     print(post.title)

    #if you got multiple values that you want to query for
    # post_tagged_python = BlogPost.objects(tags__in=['MongoDB'])

    # for post in post_tagged_python:
    #     print(post.content)


    #String queries/case insensitive string(find a match)
    #we first provide the field we want to search,double underscore
    #because we're using query operator
    # python_posts = BlogPost.objects(content__icontains='python')

    # for post in python_posts:
    #     print(post.content)

    # python_posts = BlogPost.objects(title__icontains='my')

    # for post in python_posts:
    #     print(post.title)

    #contain is case sensitive
    # python_posts = BlogPost.objects(title__contains='first')

    # for post in python_posts:
    #     print(post.title)

    #Limiting and Skipping results
    # Get the first 

    #The first method is going to return the first document in the 
    #collection
    # first = BlogPost.objects.first()
    # print(first.title)

    #Get the first 2 documents/here we're going to use the python
    #slicing method

    # first_two = BlogPost.objects()[:2]

    # for post in first_two:
    #     print(post.title)

    #Get all but the first 2
    # all_but = BlogPost.objects()[2:]

    # for post in all_but:
    #     print(post.title)

    #sliced is very useful for pagination
    # sliced = BlogPost.objects()[2:4]

    # for post in sliced:
    #     print(post.title)

    #Counting

    # user_count = User.objects().count()
    # print(user_count)

    #Aggregation

    # average = BlogPost.objects.average('rating')
    # print(average)

    # total_rating = BlogPost.objects.sum('rating')
    # print(total_rating)

    # zakhele = User.objects(username='zakhele').get()
    # print(zakhele.json())




    # return render_template('admin/dash_board.html')



@socketio.on('join')
def join(data):

    print(data)
    # check = request.sid
    # print(check)
    # print(data)
    if data != {'user_name': {}, 'room': {}}:
        join_room(data['room'])
    # print(data['room'])
    #When joining the room we receve this message automatically
    if data != {'user_name': {}, 'room': {}}:
        emit('my event',{'user_name':'chatbot','message':data['user_name'] + ' has joined the '+data['room'] + ' room.'},room=data['room'])

@socketio.on('leave')
def leave(data):

    if data != None:
        leave_room(data['room'])

    if data != None:
        emit('my event',{'user_name':'chatbot','message':data['user_name'] + ' has left the '+data['room'] + ' room.'},room=data['room'])

@socketio.on('open_profile')
def open_profile(data):

    #The person who their profile has been opened.
    post_id= data['user']
    # print(post_id)
    # current_user
    user = find_user(post_id)

    # push_user_open_your_profile(post_id,data)
    #push that someone has viewed my profile
    push_user_liked_you(post_id,data)


    current = find_user(post_id)
    #checking whether someone has viewd my profile
    current = len(current['liked'])

    #updating notification that someone has liked my profile
    notification_update(post_id,current)

    
    # print('hello')
    # print(user['username'])

    # noti_user = len(ola_user['liked'])
    # notification_update( ola_user['username'],ola_noti_user)

    # post = find_user(user_post)
    socketio.emit('Notification',data,room=post_id)
    # print("Phakathi inside we did it, what's is up bitches!!!!!!!!!")


    # print(data['user'])
    # socketio.emit('Profile',data,room=post_id)

@app.route('/message',methods=['GET','POST'])
def message():
    id = session.get('USER')

   
    id=session.get("USER")

    form = MessageForm()
    existing_user = find_id(id)
    existing_blog_post = find_blog_post(id)
    user = existing_user['username']

    rooms = []

    for i in existing_user['liked']:
        if i['id'] == 'like':
            other_user = find_user(i['owner'])
            for k in other_user['liked']:
                if k['id'] == 'like':
                    if k['owner'] == i['user']:
                        # print(k['owner'])
                        # print('--------------------------------')
                        # print(i['user'])
                        rooms.append(i['owner'])

    rooms = list(dict.fromkeys(rooms))
    
    msg = collection()


    return render_template('public/chat.html',rooms=rooms,msg=msg,form=form,existing_blog_post=existing_blog_post,existing_user=existing_user,id=id,user=user)

def collection():
    user = session.get('USER')

    active_user = find_id_for_session(user)
    
    # chat = []
    # for i in user:
    #     chat.append(i['messages'])

    # all_chat = []
    # for l in  active_user:
    #     for k in l:
    #         all_chat.append(k)
    #         print(k)
    all_chat = active_user['messages']
    return sorted(all_chat,key=itemgetter('time'))



@socketio.on('my event')
def handle_event(data):
    id = session.get("USER")
    if data is not None:
        messages = data
        # print(data['room'])
        # print(data['room'])
        if messages != {}:
            push_user_messages(id,messages)
            push_owner_messages(data['room'],messages)
            emit('my event',{'user_name':data['user_name'],'message':data['message'],'time_stamp':strftime('%b-%d %I:%M%p',localtime())},room=data['room'],broadcast=False)
    # print(data)


@socketio.on('like')
def handle_my_custom_event(data):

    # getting the usernames
    username = data['owner']
    post_id = data['user']

    print(f"This belong to {post_id}")

    #getting the current user
    # prev = find_user(username)
    # prev_liked = prev['likes']
    
    #Recording that i have liked someone
    push_user_likes(username,data)

    #Recording that someone has liked me
    push_user_liked_you(post_id,data)

    #getting the current user to check
    #whether someone has liked their profile
    old_user = find_user(post_id)

    #checking whether someone has liked my profile
    print(old_user)
    if old_user != None:
        old_noti_user = len(old_user['liked'])

    #updating notification that someone has liked my profile
    if old_user != None:
        notification_update( old_user['username'],old_noti_user)

    # current = find_user(username)

    # current_liked = current['liked']

    # notification = len(current_liked)

    # number = notification_update( current['username'],notification)
    # noti = find_user(username)
   
    # number = noti['notification']

    socketio.emit('Notification',data,room=post_id)

# @socketio.on('profile')
# def profile(data):
#     print(data)

@app.template_filter('low')  
def low(t):
    # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1347517370))
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t/1000.0))

@app.route('/jinja')
def jinja():

    

    id = session.get('USER')

    existing_user =  find_id(id)


    profile = []
    for i in existing_user['liked']:
        # user = find_user(i['owner'])
        profile.append(i)
    
        # for k in existing_user['profile_open']:
        #     # user = find_user(k['owner'])
        #     profile.append(k)
        #     break
          

    # if len(existing_user['liked']) == 0:
    # for k in existing_user['profile_open']:
    #     profile.append(k)
    profile = sorted(profile,key=itemgetter('time'))   

    notification_numb = existing_user['notification']

    insert_notification(id,notification_numb)

    my_name = 'madi'

    age = 38

   
    

    langs = ["python","Javascript","Bash","c","Ruby"]
      
    friends = {
        "Tom":30,
        "Ally":60,
        "Tony":56,
        "Chelsea":28
    }
    colours = ('red','green')

   

    cool = True
    class gitremote:
        

        def __init__(self, name, discription, url):
            self.name = name
            self.discription =discription
            self.url = url
        def pull(self):
            return f'pullin repo {self.name}'
        def clone(self):
                return f'cloning into {self.url}'
        

    my_remote = gitremote(
        name='flask',
        discription='template design tutorial',
        url='https://github.com/jinja'
    )
    def repeat(x,qty):
        return x *  qty

    date = datetime.utcnow()

    my_html ='<h1>This is some HTML</h1>'

    suspicious = '<script>alert("YOU GOT HACKED")</script>'

    return render_template('public/jinja.html',notification_numb=notification_numb,profile=profile,existing_user=existing_user,suspicious=suspicious,my_html=my_html,date=date,age= age,cool=cool,my_remote=my_remote ,my_name= my_name,
    langs=langs,friends=friends,colours=colours,gitremote=gitremote,repeat=repeat
    )

@app.route('/about')
def admin_about():
    return "About"

@app.route('/sign-up',methods=['GET','POST'])
def sign_up():


    if request.method == 'POST':
        req = request.form

        username = req['username']
        email = req.get('email')
        password = request.form['password']

        return redirect(request.url)
    return  render_template('public/sign_up.html')

users = {
    "mitsuhiko": {
        "name": "Armin Ronacher",
        "bio": "Creatof of the Flask framework",
        "twitter_handle": "@mitsuhiko"
    },
    "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of the Python programming language",
        "twitter_handle": "@gvanrossum"
    },
    "elonmusk": {
        "name": "Elon Musk",
        "bio": "technology entrepreneur, investor, and engineer",
        "twitter_handle": "@elonmusk"
    }
}


# @app.route('/profile/<username>')
# def profile(username):

#     user = None

#     if username in users:
#         user = users[username]

#     return render_template('public/profile.html',username=username,user=user)

@app.route('/multiple/<foo>/<bar>/<baz>')
def multi(foo, bar, baz):
    return f'foo is {foo}, bar is {bar}, baz is {baz}'

@app.route('/json',methods=['POST'])
def json():
    if request.is_json:

        req = request.get_json()
        response = {
            "message":"JSON recieved",
            "name":req.get('name')
        }

        #josonify takes any python strings,list, dictionary and convert to JSON
        res = make_response(jsonify(response),200)

        return res
    else:
        res = make_response(jsonify("{'message':'No JSON received'}"),400)
        return "No JSON received",400

@app.route('/landing',methods=['GET','POST'])
def landing():
    if session.get('USER',None) is not None:
      
        return render_template('public/landing_page.html')
    else:
        print("Userename not found in session")

@app.route('/landing/create-entry',methods=['POST'])
def create_entry():
    
    req = request.get_json()

    print(req)
    user = User.objects(id=session["USER"])
    print(user)
    # if req['bio'] and req['age'] != " ":
    #     user.update_one(set__bio=req['bio'])
    #     user.update_one(set__age=req['age'])
    #     flash('Information updated','success')
    #     #return redirect(url_for('profile'))
    # else:
    #     flash("Sorry you have to update the missing information before moving foward","danger")
  
    # res = make_response(jsonify(req),200)


    return render_template(url_for('profile'))

# https://duckduckgo.com/?t=ffab&q=querystring&ia=web

@app.route('/query')
def query():

    print(request.query_string)

    return render_template("public/create_post.html")

    # if request.args:
    #     args = request.args

    #     serialized = ", ".join(f'{k}: {k}'for k, v in args.items())
    #     return f'(Query) {serialized}',200
    # else:
    #     return "No query received",200

        # if 'title' in args:
        #     #title = request.args.get('title')
        #     title = args['title']
        # print(title)
    # for k, v in args.items():
    #     print(F"{k}:{v}")

    # if "foo" in args:
    #     foo = args.get('foo')

    # print(foo)



# ?foo=foo&bar=bar&baz=baz&title=query+strings+with+flask

@app.route('/registration',methods=['POST','GET'])
def registration():
    form=RegistrationForm()
    if request.method =='POST':
        create_users(form)
        create_post(form)
        return redirect(url_for('login'))
    return render_template('public/registration.html',form=form,title='SignUp')


@app.route('/login',methods=['POST','GET'])
def login():

    form=LoginForm()
    if request.method== 'POST':
        try:
            if form.validate_on_submit():
                
                
                existing_user=find_username(form)
                blog_post = db.post.find({'author':existing_user['_id']})
                
                # print(existing_user['username'])
                # print(blog_post[0]['author'])
        
                for post in blog_post:
                    author = post
                # print(len(author))

                if existing_user['username'] == form.username.data:
                    if bcrypt.check_password_hash(existing_user['password'] ,form.password.data) == True:
                        flash('You have logged in ','success')
                        # print(existing_user['username'])
                        # print(existing_user['_id'])
                        session["USER"] = str(existing_user['_id'])
                        # print(type(session["USER"]))
                        session["USERNAME"]=form.username.data

                        if existing_user['registered'] == True:
                            return redirect(url_for('profile'))
                        else:
                            return redirect(url_for('update'))
                    else:
                        flash('Please check your password or email and try again','danger')
                        return redirect(request.url)           
                else:
                    flash('Sorry the user doesnt\'t exist please try again','danger')
                    return redirect(request.url)
        except TypeError:
            flash("The user doesn't exist",'danger')
            return redirect(request.url)
            
    else:
        return render_template('public/login.html',form=form)

def allowed_image(filename):
    
    #I want to make sure that ther's a "."
    #in the filename
    if not "." in filename:
        return False
    #else i want to split the extension from
    #the filename//split from the right and
    #from the (".",1)the right and take the
    #first element 
    ext = filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route('/upload-image',methods=['GET','POST'])
def upload_image():

    
    if request.method == 'POST':
        if request.files:

            if not allowed_image_filesize(request.cookies.get('filesize')):
                flash('File exceeded maximum size','danger')
                return redirect(request.url)

            image = request.files['image']

            if image.filename == "":
                flash("Image must have a filename",'danger')
                return redirect(request.url)
            #The .save is just a method on the file storage object that can
            #be seen by print(image)
            #The we give the method where we want to save our image
            #.filename is an attributte of the filestorage object which is holding 
            #into our image
            if not allowed_image(image.filename):
                flash("That image extension is not allowed",'danger')
                return redirect(url_for('profile'))
            else:
                #This here will senetize the filename
                #avoid nasty uploads
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['IMAGE_UPLOADS'],filename))
                
                #With this alone we don't have control of what kind of images are being uploaded
                #print('Image saved')
                id = session.get('USER')
                # print(id)
                find = existing_user(id)
                user = find['username']
                # print(user)
                # user = User.objects(id=session["USER"])
                # update_one({'id':user},{'$set':{'profile':filename}})
                upload_profile_pic(user,filename)

                # user.update_one(set__profile_pic=filename)

            return redirect(url_for('profile'))


    return render_template('public/upload_image.html')



# @app.route('/cookies')
# def cookies():

#     cookies = request.cookies

#     #This will throw an error when the cookie doesn't exist or if it
#     #has expired
#     # flavor = cookies['flavor']

#     life = cookies.get('life')
#     print(life)

#     #anything you would pass a return statement inside a python file
#     #you can pass it into make_response
#     res = make_response('Cookies',200)

#     res.set_cookie(
#         'flavor',
#         value='chocolate chip',
#         max_age =10,
#         expires=None,
#         path=request.path,
#         domain=None,
#         secure=False,
#         httponly=False,
#         samesite=False
#         )

#     res.set_cookie("chocoloate type","dark")
#     res.set_cookie("cheary","yes")

#     return res


@app.route('/profile',methods=['GET','POST'])
def profile():

    if session.get('USER',None) is not None:

        id=session.get("USER")
        existing_user = find_id(id)
        existing_blog_post = find_blog_post(id)

        #checking if there is a new like
        liked = existing_user['liked']

        liked_number = len(liked)

        all_existing_blog_post = all_existing_post()
        all_user_post = all_existing_users()
        users = []
        posts = []
        interest = []
        inter = []
        interest_return =[]

        

        for pic in all_existing_blog_post:
            id = pic['author']
            posts.append(pic['pictures'])
            name = find_id(id)
            print(name['Interest'])
            interest.append(name['Interest'])

            if name['Interest'] != []:
                users_i = name['Interest'][0].split(',')
            user_k = existing_user['Interest'][0].split(',')
            if name['Interest'] != []:
                for k in users_i:
                    interest_return.append(k)


            if name['Interest'] != []:
                if name['username'] != existing_user['username']:
                    print(len(name['liked']))
                    if existing_user['sexualPreference'] == name['gender']:
                        for i in users_i:
                            for k in user_k:
                                if i == k:
                                    if name in users:
                                        continue
                                    else:
                                        users.append(name)
        
            
        interest_return = list(dict.fromkeys(interest_return))

        pagination =users_pagination()
        post = []
        for i in posts:
            for k in i:
                post.append(k)
        
        if request.is_json:
            req = request.get_json()

            if len(existing_user['coordinates']) == 0:
                coordinates_update(existing_user,req)

            coord =[]
            for post in all_user_post:
                coord.append(post['coordinates'])

            okc_ok = (existing_user['coordinates']['lat'], existing_user['coordinates']['long'])
            d = []
            for index in coord:
                norman_ok = (index['lat'], index['long'])
                d.append(distance.distance(okc_ok , norman_ok ).km)
            response = make_response(jsonify(req))
            return response

        return render_template('public/profile.html',interest_return= interest_return, liked_number= liked_number,liked=liked,pagination=pagination,post=post,users=users,existing_user=existing_user,user=session["USER"], all_existing_blog_post= all_existing_blog_post)
    else:
        print("Userename not found in session")
        return redirect(url_for('/login'),existing_user=existing_user,existing_blog_post=existing_blog_post) 

@app.route("/logout")
def logout():
    session.pop('user',None)
    session.clear()
    res = make_response("Cookie Removed")
    res.set_cookie('foo', 'bar', max_age=0)
    return redirect(url_for('login'))


@app.route('/update',methods=['GET','POST'])
def update():
    
    form = UpdateAccountForm()
    
    if request.method == 'POST':
        #we're going to populate this field with the action that must
        #happened whe the form is submitted
        #current_user = User.objects(id=session.get('USER'))
        id = session["USER"]
       
        user = find_id(id)
       
        if user['age'] != "" and user['bio'] != "":
            return redirect(url_for('profile'))
        else:
            if form.validate_on_submit():

                age_update(form,id)
                bio_update(form,id)
                gender_update(form,id)
                sexualPreference_update(form,id)
                registered_update(id)
                interest_update(form,id)
               
            return redirect(url_for('profile'))
    else:
        return render_template('public/update_profile.html',form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)

    #This function(splitext) returns two values,the file name without,
    #the extension and it returns the extension itself,below we grab
    #both values
    # f_name,f_ext = os.path.splitext(form_picture.filename)
    
    #on this one we grab only the extension
    _,f_ext= os.path.splitext(form_picture.filename)


    #her we concanating the extesion with the randon hex to create,
    #a new name for the uploaded image
    picture_fn = random_hex + f_ext

    #getting the root path
    picture_path = os.path.join(app.root_path,'static/img',picture_fn)


    output_size = (125,125)

    i = Image.open(form_picture)
    i.thumbnail(output_size)

    id=session.get("USER") 
  

    current_user = find_blog_post(id)
    current_post = find_id(id)
    
    # current_post.update_one(push__pictures=picture_fn)
    # current_post['pictures'].append(picture_fn)
    if len(current_user['pictures']) < 7:
        push_pictures_blog_post(id,picture_fn)
    else:
        flash("Sorry you have reach a limit on number of pictures you can uplaod",'danger')
        # return redirect(url_for('profile'))
    # for post in current_post:
    #     print(post.content)

    # current_post.update_one(push_pictures=picture_fn)



    # print(current_post.content)

    print(picture_path)

    i.save(picture_path)

    # picture_path = os.path.join(app.config['IMAGE_UPLOADS'],filename)
    return picture_fn
# @app.route('/numbers',methods=['GET'])
# def pagination():
#     print(users_pagination())

    return render_template('public/profile.html')


@app.route("/account",methods=['POST','GET'])
def account():
    form=UploadsForm()

    id_=session.get("USER") 
    existing_blog_post = find_blog_post(id_)
    existing_user = find_id(id_)

    if request.method == 'POST':
        if form.validate_on_submit():
            if form.username.data != existing_user['username']:
                if find_username(form) == None:
                    username_update(form,existing_user)
                    flash('username has been updated','success')
                else:
                    flash('Sorry the username has already been taken')
            if form.email.data != existing_user['email']:
                if find_email(form) == None:
                    email_update(form,existing_user)
                    flash('email has been updated','success')
                else:
                    flash('Sorry the email has already been taken')
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
    elif request.method =='GET':
        form.username.data = existing_user['username']
        form.email.data = existing_user['email']
        
    return render_template('public/account.html',form=form,existing_user=existing_user)


@app.route("/post/new",methods=['GET','POST'])
def new_post():
    form= PostForm()
    if form.validate_on_submit():
        flash('Your Post has been created','success')
        return redirect(url_for('profile'))

    return render_template('public/create_post.html',title='Post',form=form)


@app.route("/post/<string:post_id>")
def post(post_id):
    user =session.get("USER")
    # id = str(post_id)
    # print(id)

    post = find_user(post_id)

    id = post['_id']

    author = find_blog_post(id)

    print(type(author))
    for pic in author:
        print(pic)
    

    

    return render_template('public/post.html',post=post,author=author)



@app.route("/post/<string:post_id>/update",methods=['GET','POST'])
def update_post(post_id):
    id = str(post_id)
    post = find_blog_post(id)

    print(post['author'])
    # print(session["USER"])
    # return redirect(request.url)
    if str(post['author']) != session["USER"]:
        abort(403)
    form = PostForm()
    author=str(post['author'])
    
    return render_template('public/post.html',form=form,post=post,current_user=session["USER"],author=author )

@app.route("/post/<string:post_id>/delete",methods=['POST',])
def delete_post(post_id):
    # id = str(post_id)
    id = post_id
    post = find_post(id)
    id = post['author']
    picture = post_id
    delete_existing_post(id,picture)
    # print(selected)

    # post = find_blog_post(id)
    # print(post)

    # if str(post['author']) != session["USER"]:
    #     abort(403)
    # delete_existing_post(id)
    # flash('Your post has been deleted!','success')
    # return redirect(request.url)
    return redirect(url_for('profile'))


@app.route("/hash_tag/<post_id>",methods=['POST','GET'])
def hash_tag(post_id):

    id=session.get("USER")
    tags = post_id
    tag = request.url
    

    existing_user = find_id(id)
    liked = existing_user['liked']

    liked_number = len(liked)
    all_existing_blog_post = all_existing_post()
    all_existing_user = all_existing_users()
    users = []
 
   
    
    for name in all_existing_user:
          
        users_i = name['Interest'][0].split(',')
        user_k = existing_user['Interest'][0].split(',')

        if name['username'] != existing_user['username']:
            for i in users_i:
            
                if i == tags:
                    if name in users:
                        continue
                    else:
                        users.append(name)
    return render_template('public/landing_page.html',users=users,existing_user=existing_user)
