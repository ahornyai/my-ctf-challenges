from functools import wraps
from flask import session, redirect, jsonify

def authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect("/login")
        
        return f(*args, **kwargs)
    return decorated_function

def is_teacher(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "role" not in session or session["role"] != "teacher":
            return jsonify({"error": "nice try :D"}), 401
        
        return f(*args, **kwargs)
    return decorated_function