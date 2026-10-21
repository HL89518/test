from urllib.request import urlopen

def getText(filename):
   if filename.startswith('http://') or filename.startswith('https://'):
       txt=urlopen(filename).read().decode('utf-8') ## 使用 urlopen 直接读取网址内容，并以 utf-8 解码
   else:
     with open(filename,'r') as f:
       txt=f.read()
   txt=txt.lower()
   for symbol in '''!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~0123456789''':
        txt=txt.replace(symbol,' ')
   return txt

def WordCount(filename):
     hamletTxt=getText(filename)
     words=hamletTxt.split() #按空格分词
     counts={} #字典
     for word in words:
         counts[word]=counts.get(word,0)+1 #字典中key为word的值等于原计数值加1，若原字典没有这个word，就取0再加1，即为第一个
     items=list(counts.items())  #将字典转为列表
     items.sort(key=lambda x:x[1],reverse=True)  #按key(word)对应的value(即词频）来排序）
     for i in range(10):
         word,count=items[i]
         print('{0:<10}{1:>5}'.format(word,count))
     if filename.startswith('http://') or filename.startswith('https://'):
         outfilename ='WordCount_Url.txt'
     else:
         outfilename ='WordCount_Txt.txt'
     with open(outfilename,'w',encoding='utf-8') as f:
         for i in range(len(items)):
             word,count=items[i]
             f.write('{0:<10}{1:>5}\n'.format(word,count))


print('=======================URL=====================')
   #WordCount('https://docs.python.org/3.16/tutorial/errors.html')
WordCount('https://python123.io/resources/pye/hamlet.txt')
print('=======================txt=====================')
WordCount('hamlet.txt')


import jieba
txt=open('threekingdoms.txt','r',encoding='utf-8').read()
excludes={'将军','却说','荆州','二人','不可','不能','如此','商议','如何','左右','次日','大喜','军马'}
words=jieba.lcut(txt)
counts={}
for word in words:
    if len(word)==1:
      continue  #单个的字跳过本次循环
    elif word=='诸葛亮' or word=='孔明曰':
         rword='孔明'
    elif word=='关公' or word=='云长':
         rword='关羽'
    elif word=='玄德' or word =='玄德曰':
         rword='刘备'
    elif word=='孟德' or word =='丞相':
         rword='曹操'
    else:
         rword=word
    counts[rword]=counts.get(rword,0)+1
for word in excludes:
    del counts[word]
items=list(counts.items())
items.sort(key=lambda x:x[1],reverse=True)
print('=============threekingdoms human TOP10 =============')
for i in range(10):
    word,count=items[i]
    print('{0:<10}{1:>5}'.format(word,count))
with open('threekingdomshuman.txt', 'w', encoding='utf-8') as f:
    for i in range(len(items)):
        word, count = items[i]
        f.write('{0:<10}{1:>5}\n'.format(word, count))



