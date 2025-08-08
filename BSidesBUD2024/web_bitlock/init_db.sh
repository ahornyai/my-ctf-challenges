#!/bin/sh

sqlite3 users.db <<SQL
CREATE TABLE users (username VARCHAR(255), password VARCHAR(255));
SQL
