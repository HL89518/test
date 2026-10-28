import os  # 路径操作、目录创建、遍历、重命名
import pandas as pd  # 生成并导出 Excel
import random   # 生成随机数据
import shutil  # 递归删除、复制文件

print("====== A.os.makedirs ======")
shutil.rmtree("123",ignore_errors=True)                  # 123 及里面所有内容全删
print("123 已删除") #若123已存在，整个删掉，避免多次运行该程序时文件越积越多
os.makedirs('123',exist_ok=True)
os.makedirs('./123/test/new/deep/dir',exist_ok=True)  #不存在就自动创建，存在就跳过。
print('多级目录已建：',os.path.isdir('./123/test/new/deep/dir'))
            #====== A.os.makedirs ======
            #123 已删除
            #多级目录已建： True

txt='./123/test/new/deep/dir \n this is a txt file\n'  #创建一个文件
with open('123.txt','w',encoding='utf-8') as f:
    f.write(txt)
shutil.copy2('123.txt','./123/test/new/deep/dir/123.txt') #复制内容 + 权限 + 元数据（mtime 等）,保留修改时间，适合备份/归档。
os.replace('123.txt','./123/test/new/deep/dir/456.txt')  #将文件移到另一个目录,目标存在 → 直接覆盖；不存在 → 正常移动

print('=====B.随机数据组合生成5个表格存到子目录123下面=====')
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


print('=====c.收集整理xlsx文件列出来=====')
folder='123'
targets=[] #存带路径的文件名列表
for root, dirs, files in os.walk(folder): #递归遍历目录树,返回三元组:当前目录，子目录列表，文件列表
    for name in files:  #name 为纯文件名，不包含路径，只有文件名本身（含扩展名）
        if os.path.splitext(name)[1]=='.xlsx':      #判断扩展名
            targets.append(os.path.join(root,name)) #收集所有.xlsx文件（将当前路径和其下的文件名串接起来，产生"路径 + 文件名

print(f'共找到{len(targets)}个xlsx文件')
for p in targets:  #打印出文件名（带当前路径）
    print(' ',p)

        #=====c.收集整理xlsx文件列出来=====
        #共找到5个xlsx文件
         #123\产品1.xlsx
         # 123\产品2.xlsx
         # 123\产品3.xlsx
         # 123\产品4.xlsx
         # 123\产品5.xlsx

print("========D. os.rename,COPY ==========")
for i,src in enumerate(targets,start=1): #对文件名列表进行枚举
    root,name=os.path.split(src)         #按最后一个路径分隔符拆，拆分目录和文件名
    stem,ext=os.path.splitext(name)      #按最后一个点 . 拆，拆文件名为前缀主名及后缀扩展名
    dst=os.path.join(root,f'{stem}_{i:04d}{ext}')  #命名加上i编号4位数，不足补0

    if not os.path.exists(dst): #安全检查，不存在目标文件名时，进行更名操作
        os.rename(src,dst)
        print(f'rename is ok : {src} to {dst}')
    else:
        print(f'SKIP！{dst} is exist')

        #========D. os.rename,COPY ==========
        #rename is ok : 123\产品1.xlsx to 123\产品1_0001.xlsx
        #rename is ok : 123\产品2.xlsx to 123\产品2_0002.xlsx
        #rename is ok : 123\产品3.xlsx to 123\产品3_0003.xlsx
        #rename is ok : 123\产品4.xlsx to 123\产品4_0004.xlsx
        #rename is ok : 123\产品5.xlsx to 123\产品5_0005.xlsx


print("=======E. os.walk,递归遍历目录树 ========")
for root, dirs, files in os.walk('./123'):
    print(f'  目录：{root}')
    print(f'      子目录：{dirs}')
    print(f'      文件名：{files}')

#        =======E. os.walk,递归遍历目录树 ========
#          目录：./123
#              子目录：['test']
#              文件名：['产品1_0001.xlsx', '产品2_0002.xlsx', '产品3_0003.xlsx', '产品4_0004.xlsx', '产品5_0005.xlsx']
#         目录：./123\test
#              子目录：['new']
#              文件名：[]
#          目录：./123\test\new
#              子目录：['deep']
#              文件名：[]
#          目录：./123\test\new\deep
#             子目录：['dir']
#              文件名：[]
#          目录：./123\test\new\deep\dir
#              子目录：[]
#              文件名：['123.txt', '456.txt']

