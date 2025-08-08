#!/usr/bin/env python3

from time import sleep, time
import os

FLAG = os.getenv('FLAG', 'BSIDES{fake_flag}').lower()

# Efficient string compare algorithm.
def strcmp(a, b):
    if len(a) != len(b):
        return False

    for (a_ch, b_ch) in zip(a, b):
        sleep(0.01)

        if a_ch != b_ch:
            return False

    return True

print("[ Router Login ]")

while True:
    password = input("Password: ").lower()
    start_time = time()

    if strcmp(password, FLAG):
        print("How did you guess it??")
        break
    else:
        print(f"Failed attempt took {time() - start_time} seconds.")

print("Goodbye!")