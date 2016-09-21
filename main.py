# Kimberly Wrate
# Lesson 2 for Udacity's web development course
# URL: https://user-signup-144117.appspot.com
# Sign up users
# name, password, verify password, email
# welcome page redirected: welcome?username=x; says, "Welcome, username!"
# show an error message if nothing is entered
# username or email with a space is invalid
# keep invalid usernames and emails in the form
# when invalid passwords are entered, clear the password textboxes
# Email is an optional field

# Problems:
# All I want now is for the error message to appear on the appropriate line. -- Not absolutely necessary, though.
# I also need to enable multiple error messages to appear at once. --I'm going to try changing elif to if. -- Could I get by without this? I think so.
# Textboxes are too squished together (or too far apart) -- Not the end of the world though.

import re
import cgi

#Check for valid username, password, and email address
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASSWORD_RE = re.compile("^.{3,20}$")
def valid_password(password):
    return PASSWORD_RE.match(password)

EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

def escape_html(s):
        return cgi.escape(s, quote = True)
    

import webapp2

form="""
<form method="post">
    <h1>Signup</h1>
    <br>
    <label>
        Username
	<input type="text" name="username" value="%(username)s">
    </label>
    <br>
    <label>
        Password
	<input type="password" name="password">
    </label>
    <br>
    <label>
        Verify Password
	<input type="password" name="verify">
    </label>
    <br>
    <label>
        Email (optional)
	<input type="text" name="email" value="%(email)s">
    </label>
    <div style="color: red">%(error)s</div>
    <br>
    <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", username="", email=""):
        self.response.out.write(form % {"error": error,
                                        "username": escape_html(username),
                                        "email": escape_html(email)})
        
    def get(self):
        self.write_form()
        
    def post(self):
        user_name = self.request.get('username')
        username = valid_username(user_name)
        user_password = self.request.get('password')
        verify_password = self.request.get('verify')
        user_email = self.request.get('email')
        if(user_email != ""):
            email = valid_email(user_email)
        else:
            email = True
        
        if not(username):
            self.write_form("Invalid username", "", user_email)
        elif not(valid_password(user_password)):
            self.write_form("Invalid password", user_name, user_email)
        elif(user_password != verify_password):
            self.write_form("Your passwords didn't match", user_name, user_email)
        elif not(email):
            self.write_form("Invalid e-mail address", user_name, "")
        else:
            self.redirect("/welcome?username="+user_name)


class WelcomeHandler(webapp2.RequestHandler): 
    def get(self):
        user_name = self.request.get('username')
        message = 'Welcome, ' + user_name + '!'
        self.response.out.write(message)

app = webapp2.WSGIApplication([('/', MainPage), ('/welcome', WelcomeHandler)],
                                debug=True)
