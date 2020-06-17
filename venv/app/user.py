class User:
    def __init__(self,username,firstname,lastname,email,password):
        self.username = username
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname

    @staticmethod
    def is_authenticated(self):
        return True

    @staticmethod
    def is_active(self):
        return True

    @staticmethod
    def is_annoymous(self):
        return True
        
    def get_id(self):
        return self.username
    
    


