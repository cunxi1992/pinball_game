# -*- coding: utf-8 -*-
import tkinter as tkinter
import tkinter.messagebox as mb
import random,time

'''
欢迎关注 微信公众号菜鸟学Python
更多好玩有趣的实战项目
'''

class Ball():
    '''
    创建Ball类，初始化对象，即创建对象设置属性,
    init函数是在对象被创建的同时就设置属性的一种方法，Python会在创建新对象时自动调用这个函数。
    '''

    def __init__(self,canvas,paddle,score,color,init_x=100,init_y=100):
        '''
        Ball类初始化属性
        :param canvas:画布
        :param paddle:球拍
        :param score:得分
        :param color:小球的颜色
        :param init_x:小球球的初始横坐标，有默认值，可不传
        :param init_y:小球球的初始纵坐标，有默认值，可不传
        '''
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.color = color

        # 保存tkinter画小球返回的id，为后期移动屏幕上的小球做准备，
        # 参数分别表示为:(10,10)表示左上角x,y坐标，(30,30)表示右下角x,y坐标，即创建一个直径为20的圆
        # fill为小球的填充色
        self.id = canvas.create_oval(10,10,30,30,fill=self.color)
        # 将小球移动到初始位置，初始位置可通过传参进行更改，有默认值
        self.canvas.move(self.id,init_x,init_y)

        # 给一串x分量的起始值（x和y代表横坐标和纵坐标的分量）
        starts = [-3,-2,-1,1,2,3]
        # shuffle() 方法将序列的所有元素随机排序
        random.shuffle(starts)
        # 随机混排序，赋值给对象变量x，让它起始的时候获得随机分量值，引起球每次起始角度都不同
        self.x = starts[0]
        # 对象变量y就是垂直分量移动的初始值，等价于上下移动，值代表移动多少像素点
        self.y = -3

        # winfo_height()函数来获取画布当前的高度，赋值给对象变量
        self.canvas_height = self.canvas.winfo_height()
        # winfo_width()函数来获取画布当前的宽度，赋值给对象变量
        self.canvas_width = self.canvas.winfo_width()
        # 小球是否碰触到画布底部，初始值为False，即没有碰到
        self.hit_bottom = False


    def draw(self):
        '''
        该函数用于让小球水平和垂直运动，在运动的过程中，判断是否得分、游戏是否结束
        '''
        # 让小球可以水平和垂直运动
        self.canvas.move(self.id,self.x,self.y)
        # coords函数通过id返回画布球的坐标列表（两个坐标，左上角的坐标和右下角的两个坐标）
        position = self.canvas.coords(self.id)
        # 判断小球是否撞到画布顶部或者底部，保证小球反弹回去，不消失
        if position[1] <= 0: # 如果小球的左上角y坐标小于0，则向下移动3个像素
            self.y = 3
        if position[3] >= self.canvas_height: # 如果小球的右下角y坐标大于画布宽度，则表示小球碰到了画布底部，游戏结束
            self.hit_bottom = True
        if self.hit_paddle(position) == True: # 判断 球 是否碰到了 球拍，如果碰到了则使小球回弹
            self.y = -3
        if position[0] <= 0: # 如果小球的左上角x坐标 小于等于0，则向右移动3个像素
            self.x = 3
        if position[2] >= self.canvas_width: # 如果小球的右下角x坐标 大于等于画布宽度，则向左移动3个像素
            self.x = -3


    def hit_paddle(self,position):
        '''
        该函数用于判断 球 是否碰到了 球拍，如果碰到了则使小球回弹，否则游戏结束
        :param position:小球的坐标
        '''
        # 获取球拍在画布的坐标，返回一个数组（两个坐标，左上角的坐标和右下角的两个坐标）
        paddle_position = self.canvas.coords(self.paddle.id)
        print ('paddle_position:',paddle_position[0],paddle_position[1],paddle_position[2],paddle_position[3])
        # 如果小球的右下角x坐标 大于等于 球拍左上角x坐标，且小球左上角x坐标 小于等于 球拍右下角x坐标
        if position[2] >= paddle_position[0] and position[0] <= paddle_position[2]:
            # 如果小球右下角y坐标 大于等于 球拍左上角y坐标，且小球右下角y坐标 小于等于 球拍右下角坐标
           if position[3] >= paddle_position[1] and position[3] <= paddle_position[3]:
                # 横坐标 等于
               self.x += self.paddle.x
               colors = ['red','green']
               # shuffle() 方法将序列的所有元素随机排序，以便随机获得小球颜色
               random.shuffle(colors)
               self.color= colors[0]
               #
               self.canvas.itemconfig(self.id,fill=colors[0])
               # 计算得分并展示，且同时将小球的颜色、关卡颜色同步
               self.score.hit(ball_color = self.color)
               self.canvas.itemconfig(self.paddle.id,fill=self.color)
               # 增加或减少球拍的宽度
               self.adjust_paddle(paddle_position)
               return True

        return False


    def adjust_paddle(self,paddle_position):
        '''
        该函数用于增加或减少球拍的宽度
        :paddle_position:球拍的位置坐标
        '''
        # 球拍每次的增量大小
        paddle_grow_length = 30
        # 球拍的宽度 = 球拍的右下角x坐标 - 球拍的左上角x坐标
        paddle_width = paddle_position[2] - paddle_position[0]
        if self.color == 'red': # 如果当前球的颜色为红色
            if paddle_width > 30: # 如果球拍的宽度大于60
                if paddle_position[2] >= self.canvas_width: # 如果球拍右下角的x坐标 大于等于 画布宽度
                    # 球拍右下角x坐标 = 球拍右下角x坐标 - 增量值
                    paddle_position[2] = paddle_position[2] - paddle_grow_length
                else:
                    # 球拍的左上角x坐标 = 球拍的左上角x坐标 + 增量值
                    paddle_position[0] = paddle_position[0] + paddle_grow_length

        elif self.color == 'green': # 如果当前球的颜色为绿色
            if paddle_width < 300: # 如果球拍的宽度小于300
                if paddle_position[2] >= self.canvas_width: # 如果球拍的右下角x坐标 大于等于 画布宽度
                    # 球拍左上角x坐标 - 增量值
                    paddle_position[0] = paddle_position[0] - paddle_grow_length
                else:
                    # 球拍右下角x坐标 + 增量值
                    paddle_position[2]=paddle_position[2]+paddle_grow_length