from pathlib import Path  # 面向对象路径库
print("======= 用pathlib实现上面的功能========")

print('=========0.建立目录，由123-》456=========')
BASE = Path("456")   # ← 456目录
print(BASE,type(BASE))  #456 <class 'pathlib.WindowsPath'>
DEEP = BASE / "test" / "new" / "deep" / "dir"       # Path 用 / 拼多级路径
        #======= 用pathlib实现上面的功能========
        #=========0.建立目录，由123-》456=========
        #456 <class 'pathlib.WindowsPath'>

print('===========Path.mkdir===========')
if BASE.exists():
     shutil.rmtree(BASE) #若456已存在，整个删掉，避免多次运行该程序时文件越积越多
BASE.mkdir(parents=True,exist_ok=True)
DEEP.mkdir(parents=True,exist_ok=True)
print('多级目录已建：',DEEP.is_dir())
        #===========Path.mkdir===========
        #多级目录已建： True
print('================1.生成文件，复制，移动=================')
txt = "./456/test/new/deep/dir \n this is a txt file\n"
src_txt=Path(BASE/'123.txt') #创建"路径对象"（纯内存，不碰磁盘）
src_txt.write_text(txt,encoding='utf-8') #在磁盘上生成 456/123.txt，并写入内容

# 复制（pathlib 无复制函数，仍用 shutil；dst 可以是 Path 对象）
shutil.copy2(src_txt, DEEP/"123.txt")   #将123.txt复制到另一个目录
print("复制完成：", (DEEP/"123.txt").exists())

# 移动并覆盖（等价 os.replace）
src_txt.replace(DEEP/"456.txt")   #将123.txt移到新目录，并更名为456.txt
print("移动完成：", (DEEP/"456.txt").exists(), "原文件还在吗：", src_txt.exists())
            #================1.生成文件，复制，移动=================
            #复制完成： True
            #移动完成： True 原文件还在吗： False


print("===== 2.随机数据组合生成5个表格存到 456 下面 =====")
products = ["香蕉", "苹果", "桔子", "西瓜", "葡萄", "菠萝", "草莓", "芒果", "梨", "桃子"]
prices = [1, 2, 3, 4, 5]
quantities = [10, 20, 30, 40, 50, 60, 70, 80]
salesman = ["张三", "李四", "王五", "赵六"]
for i in range(1, 6):
    df = pd.DataFrame({
        "产品名称": random.choices(products, k=5),
        "产品价格": random.choices(prices, k=5),
        "产品数量": random.choices(quantities, k=5),
        "产品销售": random.choices(salesman, k=5),
    })
    out = BASE/f"产品{i}.xlsx"                    # Path 拼文件名(含路径）
    df.to_excel(out, index=False)
    print("  生成：", out)

                #===== 2.随机数据组合生成5个表格存到 456 下面 =====
                #  生成： 456\产品1.xlsx
                #  生成： 456\产品2.xlsx
                #  生成： 456\产品3.xlsx
                # 生成： 456\产品4.xlsx
                #  生成： 456\产品5.xlsx

print('# ========== 3. rglob 递归收集 .xlsx（等价 os.walk） ==========')
print("== Path.rglob ==")
targets = sorted(p for p in BASE.rglob("*.xlsx") if p.is_file()) #“把 BASE.rglob("*.xlsx") 里所有 p，只要 p.is_file() 为真，收集起来排个序，赋给 targets。”
    # rglob 递归匹配；sorted 保证顺序稳定
    #rglob = recursive glob，递归遍历 BASE 及其所有子目录。
    #返回一个生成器（Generator[Path]），逐个产出匹配 *.xlsx 的 Path 对象。
    #注意：rglob 匹配的是名字匹配 *.xlsx 的项，理论上包括文件，也可能包括名为 xx.xlsx 的目录（极少见），所以后面要过滤。
    #(p for p in BASE.rglob("*.xlsx") if p.is_file())这是生成器表达式（注意是圆括号，不是方括号）：
    #targets的类型是列表，
