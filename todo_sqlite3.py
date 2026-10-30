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
           created_at timestamp default (datetime('now', 'localtime'))     
        )
        ''')

def add_task(content):
    with get_db() as conn:  #添加任务
        cursor = conn.execute('insert into tasks (content) values(?)',(content,)) #在表tasks中插入content列，内容为传递来的参数
        print(f'✅ 已添加任务 [id:{cursor.lastrowid}]:{content}')

def list_tasks(show_all=False):
    with get_db() as conn:
        if show_all:
            cursor = conn.execute('select * from tasks order by id') #查看全部任务
        else:
            cursor = conn.execute('select * from tasks where status="待办" order by id') #默认只显示未完成的

        tasks = cursor.fetchall()

        if not tasks:
            print('📭 没有找到任务。')
            return

        print('\n=== 📝 我的待办清单 ===')
        for task in tasks:
            #status_icon= "✅" if task['status']=='已完成' else "⏳"
            #print(f'[{task["id"]}]{status_icon}: {task["content"]},创建于：{task["created_at"]}')
            print(f'[{task["id"]}:]{task["status"]}:: {task["content"]},创建于：{task["created_at"]}')
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
             cursor = conn.execute("drop table if exists tasks")
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

    # 3. 解析参数并执行对应函数
    args = parser.parse_args()

    # 加这一行，看看 args 到底长啥样
    print(f"【调试信息】解析出来的参数: {args}")

    if args.command == "add":
        add_task(args.content)
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
python todo_sqlite3.py add "学习SQLite的增删改查"
python todo_sqlite3.py add "去超市买菜"
python todo_sqlite3.py add "写周报"

2.查看任务
python todo_sqlite3.py list


3.完成任务
python todo_sqlite3.py done 2

4.再次查看
python todo_sqlite3.py list        # 此时只会看到 1 和 3（第 2 条不见了）
python todo_sqlite3.py list -a     # 加 -a 参数，你会看到第 2 条变成了 ✅ 已完成

5.删除任务
python todo_sqlite3.py delete 3
python todo_sqlite3.py list

6.删除任务表
python todo_sqlite3.py drop  #drop table,不只是其中的任务。下次add时，会重建table.

'''