class Paddle:
    '''
    球拍类
    '''
    def __init__(self,canvas,color):
        '''
        :param canvas:画布
        :param color:球拍的颜色
        '''
        self.canvas = canvas
        # winfo_width()函数来获取画布当前的宽度，赋值给对象变量
        self.canvas_width = self.canvas.winfo_width()
        # winfo_height()函数来获取画布当前的高度，赋值给对象变量
        self.canvas_height = self.canvas.winfo_height()
        # 保存tkinter画球拍时返回的id，为后期移动屏幕上的球拍做准备，
        # create_rectangle 画矩形，fill为球拍的颜色
        self.id = canvas.create_rectangle(0,0,180,15,fill=color)
        # 将球拍移动至初始位置
        self.canvas.move(self.id,200,self.canvas_height*0.75)
        # 设置对象变量x，初始值为0.也就是球拍先不移动
        self.x = 0
        # 游戏是否开始，默认为Flase，即 不开始
        self.started = False
        # 是否继续游戏，默认值为 否
        self.continue_game = False
        # 初始化时将事件‘按下左键’和函数向左移动绑定
        self.canvas.bind_all('<KeyPress-Left>',self.turn_left)
        # 初始化时将事件‘按下右键’和函数向右移动绑定
        self.canvas.bind_all('<KeyPress-Right>',self.turn_right)
        # 初始化时将事件‘按下Enter键’和函数继续游戏绑定
        self.canvas.bind_all('<KeyPress-Enter>',self.continue_game)
        # 按任意键开始游戏
        self.canvas.bind_all('<Button-1>',self.start_game)
        # 初始化时将事件‘按下space键’和函数暂停游戏绑定
        self.canvas.bind_all('<space>',self.pause_game)

    def turn_left(self,event):
        '''
        该函数用于向左移动时，
        '''
        # 获取球拍的位置坐标
        position = self.canvas.coords(self.id)
        # 如果球拍的左上角x坐标 小于 0
        if position[0] <= 0:
            # 则再次按向左移动时，移动距离为0
            self.x = 0
        else:
            # 每次向左移动3个像素
            self.x = -3

    def turn_right(self,event):

        # 获取球拍的位置坐标
        position = self.canvas.coords(self.id)
        # 如果球拍的右下角x坐标 大于等于 画布宽度
        if position[2] >= self.canvas_width:
            # 则再次按向右移动时，移动距离为0
            self.x = 0
        else:
            # 每次向右移动3个像素
            self.x = 3

    def start_game(self,evt):
        self.started = True

    def pause_game(self,evt):
        if self.started:
            self.started=False
        else:
            self.started=True

    def draw(self):
        '''
        该函数用于移动球拍
        '''
        # 球拍类可以水平移动
        self.canvas.move(self.id,self.x,0)
        # 获取球拍的位置坐标
        position = self.canvas.coords(self.id)
        # 如果球拍左上角x坐标小于等于0，则停止移动
        if position[0] <= 0:
            self.x = 0
        # 如果球拍右下角x坐标大于等于0，则停止移动
        elif position[2] >= self.canvas_width:
            self.x = 0


