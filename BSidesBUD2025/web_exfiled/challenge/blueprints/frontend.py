from flask import Blueprint, session, redirect, render_template
from auth import authenticated
from database import get_tests, get_questions, get_test_info
from urllib.parse import quote_plus

web = Blueprint('web', __name__)

@web.route("/login")
def login():
    return render_template("login.html")

@web.route("/register")
def register():
    return render_template("register.html")

@web.route("/")
@authenticated
def dashboard():
    return render_template("dashboard.html", username=session["username"], role=session["role"], tests=get_tests())

@web.route("/submit")
@authenticated
def submit():
    return render_template("submit.html", username=session["username"], role=session["role"])

@web.route("/take-test/<int:test_id>")
@authenticated
def test(test_id):
    test_info = get_test_info(test_id)

    if test_info is None:
        return redirect("/?err=" + quote_plus("This test doesn't exist."))

    return render_template("test.html", 
                           username=session["username"], 
                           role=session["role"], 
                           questions=get_questions(test_id), 
                           test_id=test_info[0], 
                           test_title=test_info[1])

@web.route("/logout")
@authenticated
def logout():
    session.clear()

    return redirect("/login")