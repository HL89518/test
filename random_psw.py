import random
import string

def generate_password(length=8):
    char=string.ascii_letters+string.digits+string.punctuation
    return "".join(random.choice(char) for _ in range(length))

def generate_password_digit(length=6):
    char=string.digits
    return "".join(random.choice(char) for _ in range(length))


print(generate_password(12))
print(generate_password(8))
print(generate_password_digit(8))
print(generate_password_digit(7))


def generate_password_sec(length=16):
    upper=string.ascii_uppercase
    lower=string.ascii_lowercase
    digits=string.digits
    symbols='!@#$%^&*'
    all_chars=upper+lower+digits+symbols
    password_1=random.sample(all_chars,length-4)
    password_2=[random.choice(upper),random.choice(lower),random.choice(digits),random.choice(symbols)]
    password=password_1+password_2
    print(':',password)
    random.shuffle(password)
    return ''.join(password)

print(generate_password_sec(8))
print(generate_password_sec())