class Score():
    '''
    得分类
    '''
    def __init__(self,canvas,color):
        '''
        初始化得分类
        :param canvas:画布
        :param color:得分文本的颜色
        '''
        # 初始化得分为0
        self.score = 0
        # 把参数canvas赋值给对象变量canvas
        self.canvas = canvas
        # winfo_width()函数来获取画布当前的宽度，赋值给对象变量
        self.canvas_width = self.canvas.winfo_width()
        # winfo_height()函数来获取画布当前的高度，赋值给对象变量
        self.canvas_height = self.canvas.winfo_height()
        # 创建文本控件，用户保存用户保存得分
        self.id = canvas.create_text(self.canvas_width-150,10,text='score:0',fill=color,font=(None, 18, "bold"))
        # 用户保存游戏的关卡颜色
        self.note = canvas.create_text(self.canvas_width-70,10,text='--',fill='red',font=(None, 18, "bold"))

    def hit(self,ball_color='grey'):
        '''
        该函数用于将计算得分并展示，且同时将小球的颜色、关卡颜色同步
        :param ball_color:小球的颜色，默认为'grey'
        '''
        # 得分递增
        self.score += 1
        # 将得分展示在文本控件中
        self.canvas.itemconfig(self.id,text='score:{}'.format(self.score))
        # 将小球的颜色同步至游戏关卡的颜色
        if ball_color == 'red':
            self.canvas.itemconfig(self.note,text='{}-'.format('W'),fill='red')
        elif ball_color=='green':
            self.canvas.itemconfig(self.note,text='{}+'.format('W'),fill='green')
        else:
            self.canvas.itemconfig(self.note,text='--',fill='grey')

def main():
    # tkinter.Tk()类创建一个tk对象，它就是一个基本窗口，可以在其上增加其他东西
    tk = tkinter.Tk()
    # call back for Quit
    def callback():
        '''
        该函数用于，当点击窗口 关闭 按钮时，展示一个消息提示框，询问是否要关闭，
        点击 是，则退出窗口
        '''
        if mb.askokcancel("Quit", "Do you really wish to quit?"):
            # Ball.flag = False
            tk.destroy()
    # 使用protocol将 WM_DELETE_WINDOW 与 callback 绑定,程序在退出时打印 'WM_DELETE_WINDOW'
    tk.protocol("WM_DELETE_WINDOW", callback)

    # 画布的宽
    canvas_width = 600
    # 画布的高
    canvas_hight = 500
    # 窗口标题
    tk.title("Ball Game V1.2")
    # 窗口不可被拉伸,(0,0)的意思是“窗口的大小在水平方向上和垂直方向上都不能改变”
    tk.resizable(0,0)
    # 调用wm_attributes，将窗口始终放到所有其他窗口之前（-topmost）,将1改为0画布窗口不在其他窗口之前
    tk.wm_attributes("-topmost",1)
    # 创建画布,bd=0,highlightthickness=0 作用是画布之外没有边框，可以使游戏屏幕看上去更加美观。最后一个bd是画布的背景色。
    canvas = tkinter.Canvas(tk,width=canvas_width,height=canvas_hight,bd=0,highlightthickness=0,bg='#00ffff')
    # 按照上面一行指定的宽度高度参数调整其自身大小
    canvas.pack()
    # update强制更新屏幕，实时更新画布
    tk.update()

    # 创建得分类，得分控件的颜色为红色
    score = Score(canvas,'red')
    # 创建 球拍类，
    paddle = Paddle(canvas,"red")
    # 创建 小球类，小球的默认颜色为灰色
    ball = Ball(canvas,paddle,score,"grey")

    # 游戏结束时的提示
    game_over_text = canvas.create_text(canvas_width/2,canvas_hight/2,text='Game over',state='hidden',fill='red',font=(None, 18, "bold"))
    # 游戏开始时的提示
    introduce = 'Welcome to Ball GameV1.2:\nClick Any Key--Start\nStop--Enter\nContinue-Enter\n'
    game_start_text = canvas.create_text(canvas_width/2,canvas_hight/2,text=introduce,state='normal',fill='magenta',font=(None, 18, "bold"))

    # 主循环，让tkinter不停地重画屏幕
    while True:
        # 如果小球没有碰到了底部，且 游戏尚未开始
        if (ball.hit_bottom == False) and ball.paddle.started:
            canvas.itemconfig(game_start_text,state='hidden')
            ball.draw()
            paddle.draw()
        # 如果小球碰到了底部，则游戏结束
        if ball.hit_bottom == True:
            time.sleep(0.1)
            canvas.itemconfig(game_over_text,state='normal')
        # 不停的刷新画布
        tk.update_idletasks()
        # 强制更新屏幕
        tk.update()
        time.sleep(0.01)

if __name__=='__main__':
    main()




