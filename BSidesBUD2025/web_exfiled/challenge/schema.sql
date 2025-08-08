-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- Table: users
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL
);

-- Table: tests
CREATE TABLE tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL
);

-- Table: questions
CREATE TABLE questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL,
    question VARCHAR(255) NOT NULL,
    answer BOOLEAN NOT NULL,
    FOREIGN KEY (test_id) REFERENCES tests(id)
);

-- Table: submissions
CREATE TABLE submissions (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (test_id) REFERENCES tests(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Table: submission_answers
CREATE TABLE submission_answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    answer BOOLEAN NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions(submission_id),
    FOREIGN KEY (question_id) REFERENCES questions(question_id)
);

-- Create tests
INSERT INTO tests (id, title, description) VALUES
(0, '🧮 Math Test', 'Covers algebra, geometry, and basic arithmetic.'),
(1, '📜 History Test', 'Includes world history and important events.'),
(2, '🏁 Flag Test', 'Covers all the bits in the flag.');

-- Math questions
INSERT INTO questions (test_id, question, answer) VALUES
(0, 'Is 0 an even number?', 1),
(0, 'Is 9 a prime number?', 0),
(0, 'Is the square root of 25 equal to 5?', 1),
(0, 'Is 2 + 2 equal to 5?', 0),
(0, 'Is π (pi) a rational number?', 0),
(0, 'Is -3 less than -5?', 0),
(0, 'Is 1 a multiple of every integer?', 0),
(0, 'Is 100 divisible by 10?', 1),
(0, 'Is the product of two odd numbers always odd?', 1),
(0, 'Is the sum of the angles in a triangle always 180 degrees?', 1);

-- History questions
INSERT INTO questions (test_id, question, answer) VALUES
(1, 'Was Julius Caesar a Roman Emperor?', 0),
(1, 'Did World War II end in 1945?', 1),
(1, 'Did the Cold War involve direct combat between the USA and USSR?', 0);