import re

class user_credentials():

    def __init__(self,email,password):
        self.email = email
        self.password = password

    def email_check(self):
        
        if re.findall(r".*\@.*.com",self.email):

            return True
        else:

            return False

    def password_check(self):
        return len(self.password)>7

    def get_email(self):
        return self.email
    
    def get_password(self):
        return self.password
            

