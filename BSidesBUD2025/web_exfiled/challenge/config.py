import os

DATABASE_PATH = "database.db"
HOST = os.getenv("HOST", "http://localhost:1337")
TEACHER_USERNAME = os.getenv("TEACHER_USERNAME", "teacher")
TEACHER_PASSWORD = os.getenv("TEACHER_PASSWORD", "password")
FLAG = os.getenv("FLAG", "bsides{fake_flag}").encode()