import turtle
import time
def drawgap(): #字段间留点间隙
    turtle.penup()
    turtle.fd(5)
def drawline(draw): #线（单段管）绘制
    drawgap()
    turtle.pendown() if draw else turtle.penup() #True时落笔画线段，False时提笔不画，只走线路
    turtle.fd(40)
    drawgap()
    turtle.right(90)

def drawdigit(digit): #根据数字绘制七段数码管
    drawline(True) if digit in [2,3,4,5,6,8,9] else drawline(False)
    drawline(True) if digit in [0,1,3,4,5,6,7,8,9] else drawline(False)
    drawline(True) if digit in [0,2,3,5,6,8,9] else drawline(False)
    drawline(True) if digit in [0,2,6,8] else drawline(False)
    turtle.left(90)
    drawline(True) if digit in [0,4,5,6,8,9] else drawline(False)
    drawline(True) if digit in [0,2,3,5,6,7,8,9] else drawline(False)
    drawline(True) if digit in [0,1,2,3,4,7,8,9] else drawline(False)
    turtle.left(180) #方向调到X正方向
    turtle.penup()  #抬笔
    turtle.fd(20)   #向前20，为画下一个7段字符做准备

def drawstr(string): #获取日期
        for char in string:
            if char == ':':
                turtle.pencolor('green')
                turtle.write(':', font=('Arial', 32, 'normal'))
                turtle.fd(40)
            else:
                turtle.pencolor('red')
                drawdigit(eval(char))  # 将char转换成整数


def main():
    seconds= int(input('enter seconds for  countdown:\n'))
    turtle.setup(400,200,900,50)
    turtle.speed(0)
    turtle.pensize(5)
    turtle.color('red')
    turtle.tracer(0)
    turtle.hideturtle()
    while seconds >=0:
            turtle.clear()
            turtle.penup()
            turtle.goto(-140, 0)
            turtle.seth(0)
            minutes = seconds // 60
            sec = seconds % 60
            drawstr(f"{minutes:02d}:{sec:02d}")
            turtle.update()
            time.sleep(1)
            seconds -= 1
    turtle.done()




main()



