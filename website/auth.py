from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p>login</>"

@auth.route('/sign-up')
def sign_up():
    return "<p>Sign Up</>"