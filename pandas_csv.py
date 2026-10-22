import pandas as pd

df=pd.read_csv('sales.csv') # or pd.read_excel('sales.xlsx')

print('==数据预览===')
print(df.dtypes) #查看列类型
print(df.shape)  #行数，列数
l,c=df.shape
print(l,c)
print(df) #全部数据
print(df.head(3)) #前三行数据
print(df.tail(3)) #尾三行数据

print('\n===求和/均值===')
print('总数量：',df['quantity'].sum()) #单列求和
print('平均单价：',df['price'].mean()) #单列求均值

print('\n===数值列描述统计===')
print(df[['quantity','price']].describe())  # 一次性看数值列的常用统计量，会输出 count、mean、std、min、25%/50%/75% 分位数、max，适合快速摸底

print('\n===按地区分组计数===')
print(df.groupby('region').size())  # 按地区分组计数（每个地区多少条记录）

print('\n===按地区聚合===') #按地区统计数量总和与单价均值
print(df.groupby('region').agg(
    order_count=('quantity', 'size'), #按分组后每组quantity的个数来计数
    total_qty=('quantity', 'sum'),  #按分组后每组quantity的值求和
    avg_price=('price', 'mean'),  #按分组后每组price的值求平均值
))

print(df.groupby(['region', 'product']).size()) # 按地区 + 产品分组计数


print('\n===求每行销售额===')
df['sales']=df['quantity']*df['price']    # 1. 每行销售额 = quantity * price

print(df)
print('\n===求每行销售额及表尾追加求和===')
total_row={
    'region':'合计',
    'product':'',
    'quantity':df['quantity'].sum(),
    'price':'',
    'sales':df['sales'].sum(),
}

df=pd.concat([df,pd.DataFrame([total_row])],ignore_index=True)
print(df)

