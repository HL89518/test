import os, sqlite3

db_file = os.path.join(os.path.dirname(__file__), 'test3.db')  #连接目录及文件名
if os.path.isfile(db_file):
    os.remove(db_file)  #文件存在时先删除

# 初始数据:
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
cursor.execute(r"insert into user values ('A-001', 'Adam', 95)")
cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
conn.commit()
cursor.close()
conn.close()

def get_score_in(low, high):
    with sqlite3.connect(db_file) as conn:
        cursor=conn.cursor()
        cursor.execute('select * from user where score between ? and ? order by score',(low,high))
        names=[(row[0],row[1],row[2]) for row in cursor.fetchall()]

    return names



# 测试:
print(get_score_in(60, 80))
print(get_score_in(80, 95))
print(get_score_in(60, 100))

assert get_score_in(80, 95) == [('A-001','Adam',95)], get_score_in(80, 95)


print('Pass')

with sqlite3.connect(db_file) as conn:
    cursor = conn.cursor()
    cursor.execute('update user set score =? where id=?',(99,'A-001'))
    cursor.execute('delete from user where id=?',('A-002',))


print('names after update A-001 score to 99&delete A-002:',get_score_in(60, 100))

conn = sqlite3.connect(db_file)
cursor = conn.cursor()
try:
    cursor.execute('insert into user values (?, ?, ?)', ('A-004', 'Bob', 88))
    cursor.execute('update user set score = score - 10 where id = ?', ('A-001',))
    conn.commit()              # 全部成功才提交
except sqlite3.Error as e:
    conn.rollback()            # 出错则回滚，保持数据一致
    print('出错：', e)


print(get_score_in(60, 100))