'''[
        Path('456/产品1.xlsx'),
        Path('456/产品2.xlsx'),
        Path('456/产品3.xlsx'),
        Path('456/产品4.xlsx'),
        Path('456/产品5.xlsx'),
]'''

print(f"共找到 {len(targets)} 个 xlsx 文件")
for p in targets:
    print("  ", p)

                    ## ========== 3. rglob 递归收集 .xlsx（等价 os.walk） ==========
                    #== Path.rglob ==
                    #共找到 5 个 xlsx 文件
                    #   456\产品1.xlsx
                    #   456\产品2.xlsx
                    #   456\产品3.xlsx
                    #   456\产品4.xlsx
                    #   456\产品5.xlsx

print('# ========== 4. 重命名：stem + 编号，保留 suffix ==========')
print("======== Path.rename ========")
for i, src in enumerate(targets, start=1):
    # with_name 换文件名；这里用 f-string 拼 新stem + 4位编号 + 原后缀
    new_name = f"{src.stem}_{i:04d}{src.suffix}" #stem 只取“文件名去掉扩展名”的部分，不含目录,suffix只取后缀
    dst = src.with_name(new_name)     # with_name 只替换"文件名"部分，父目录保持不变等价 os.path.join(src.parent, new_name)
    # 也可以用 with_stem（Python 3.9+）：src.with_stem(f"{src.stem}_{i:04d}")

            #src = Path('456/test/new/deep/dir/产品3.xlsx')
            #src.stem  # → '产品3'        ← 只有主名，不含目录，不含 .xlsx
            #src.name  # → '产品3.xlsx'   ← 文件名（含后缀），不含目录
            #src.suffix  # → '.xlsx'        ← 只有后缀
            #src.parent  # → Path('456/test/new/deep/dir')   ← 目录'''

    if not dst.exists():                            # 安全检查
        src.rename(dst)                             # 等价 os.rename
        print(f"rename is ok : {src} to {dst}")
    else:
        print(f"SKIP {dst} is exist")

                ## ========== 4. 重命名：stem + 编号，保留 suffix ==========
                #======== Path.rename ========
                #rename is ok : 456\产品1.xlsx to 456\产品1_0001.xlsx
                #rename is ok : 456\产品2.xlsx to 456\产品2_0002.xlsx
                #rename is ok : 456\产品3.xlsx to 456\产品3_0003.xlsx
                #rename is ok : 456\产品4.xlsx to 456\产品4_0004.xlsx
                #rename is ok : 456\产品5.xlsx to 456\产品5_0005.xlsx

print('========== 5. 递归遍历展示（等价 os.walk） ==========')
print("== Path.rglob 递归遍历目录树 ==")
for p in sorted(BASE.rglob("*")):  #rglob("*") 匹配 BASE 下所有条目（文件和目录，递归），每个 p 都是完整路径的 Path 对象,
                                   #sorted() 比较 Path 对象时，实际比较的是它们的字符串形式（Path.__lt__ 按路径字符串字典序比较）
    kind = "DIR " if p.is_dir() else "FILE"
                                    # 用相对路径显示层级，效果类似 os.walk 的 root/dirs/files
    print(f"  [{kind}] {p.relative_to(BASE.parent)}") #返回 p 相对于 BASE.parent 的路径，即去掉前面的 ./，显示成 456/... 开头
                                                        #BASE.parent = Path('.')（因为 BASE = Path("456")，其父是当前目录 .）
                                                       #relative_to 返回 p 相对于 BASE.parent 的路径，即去掉前面的 ./，显示成 456/... 开头。
# ========== 5. 递归遍历展示（等价 os.walk） ==========
#== Path.rglob 递归遍历目录树 ==
  #[DIR ] 456\test
  #[DIR ] 456\test\new
  #[DIR ] 456\test\new\deep
  #[DIR ] 456\test\new\deep\dir
  #[FILE] 456\test\new\deep\dir\123.txt
  #[FILE] 456\test\new\deep\dir\456.txt
  #[FILE] 456\产品1_0001.xlsx
  #[FILE] 456\产品2_0002.xlsx
  #[FILE] 456\产品3_0003.xlsx
  #[FILE] 456\产品4_0004.xlsx
  #[FILE] 456\产品5_0005.xlsx