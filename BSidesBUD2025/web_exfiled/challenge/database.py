import sqlite3
from flask import g, current_app
from argon2 import PasswordHasher
from config import DATABASE_PATH, TEACHER_PASSWORD, TEACHER_USERNAME, FLAG

PH = PasswordHasher()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    db = get_db()
    cur = db.cursor()

    with current_app.open_resource('schema.sql', mode='r') as f:
        cur.executescript(f.read())
    
    # Create teacher user
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'teacher')", [TEACHER_USERNAME, PH.hash(TEACHER_PASSWORD)])
    
    # Place flag questions (test_id=2)
    bits = bin(int(FLAG.hex(), 16))[2:]

    for i in range(len(bits)):
        cur.execute(f"INSERT INTO questions (test_id, question, answer) VALUES (2, 'What is the value of the {i+1}. bit in the flag?', ?);", [int(bits[i])])

    db.commit()

def register(username, password):
    db = get_db()
    cur = db.cursor()

    try:
        hashed_password = PH.hash(password)
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'student')", [username, hashed_password])

        db.commit()

        return True
    except sqlite3.IntegrityError: # This error occurs if the username already exists
        db.rollback()
        return False

def login(username, password):
    user = query_db("SELECT * FROM users WHERE username=?", [username], True)

    if user == None:
        return False, None
    
    try:
        if PH.verify(user[2], password):
            return True, (user[0], user[1], user[3])
    except:
        return False, None
    
    return False, None

def get_tests():
    return query_db("SELECT * FROM tests")

def get_test_info(test_id):
    return query_db("SELECT id, title FROM tests WHERE id=?", [test_id], True)

def get_questions(test_id):
    return query_db("SELECT question_id, question FROM questions WHERE test_id=?", [test_id])

def create_submission(test_id, user_id, answers):
    db = get_db()
    cur = db.cursor()

    cur.execute("INSERT INTO submissions (test_id, user_id) VALUES (?, ?)", [test_id, user_id])
    submission_id = cur.lastrowid

    for question_id, answer in answers.items():
        cur.execute("INSERT INTO submission_answers (submission_id, question_id, answer) VALUES (?, ?, ?)", [submission_id, question_id, answer])
    
    db.commit()
    return submission_id

def check_answer(submission_id, question_id):
    user_answer = query_db("SELECT answer FROM submission_answers WHERE submission_id=? AND question_id=?", [submission_id, question_id], one=True)
    correct_answer = query_db("SELECT answer FROM questions WHERE question_id=?", [question_id], one=True)

    if user_answer == None:
        return False

    return user_answer == correct_answer