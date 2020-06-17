

class creation:
    def json(self):
        user_dict = {
        "username":self.username,
        "email":self.email,
        "password":self.password,
        "age":self.age,
        "bio":self.bio,
        "categories":self.categories,
        "registered":self.registered,
        "date_create":self.datetime.utcnow,
        "gender":self.gender,
        "sexualPreference":self.sexualPreference,
        "AccountVerification":0,
        "coordinates":0 
    }

    meta = {
        "indexe":['username','email'],
        "ordering":['-date_created']
    }

def Post(self):
    BlogPost ={
    "title":"",
    "content":"",
    "author" :"",
    "date_create":"",
    }
    return json.dumps(BlogPost)

#Dynamic documents

BlogPost= {

    "title":""
  
}