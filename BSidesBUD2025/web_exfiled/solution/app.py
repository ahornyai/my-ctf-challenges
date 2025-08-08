from flask import Flask
from Crypto.Util.number import long_to_bytes

app = Flask(__name__)

questions = [2]*199

@app.route("/set_flag/<int:index>/<int:value>")
def set_question_bit(index, value):
    questions[index] = value
    print(f"setting {index}: {value}, number of unset bits: {questions.count(2)}")
    print("".join(map(str, questions)))

    return "ok"

@app.route("/flag")
def get_flag():
    print(questions)
    return long_to_bytes(int("".join(map(str, questions)), 2))

@app.route("/reset")
def reset():
    global questions
    questions = [2]*199
    return "done"

app.run(host='0.0.0.0', port=4444, ssl_context=("cert.pem", "key.pem"))