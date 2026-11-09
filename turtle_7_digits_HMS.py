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

def drawdate(date): #获取日期

    for i in date:
        if i =='-':
            turtle.pencolor('green')
            turtle.write(':',font=('Arial',18,'normal'))
            turtle.fd(40)
        elif i =='=':
            turtle.pencolor('blue')
            turtle.write(':',font=('Arial',18,'normal'))
            turtle.fd(40)
        #elif i =='+':
        #    turtle.pencolor('black')
        #    turtle.write(':',font=('Arial',18,'normal'))

        else:
            turtle.pencolor('red')
            drawdigit(eval(i)) #将i转换成整数

def main():
    turtle.setup(530,200,50,50)
    turtle.penup()
    turtle.speed(0)
    #turtle.fd(-245)
    turtle.pensize(5)
    turtle.tracer(0)
    turtle.hideturtle()
    while(True):
        turtle.clear()
        turtle.penup()
        turtle.goto(-245,0)
        turtle.seth(0)
        drawdate(time.strftime("%H-%M=%S",time.localtime()))
        turtle.update()
        time.sleep(1)


main()



