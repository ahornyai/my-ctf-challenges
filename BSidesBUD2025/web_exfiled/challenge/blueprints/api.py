from flask import Blueprint, request, session, redirect, request
from auth import authenticated, is_teacher
from bot import check_submission
from database import *
from urllib.parse import quote_plus
from threading import Thread
from time import time

api = Blueprint('api', __name__)

@api.route("/login", methods=["GET", "POST"])
def handle_login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    next_page = request.args.get("next", "/").strip()

    if "username" in session:
        return redirect(next_page)

    success, user = login(username, password)

    if not success:
        return redirect("/login?err=" + quote_plus("Failed to login."))

    session["user_id"] = user[0]
    session["username"] = user[1]
    session["role"] = user[2]
    session["last_submission"] = 0

    return redirect(next_page)

@api.route("/register", methods=["POST"])
def handle_register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if not username.isalnum():
        return redirect("/register?err=" + quote_plus("The username has to be alphanumeric."))

    if len(username) < 3:
        return redirect("/register?err=" + quote_plus("The username is too short."))

    if len(username) > 255:
        return redirect("/register?err=" + quote_plus("The username is too long."))

    success = register(username, password)

    if not success:
        return redirect("/register?err=" + quote_plus("A user with this username already exists."))

    return redirect("/register?msg=" + quote_plus("Successful registration."))

@api.route("/student/submit-test", methods=["POST"])
@authenticated
def submit_test():
    test_id = request.form.get("test_id", "").strip()

    if not test_id.isdecimal():
        return redirect("/?err=" + quote_plus("bruh"))
    
    questions = get_questions(test_id)
    
    if len(questions) == 0:
        return redirect("/?err=" + quote_plus("This test doesn't exist."))

    ids = [q[0] for q in questions]
    answers = dict()

    for id in ids:
        answer = request.form.get("q" + str(id), "").strip()

        if answer != "1" and answer != "0":
            return redirect("/?err=" + quote_plus("Incorrect answer format."))

        answers[id] = int(answer)

    submission_id = create_submission(test_id, session["user_id"], answers)

    return redirect("/?msg=" + quote_plus("Successful submission. Submission ID: " + str(submission_id)))

@api.route("/student/submit-external", methods=["POST"])
@authenticated
def send_test():
    url = request.form.get("url", "").strip()

    if len(url) == 0:
        return redirect("/submit?err=" + quote_plus("Url is missing."))
    
    cooldown = time() - session["last_submission"]

    if cooldown < 10:
        return redirect("/submit?err=" + quote_plus(f"You are on a cooldown, wait {round(10-cooldown, 1)} seconds before your next submission."))
    
    print(f"Scheduling {url} submitted by: {session["username"]}")
    session["last_submission"] = time()
    Thread(target=check_submission, args=(url,)).start()

    return redirect("/submit?msg=" + quote_plus("Successful submission"))

@api.route("/teacher/check-test/<int:submission_id>/<int:question_id>", methods=["GET", "OPTIONS"])
@is_teacher
def check_test(submission_id, question_id):
    if check_answer(submission_id, question_id):
        return "yayy, correct answer! :D", 200
    else:
        return "wrong answer :(", 418
