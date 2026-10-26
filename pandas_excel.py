import pandas as pd



data={
'产品名称':['iphone17','ipad pro','macbook air'],'价格':[6999,5799,8999],'库存':[100,50,30]}

df=pd.DataFrame(data)

print(df.head())

df.to_excel('apple产品List.xlsx',index=False)

print('写入完成')

print('读取表格：')
df1=pd.read_excel('apple产品List.xlsx')

#打印前5行
print(df1.head())
print('#使用单层 [] 结合切片（类似 Python 列表')
print(df1[0:2]) #取第0，1行。

print('取单行（返回 Series）')
print(df1.iloc[2]) #取第2行

print('取连续的多行（切片，同样是左闭右开）')
print(df1.iloc[0:3])
print(df1.iloc[[0, 2]]) #取第0，2行
print(df1.iloc[-2:]) #取最后2行

print('#=====选择单列,产品名称：======')
print(df1['产品名称'])
print('=====#选择多列，自动带表头：=====')
print(df1[['产品名称','价格','库存']])
'''当你给外层 [] 传入一个列表时，Pandas 就知道你要按列提取。单层 df1['产品名称'] 提取出来的是一个 Series（一维数组），而双层 df1[['产品名称','价格']] 提取出来的是一个 DataFrame（二维表格）。'''

print('======按条件筛选：======')
print(df1[df1['价格']>7000])
'''#按条件筛选,内层 df1['价格']>7000：先执行判断。它会生成一个由 True 和 False 组成的 布尔序列（Boolean Series）。比如 [False, False, True]。

外层 []：把上面生成的这个布尔序列传给外层。Pandas 收到布尔序列后，会逐行对比。如果是 True，就保留这一行；如果是 False，就丢弃这一行。

总结：当你给外层 [] 传入一个布尔条件时，Pandas 就知道你要按行过滤数据。这叫“布尔索引”。'''

print('=======修改表格内容，增加列,再存新档：=======')
df1['折扣价']=df1['价格']*0.9
print(df1.head())
df1.to_excel('apple产品List_1.xlsx',index=True)


import random
print('=====将100个表格放在同一EXCEL表格（产品销售汇总100.xlsx)的各SHEET页下=====')
products=['香蕉','苹果','桔子','西瓜','葡萄','菠萝','草莓','芒果','梨','桃子']
prices=[1,2,3]
quantities=[10,20,30,40,50,60,70,80]
salesman=['张三','李四','王五','赵六']
with pd.ExcelWriter('产品销售汇总100.xlsx', engine='openpyxl') as writer:  #将100个表格放在同一表格的各SHEET页下
  for i in range(1,101):
    df=pd.DataFrame( #生成一个二维行列表格数据
        {
            '产品名称':random.choices(products,k=5),#随机生产一个5个产品名称的列表
            '产品价格':random.choices(prices,k=5),
            '产品数量':random.choices(quantities,k=5),
            '产品销售':random.choices(salesman,k=5)
        }
    )

    df.to_excel(writer,sheet_name=f'products_{i}',index=False) #将df写入当前sheet中

print('======#将同一个EXCEl表中的各SHEET页合并成一个sheet======')
data=[]
for i in range(0,100):
    df=pd.read_excel('产品销售汇总100.xlsx',sheet_name=i)  #读第i个表格
    data.append(df) #data是一个列表,df是一个二维表格
df1=pd.concat(data,ignore_index=True)  #将DATA这个列表中的数据拼接成DATAFRAME
'''1.保留第一份的列名：Pandas 会拿 data 列表里的第一个表格（即第 0 个 Sheet）的列名，作为最终大表格的总表头。
   2.自动对齐与匹配：当它在拼第二个、第三个……直到第 100 个表格时，它会去检查这些表格的列名。
   3.如果后面表格的列名和第一个表格完全一样（比如都有'产品名称', '价格', '库存'），它就直接把数据行接在下面，后面的列名自动被忽略（丢弃），不会在中间插一行表头。'''
df1.to_excel('产品汇总表all_in_one.xlsx',index=False)     #加上 ignore_index=True 后：Pandas 在拼接时，会忽略掉原来那 100 个表格各自的旧行号。
print(f'汇总完成，共{len(df1)}行')
rows,columns=df1.shape
print('总行数{},总列数{}'.format(rows,columns))


print('=====随机数据组合生成5个表格=====')
products=['香蕉','苹果','桔子','西瓜','葡萄','菠萝','草莓','芒果','梨','桃子']
prices=[1,2,3,4,5]
quantities=[10,20,30,40,50,60,70,80]
salesman=['张三','李四','王五','赵六']

for i in range(1,6):
    df=pd.DataFrame(
        {
            '产品名称':random.choices(products,k=5),
            '产品价格':random.choices(prices,k=5),
            '产品数量':random.choices(quantities,k=5),
            '产品销售':random.choices(salesman,k=5)
        }
    )
    df.to_excel('产品'+str(i)+'.xlsx',index=False)

print('=====将上面生成的5个命名有规律的表格文件合并成一个表格=====')

data=[]
for i in range(1,6):
    df=pd.read_excel('产品'+str(i)+'.xlsx') #将命名有规律的EXCEL表格中数据汇总成一个表格
    data.append(df)
df1=pd.concat(data,ignore_index=True)
df1.to_excel('产品汇总表.xlsx',index=False)
print(f'汇总完成，共{len(df1)}行')



import os
print('=====随机数据组合生成5个表格存到子目录123下面=====')
products=['香蕉','苹果','桔子','西瓜','葡萄','菠萝','草莓','芒果','梨','桃子']
prices=[1,2,3,4,5]
quantities=[10,20,30,40,50,60,70,80]
salesman=['张三','李四','王五','赵六']
os.makedirs('123',exist_ok=True)  #不存在就自动创建，存在就跳过。
for i in range(1,6):
    df=pd.DataFrame(
        {
            '产品名称':random.choices(products,k=5),
            '产品价格':random.choices(prices,k=5),
            '产品数量':random.choices(quantities,k=5),
            '产品销售':random.choices(salesman,k=5)
        }
    )
    df.to_excel(r'123/产品'+str(i)+'.xlsx',index=False)


print('=====子目录123下面的所有EXCEL文件汇总成一个文件存在123下面=====')
data=[]
for i in os.listdir('123'):  #将同一文件夹123下的表格汇总
    path=os.path.join('123',i)
    if not os.path.isfile(path): #若不是文件（是文件夹），则跳过不理，继续下一个循环
        continue
    if i=='产品汇总表.xlsx':
        continue
    print(i)  #列出所有文件
    df=pd.read_excel(path)
    data.append(df)

df1=pd.concat(data,ignore_index=True)
df1.to_excel('123/产品汇总表.xlsx',index=False)
print(f'汇总完成，共{len(df1)}行')




