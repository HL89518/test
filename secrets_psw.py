import secrets
import string
def generate_password(length=8):
    char=string.ascii_letters+string.digits+string.punctuation
    return ''.join(secrets.choice(char) for _ in range(length))

def generate_password_digit(length=6):
    char=string.digits
    return ''.join(secrets.choice(char) for i in range(length))

print(generate_password(12))
print(generate_password())
print(generate_password_digit(8))
print(generate_password_digit())

def generate_password_sec(length=16):
    upper=string.ascii_uppercase
    lower=string.ascii_lowercase
    digits=string.digits
    symbol='!@#$%^&*'
    all_chars=upper+lower+digits+symbol
    password_1=[secrets.choice(all_chars) for i in range(length-4)]
    password_2=[secrets.choice(upper),secrets.choice(lower),secrets.choice(digits),secrets.choice(symbol)]
    password=password_1+password_2
    #print('password:', password)
    secrets.SystemRandom().shuffle(password)  ## 安全地打乱顺序（secrets 没有提供 shuffle，可借助 SystemRandom）
    #print('password 随机排序:', password)
    return ''.join(password)

print(generate_password_sec(8))
print(generate_password_sec())


print('生成安全令牌（Token）')
print(secrets.token_urlsafe(16))
print(secrets.token_bytes(16))
print(secrets.token_hex(16))
