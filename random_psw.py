import random
import string

def generate_password(length=8): #字母，数字和标点符号  包含 ASCII 中所有 32 个可打印的标点符号 !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
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
    password_1=random.sample(all_chars,length-4)  #生成某长度的密码
    password_2=[random.choice(upper),random.choice(lower),random.choice(digits),random.choice(symbols)] #生成包含4种的4位密码
    password=password_1+password_2
    print(':',password) #列表
    random.shuffle(password) #对生成的密码再动态随机排序
    return ''.join(password) # 将列表连接成字符串密码

print(generate_password_sec(8)) #8位密码
print(generate_password_sec())  #16位（默认位数）密码

