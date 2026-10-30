import sqlite3
import argparse


DB_FILE='todo_sqlite3.db'

def get_db():
    conn = sqlite3.connect(DB_FILE) #连接数据库，如果不存在会自动创建
    conn.row_factory=sqlite3.Row #可以通过列名访问数据，像字典一样
    return conn

def init_db():
    with get_db() as conn:  #初始化建表
        conn.execute('''
        create table if not exists tasks(
           id integer primary key autoincrement,
           content text not null,
           status text default '待办',
           category text default '未分类',
           priority integer default 3, 
           created_at timestamp default (datetime('now', 'localtime'))     
        )
        ''')

def add_task(content,category,priority):
    with get_db() as conn:  #添加任务
        cursor = conn.execute('insert into tasks (content,category,priority) values(?,?,?)',(content,category,priority)) #在表tasks中插入content列，内容为传递来的参数
        print(f'✅ 已添加任务 [id:{cursor.lastrowid}]:{content}(分类: {category}, 优先级: {priority})')

def edit_task(task_id,new_content):
    with get_db() as conn:
        cursor=conn.execute('update tasks set content=? where id=?',(new_content,task_id))
        if cursor.rowcount > 0:
            print(f"✏️ 任务 {task_id} 已修改为：{new_content}")
        else:
            print(f"❌ 找不到 ID 为 {task_id} 的任务。")

def list_tasks(show_all=False):
    with get_db() as conn:
        if show_all:
            cursor = conn.execute('select * from tasks order by priority,id') #查看全部任务
        else:
            cursor = conn.execute('select * from tasks where status="待办" order by priority,id') #默认只显示未完成的

        tasks = cursor.fetchall()

        if not tasks:
            print('📭 没有找到任务。')
            return

        print('\n=== 📝 我的待办清单 ===')
        for task in tasks:
            #status_icon = "✅" if task["status"] == "已完成" else "⏳"
            status_icon = ["已办" if task["status"] == "已完成" else "待办"]
            # 根据数字显示不同的优先级图标
            #p_icon = "🔴" if task["priority"] == 1 else ("🟡" if task["priority"] == 2 else "🟢")
            p_icon = ["紧急" if task["priority"] == 1 else ("不急" if task["priority"] == 2 else "可慢")]
            # 打印时带上分类和优先级
            print(f"[{task['id']}] {status_icon} {p_icon} [{task['category']}] {task['content']}")
        print('========================================')




def complete_task(task_id):
    with get_db() as conn:
        cursor=conn.execute('update tasks set status="已完成" where id=?',(task_id,))
        if cursor.rowcount > 0:
            print(f"🎉 任务 {task_id} 已完成！")
        else:
            print(f"❌ 找不到 ID 为 {task_id} 的任务。")

def delete_task(task_id):
    """删除任务"""
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount > 0:
            print(f"🗑️ 任务 {task_id} 已删除。")
        else:
            print(f"❌ 找不到 ID 为 {task_id} 的任务。")

def drop_table():
    confirm=input("⚠️ 警告：这会删除所有任务！确定要清空吗？(y/n): ")
    if confirm.lower()=='y':
        with get_db() as conn:
             conn.execute("drop table if exists tasks")
             print(f'任务表已清除！bye-bye!')
    else:
        print('✅ 已取消drop操作。')


def main():
    # 1. 初始化数据库（每次运行都检查一下表在不在）
    init_db()

    # 2. 设置命令行参数解析器
    parser = argparse.ArgumentParser(description="📝 极简命令行待办清单")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 子命令：add
    parser_add = subparsers.add_parser("add", help="添加新任务")
    parser_add.add_argument("content", type=str, help="任务的内容")
    parser_add.add_argument('-c',"--category",type=str,default='未分类',help='任务分类（如：生活，学习，工作）')
    parser_add.add_argument('-p',"--priority",type=int,choices=[1,2,3,],default=3,help='优先级1高2中3低')
    # 子命令：list
    parser_list = subparsers.add_parser("list", help="查看任务")
    parser_list.add_argument("-a", "--all", action="store_true", help="显示所有任务（包括已完成的）")

    # 子命令：done
    parser_done = subparsers.add_parser("done", help="标记任务为已完成")
    parser_done.add_argument("id", type=int, help="任务的编号")

    # 子命令：delete
    parser_delete = subparsers.add_parser("delete", help="删除任务")
    parser_delete.add_argument("id", type=int, help="任务的编号")

    # 子命令：drop
    parser_drop = subparsers.add_parser("drop", help="删除任务表格")
    #parser_drop.add_argument("id", type=int, help="任务的编号")

    # 子命令：edit
    parser_edit =subparsers.add_parser('edit',help='修改任务内容')
    parser_edit.add_argument('id',type=int, help='要修改的任务编号')
    parser_edit.add_argument('new_content',type=str, help='新的任务内容')

    # 3. 解析参数并执行对应函数
    args = parser.parse_args()

    # 加这一行，看看 args 到底长啥样
    #print(f"【调试信息】解析出来的参数: {args}")

    if args.command == "add":
        add_task(args.content,args.category,args.priority)
    elif args.command =='edit':
        edit_task(args.id,args.new_content)
    elif args.command == "list":
        list_tasks(args.all)
    elif args.command == "done":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command =='drop':
        drop_table()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()


'''
chcp 65001  #把编码改成 UTF-8,图标显示正常

1.命令行添加任务
python todo_sqlite3_a.py add "学习SQLite的增删改查" -c  '学习' -p  2
python todo_sqlite3_a.py add "去超市买菜" -c '生活'   #默认p为3
python todo_sqlite3_a.py add "写周报"  -c '工作'  -p 2
python todo_sqlite3_a.py add "开会"  -c '工作'  -p 1

2.查看任务
python todo_sqlite3_a.py list


3.完成任务
python todo_sqlite3_a.py done 2

4.再次查看
python todo_sqlite3_a.py list        # 此时只会看到 1 ， 3，4（第 2 条不见了）
python todo_sqlite3_a.py list -a     # 加 -a 参数，你会看到第 2 条变成了 ✅ 已完成

5.修改内容
python todo_sqlite3_a.py edit 3 '写月度和周度总结'


6.删除任务
python todo_sqlite3_a.py delete 1
python todo_sqlite3_a.py list

7.删除任务表
python todo_sqlite3_a.py drop  #drop table,不只是其中的任务。下次add时，会重建table.

'''
