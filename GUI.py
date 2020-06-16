#
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from models import *
# from tkinter import *
from functools import partial  # for mouse events
from PIL import ImageTk, Image
from sqlite3 import *
import requests
import json  # for location
import smtplib  # for email
from email.mime.text import MIMEText
from email.header import Header
import math
from datetime import datetime

# 定义主界面大小
WIDTH = 1366
HEIGHT = 885

# 定义程序的名称
title = 'Heavenly Pizza GUI Ordering System'
# 定义一组颜色样式
color = {
    'bg': 'linen',
    'success': 'green4',
    'info': 'ivory2',
    'primary': 'deep sky blue',
    'error': 'tomato',
    'warning': 'orange'
}
# 定义用户找回密码配置的邮箱
mail = {
    'account': 'carol.chen.cn@outlook.com',
    'password': '1qazxsw23edc',
    'port': 587,
    'host': 'smtp.office365.com'
}
# 配置当前货币单位
money = '$'

# 定义购物车允许购买最多的Pizza个数
max_cart_item = 5
# 定义全部订单
orders = []
# 快递费
delivery_fee = 10
# 主程序初始化
s = Tk()
s.title(title)
s.geometry('{}x{}'.format(WIDTH,HEIGHT))
# 禁止用户调整窗体大小
s.resizable(0, 0)

# 读取Pizza数据，转为Pizza对象
pizzas = [Pizza(p['id'],p['name'],p['type'],p['img'],p['price'],p['content']) for p in pizzas_data]

class Main:
    def __init__(self):
        # 连接本地sqlite3数据库
        self.c = connect("mydata.db")
        self.cur = self.c.cursor()
        try:
            # 创建表 staff
            self.cur.execute("create table staff(name varchar(50),user varchar(50),passw varchar(50),email varchar(50))")
        except:
            pass
        
        # It keeps all the widgets & destroys them whenever user moves to a new window
        self.l = []  
        
        self.scr = s
        self.scr.configure(bg='white')
        self.f = Frame(self.scr, bg='white')
        self.f.place(x=0, y=0, width=WIDTH, height=HEIGHT)

        # 初始化购物车内Pizza个数
        self.ITEMS = 0
        self.TOTAL = 0
        # 定义每个Pizza 购买数量，为购物车最终结算使用
        self.user_cart = {p.id: StringVar() for p in pizzas}
        # 定义购物车里的每个Pizza的具体条目信息，比如买的哪个Pizza, 数量是多少，价格是多少
        self.items = {p.id: None for p in pizzas}
        # 定义结算页面的总价
        self.total_price = None
        # self.ids = []
        # 初始设置购物车中的Pizza对应数量都是0
        for uc in self.user_cart: self.user_cart[uc].set(0)
        # 默认进入登录页面
        self.login()
        # 窗体主函数运行
        self.scr.mainloop()


    def login(self):
        '''
        [登录界面] 
        -------------------------------------------------
        登录界面，程序运行的时候调用，包括账号、密码，登录按钮
        用户点击 [Sign in] 后进入主界面，如果没有账户，点击 
        [Sign up] 进入注册账号界面
        '''
        self.flush()
        self.f.config(bg=color['bg'])

        #   CANVAS  for image
        self.canvas = Canvas(self.f, bg=color['bg'], bd=-2)
        # previous height=125
        self.canvas.place(x=0, y=0, width=WIDTH, height=HEIGHT)
        # self.img=ImageTk.PhotoImage(Image.open('img/background_.jpg'))
        # self.canvas.create_image(681,405,image=self.img)
        self.l.append(self.canvas)

        #   USERNAME label
        self.title = Label(
            self.f, 
            bg=color['bg'], 
            text='Sign in {}'.format(title), 
            padx=10, 
            anchor='center', 
            font=('Georgia 14 bold')
        )
        self.title.place(x=WIDTH/2 - 200, y=50, width=600, height=25)
        self.l.append(self.title)

        #   USERNAME label
        self.username = Label(
            self.f,
            bg=color['bg'],
            text='Username',
            padx=10,
            anchor='e')
        self.username.place(
            x=WIDTH/2 - 110,
            y=130,
            width=110,
            height=25)
        self.l.append(self.username)

        # 存储用户名和密码的变量
        eu = StringVar()
        ep = StringVar()

        self.un_entry = Entry(
            self.f,
            textvariable=eu,
            bg='azure',
            justify='center'
        )
        self.un_entry.place(x=WIDTH/2, y=130, width=200, height=25)
        self.l.append(self.un_entry)
        # eu.set('1')

        #   PASSWORD label
        self.passw = Label(
            self.f, 
            bg=color['bg'], 
            text='Password', 
            padx=10,  
            anchor='e'
        )
        self.passw.place(x=WIDTH/2 - 110, y=175, width=110, height=25)
        self.l.append(self.passw)

        # PASSWORD entry_field
        self.p_entry = Entry(
            self.f,
            show="*",
            textvariable=ep,
            bg='azure',
            justify='center'
        )
        self.p_entry.place(x=WIDTH/2, y=175, width=200, height=25)
        self.l.append(self.p_entry)
        # ep.set('1')

        # 去注册按钮
        self.r = Button(
            self.f, 
            bg=color['info'], 
            text='Create an account >>', 
            command=self.register
        )
        self.r.place(x=WIDTH/2 - 100, y=270, width=150, height=28)
        self.l.append(self.r)

        # 登录按钮
        self.submit = Button(
            self.f,
            bg=color['success'],
            fg='snow',
            text='Sign in',
            command=lambda: self.result("login")
        )
        self.submit.place(x=WIDTH/2 + 100, y=270, width=100, height=28)
        self.l.append(self.submit)


    def register(self):
        '''
        @description:   [注册界面] 
                        用户点击登录界面的 [Sign up] 的时候调用，包括账号、
                        密码，邮箱等，用户点击 [Sign up] 后进入 登录界面，
                        如果已有账户，点击 [Sign in] 进入登录界面
        @param : 
        @return: 
        '''

        self.flush()
        self.f.config(bg=color['bg'])
        #   CANVAS  for image
        self.canvas = Canvas(self.f, bg=color['bg'], bd=-2)
        # previous height=125
        self.canvas.place(x=0, y=0, width=WIDTH, height=HEIGHT)
        # self.img=ImageTk.PhotoImage(Image.open('img/background.jpg'))
        # self.canvas.create_image(681,405,image=self.img)
        self.l.append(self.canvas)

        #   USERNAME label
        self.title = Label(
            self.f, 
            bg=color['bg'], 
            text='Sign up ' +
            title, 
            padx=10, 
            anchor='center', 
            font=('Georgia 14 bold')
        )
        self.title.place(x=WIDTH/2 - 200, y=50, width=600, height=25)
        self.l.append(self.title)

        #   NAME label
        self.Name = Label(
            self.f, 
            bg=color['bg'], 
            text='Name', 
            padx=10, anchor='e'
        )
        self.Name.place(x=WIDTH/2 - 110, y=100, width=110, height=25)
        self.l.append(self.Name)

        #   NAME entry
        self.N_entry = Entry(self.f)
        self.N_entry.place(x=WIDTH/2, y=100, width=200, height=25)
        self.l.append(self.N_entry)

        #   USERNAME label
        self.name = Label(
            self.f, 
            bg=color['bg'], 
            text='Userame', 
            padx=10, 
            anchor='e'
        )
        self.name.place(x=WIDTH/2 - 110, y=140, width=110, height=25)
        self.l.append(self.name)

        #  USERNAME entry_field
        self.n_entry = Entry(self.f)
        self.n_entry.place(x=WIDTH/2, y=140, width=200, height=25)
        self.l.append(self.n_entry)

        #   PASSWORD label
        self.plabel = Label(
            self.f, 
            bg=color['bg'], 
            text='Password', 
            padx=10, 
            anchor='e'
        )
        self.plabel.place(x=WIDTH/2 - 110, y=180, width=110, height=25)
        self.l.append(self.plabel)

        #   PASSWORD entry_field
        self.p_entry = Entry(self.f, show="*")
        self.p_entry.place(x=WIDTH/2, y=180, width=200, height=25)
        self.l.append(self.p_entry)

        #   PASSWORD2 label
        self.plabel2 = Label(
            self.f, 
            bg=color['bg'], 
            text='Retype password', 
            padx=10, 
            anchor='e'
        )
        self.plabel2.place(x=WIDTH/2 - 140, y=220, width=140, height=25)
        self.l.append(self.plabel2)

        #   PASSWORD entry_field
        self.p_entry2 = Entry(self.f, show="*")
        self.p_entry2.place(x=WIDTH/2, y=220, width=200, height=25)
        self.l.append(self.p_entry2)

        #   Email field
        self.e_mail = Label(
            self.f, 
            bg=color['bg'], 
            text="Your email", 
            padx=10, 
            anchor='e'
        )
        self.e_mail.place(x=WIDTH/2 - 110, y=260, width=110, height=25)
        self.l.append(self.e_mail)

        #   Email entry_field
        self.e_entry = Entry(self.f)
        self.e_entry.place(x=WIDTH/2, y=260, width=200, height=25)
        self.l.append(self.e_entry)

        #   REGISTER button
        self.rbutton = Button(
            self.f, 
            bg=color['success'], 
            fg='snow', 
            text='Sign up', 
            command=lambda: self.result("register")
        )
        self.rbutton.place(x=WIDTH/2 + 90, y=320, width=110, height=31)
        self.l.append(self.rbutton)

        # 返回登录按钮
        self.r = Button(
            self.f, 
            bg=color['info'], 
            text='<< Back to Sign in', 
            command=self.login
        )
        self.r.place(x=WIDTH/2 - 100, y=320, width=130, height=31)
        self.l.append(self.r)
        self.scr.mainloop()

    def flush(self):
        '''
        @description: destroys all the widgets of the frame 
        @param : 
        @return: 
        '''
        for i in self.l:
            i.destroy()

    def result(self, val):
        if val == "login":
            if not len(self.un_entry.get()) or not len(self.p_entry.get()):  # login details not given
                messagebox.showinfo(
                    "Invalid credentials", "Please fill both the fields to continue.\nPlease try again.")
            else:  # check for correct username
                x = self.cur.execute(
                    "select count(*) from staff where user=%r" % (self.un_entry.get()))
                if list(x)[0][0] == 0:  # entered username doesn't exist
                    messagebox.showinfo(
                        "Invalid credentials.", 
                        "Username %r doesn't exist.\nPlease 'register' to continue." % (
                        self.un_entry.get()))  # wrong username
                    self.__init__()
                else:  # username exists, check for correct password now
                    self.mail = list(self.cur.execute(
                        "select email from staff where user=%r" % (self.un_entry.get())))[0][0]
                    self.NAME = list(self.cur.execute(
                        "select name from staff where user=%r" % (self.un_entry.get())))[0][0]
                    print(self.NAME)
                    # checking for correct password
                    x = self.cur.execute(
                        "select count(*) from staff where passw=%r" % (self.p_entry.get()))
                    # correct password, grant access to order.
                    if list(x)[0][0]:
                        self.show_regular_pizzas()
                    else:                  # wrong password
                        messagebox.showinfo(
                            "Wrong password", "Please enter a valid password\nForgot password ?")
                        self.rbutton = Button(
                            self.scr, text='Recover my password', command=self.recover_password, padx=10, anchor='center', relief=FLAT, bg=color['warning'])
                        self.rbutton.place(
                            x=WIDTH/2, y=220, width=150, height=30)
                        self.l.append(self.rbutton)
        elif val == "register":
            if not len(self.n_entry.get()) or not len(self.N_entry.get()) or not len(self.p_entry.get()) or not len(self.p_entry2.get()) or not len(self.e_entry.get()):  # no username given
                messagebox.showinfo("Missing details",
                                    "Please fill all the fields to continue.")
            else:  # check for validity of data
                # both passwords are same,check for availability of username.
                if self.p_entry.get() == self.p_entry2.get():
                    if re.search(r'\w+@+\w+.+\w', self.e_entry.get()):
                        x = self.cur.execute(
                            "select count(*) from staff where user=%r" % (self.n_entry.get()))
                        if list(x)[0][0] != 0:   # username already taken.
                            messagebox.showinfo(
                                "Oops !", "Username %r already exists.\nPlease try another one." % (self.n_entry.get()))
                        else:                   # username available.
                            try:
                                self.cur.execute("insert into staff values(%r,%r,%r,%r)" % (
                                    self.N_entry.get(), self.n_entry.get(), self.p_entry2.get(), self.e_entry.get()))
                                self.c.commit()
                                messagebox.showinfo(
                                    "Info", "You've been successelfully registered\nRedirecting to LOGIN window")
                                self.flush()
                                self.__init__()  # registration done.... redirect to 'login' window
                            except:
                                pass
                    else:
                        messagebox.showinfo("Oops !", "invalid email")
                else:  # passwords aren't same...reconstruct the 'register' window
                    messagebox.showinfo(
                        "Mismatched passwords", "Both passwords should be same\nPlease try again.")

    def recover_password(self):
        ''' 给邮箱发送一封邮件，内容是对应账号的密码
        '''
        try:
            self.rbutton.destroy()
        except:
            self.rbutton.destroy()
        try:
            mail = list(self.cur.execute("select email from staff where user=%r and name=%r" % (
                self.un_entry.get(), self.NAME)))[0][0]
            print('email id is ', mail)
            self.mail = mail
            password = list(self.cur.execute(
                "select passw from staff where name=%r" % (self.NAME)))[0][0]
            server = smtplib.SMTP(mail['host'], mail['port'])
            server.starttls()
            print('connected to outlook')
            server.login(mail['account'], mail['password'])
            print('logged in')

            receivers = [mail]
            Subject = 'Recover password for %s' % title
            Content = 'Hello '+self.NAME+',\n\nYour password for '+title+' is '+''+password+''
            msg = MIMEText(Content, 'plain', 'utf-8')
            # msg['From'] = Header(mail['account'], 'utf-8')
            msg['To'] = Header('', 'utf-8')
            msg['Subject'] = Header(Subject, 'utf-8')
            print(msg)
            server.sendmail(mail['account'], receivers, msg.as_string())

            print('mail sent')
            server.close()
            messagebox.showinfo('Info', 'Dear '+self.NAME+', your password has been sent to ' +
                                mail+'\nPlease try again using the correct password.')
        except smtplib.SMTPException as e:
            print(e)
            messagebox.showinfo(
                'Erro', "Your password couldn't be sent. Please check your internet connection.")
        self.flush()
        self.__init__()

    def myfunction(self, event):
        # 'width' & 'height' are actual scrollable frame size.
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all"), width=WIDTH-20, height=HEIGHT-80
        )

    def entry(self, wel, color, event):                          # <<<<<< HOVERING >>>>>>
        self.wel.configure(background=color, foreground='white')

    def exit_(self, wel, color, event):
        self.wel.configure(background=color, foreground='red')

    def entryP(self, pizza_label, color, event):
        self.pizza_label.configure(background=color, foreground='white')

    def exitP(self, pizza_label, color, event):
        self.pizza_label.configure(background=color, foreground='white')

    def entryM(self, meals_label, color, event):
        self.meals_label.configure(background=color, foreground='white')

    def exitM(self, meals_label, color, event):
        self.meals_label.configure(background=color, foreground='white')

    def entryC(self, pay, color, event):
        self.pay.configure(background=color, foreground='white')

    def exitC(self, pay, color, event):
        self.pay.configure(background=color, foreground='medium aquamarine')

    def logout(self):
        ''' 注销 '''
        self.head.destroy()
        self.login()

    def create_header(self):
        ''' 创建固定头部 '''
        self.f = Frame(self.scr, relief=FLAT, bd=-2)
        self.f.place(x=0, y=60)

        self.canvas = Canvas(self.f, bd=-2)
        self.frame = Frame(self.canvas, bd=-2, bg='white')
        self.myscrollbar = Scrollbar(
            self.f, 
            orient=VERTICAL, 
            command=self.canvas.yview
        )  # SCROLL BAR   ####
        self.canvas.configure(yscrollcommand=self.myscrollbar.set)
        self.myscrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.pack(side=LEFT)
        self.canvas.create_window((0, 0), window=self.frame)
        self.frame.bind("<Configure>", self.myfunction)

        # 建立顶部菜单栏
        self.head = Canvas(self.scr, bd=-2, bg='white')  # head canvas
        self.head.place(x=0, y=0, width=WIDTH, height=60)
        self.l.append(self.head)

        # 常规 Pizza
        self.pizza_label = Label(
            self.head, text='Regular pizzas', bg='red', fg='snow', font=('Helvetica 12 bold'))
        self.pizza_label.place(x=5, y=4, width=150, height=44)
        self.pizza_label.bind(
            '<Button-1>', lambda val='1': self.show_regular_pizzas())
        self.pizza_label.bind('<Enter>', partial(
            self.entryP, self.pizza_label, 'coral'))
        self.pizza_label.bind('<Leave>', partial(
            self.exitP, self.pizza_label, 'red'))
        self.l.append(self.pizza_label)

        # 精品 Pizza
        self.meals_label = Label(
            self.scr, 
            text='Gourmet pizzas',
            bg='red', 
            fg='snow', 
            padx=10, 
            font=('Helvetica 12 bold')
        )
        self.meals_label.place(x=165, y=4, width=150, height=44)
        self.meals_label.bind(
            '<Button-1>', lambda val='1': self.show_gourmet_pizzas())
        self.meals_label.bind('<Enter>', partial(
            self.entryM, self.meals_label, 'coral'))
        self.meals_label.bind('<Leave>', partial(
            self.exitM, self.meals_label, 'red'))
        self.l.append(self.meals_label)

        # 欢迎
        self.wel = Label(
            self.head,
            text='Welcome, '+self.NAME,
            fg='red',
            bg='white',
            font=('Serif 12 bold')
        )

        self.wel.place(x=325, y=4, width=200, height=44)
        self.wel.bind('<Enter>', partial(self.entry, self.wel, 'red'))
        self.wel.bind('<Leave>', partial(self.exit_, self.wel, 'white'))
        self.l.append(self.wel)
        # self.head.create_rectangle(5, 3, 106, 54, outline='red', fill='white')

        # Orders
        self.logout_btn = Button(
            self.scr,
            text='Orders',
            relief=FLAT,
            font=('Serif 12 bold'),
            bg='snow',
            fg=color['error'],
            command=self.orders
        )
        self.logout_btn.place(x=535, y=4, width=90, height=44)
        self.l.append(self.logout_btn)

        #   Logout button
        self.logout_btn = Button(
            self.scr,
            text='Logout',
            relief=FLAT,
            font=('Serif 12 bold'),
            bg='snow',
            fg=color['error'],
            command=self.logout
        )
        self.logout_btn.place(x=635, y=4, width=90, height=44)
        self.l.append(self.logout_btn)

        # 头部右侧购物车
        self.pay = Label(
            self.scr,
            text='Checkout',
            fg='medium aquamarine',
            bg='snow',
            font=('Sans 12 bold')
        )
        self.pay.place(x=985, y=8, height=42, width=100)
        self.pay.bind(
            '<Button-1>',
            partial(self.payment_window, '1')
        )
        self.pay.bind(
            '<Enter>',
            partial(self.entryC, self.pay, 'medium aquamarine')
        )
        self.pay.bind(
            '<Leave>',
            partial(self.exitC, self.pay, 'white')
        )
        self.l.append(self.pay)

        self.head.create_rectangle(
            984, 7, 1085, 50, 
            fill='white', outline='medium aquamarine'
        )

        # 购物车小图片
        self.cart = PhotoImage(file='img/cart2.png')  # cart logo ##
        self.head.create_image(1140, 33, image=self.cart)
        # self.l.append(self.cart)

        # 购物车里有几件Pizza
        self.tl2 = Label(
            self.head, 
            bg=color['error'], 
            fg='snow',
            text=self.ITEMS, 
            font=('Sans 10 bold')
        )  # NO OF ITEMS ##
        self.tl2.place(x=1141, y=8, width=17, height=15)
        self.head.create_oval(
            1137, 5, 1162, 25, fill=color['error'], outline=color['error'])
        self.l.append(self.tl2)

        # 统计最终价格
        self.tl = Label(
            self.scr, 
            bg='brown1', 
            fg='white', 
            text='TOTAL= %s%d' % (money, self.TOTAL)
        )  # run 'TOTAL AMOUNT' on a thread  ####
        self.tl.place(x=1240, y=8, width=95, height=31)
        self.l.append(self.tl)


    def get_pizza(self, key, value):
        ''' 根据id查找pizza数据 '''
        return [p for p in pizzas if p.id == value]


    def get_order(self, key, value):
        ''' 根据id查找 Order 数据 '''
        return [o for o in orders if o.id == value]


    def show_regular_pizzas(self):
        ''' 显示普通 Pizza '''
        self.flush()
        self.create_header()

        # 定义窗体大小
        self.frame.config(
            width=WIDTH-30,
            height=HEIGHT-100
        )
        self.canva = Canvas(
            self.frame,
            bd=-2,
            bg='white',
            width=WIDTH-30,
            height=HEIGHT-100,
            highlightthickness=1
        )
        self.canva.place(x=0, y=0)

        # 定义每个 Pizza 的宽度和高度
        self.cc = 4                             # 定义每行显示4个
        self.cwidth = round((WIDTH-30)/self.cc)      # canvas width
        self.cheight = 400                      # canvas height
        self.imgs = []                          # 存储所有的 pizza 图片
        self.ids = []
        # 获取所有的普通 pizza 列表
        regular_pizzas = [p for p in pizzas if p.type == 'regular']
        # 打印 普通 Pizza 列表
        for i, item in enumerate(regular_pizzas):
            # 计算当前 Pizza 所在的行和列
            r = int(i/self.cc)
            c = i % self.cc
            # 先画一个大框
            self.veg = Canvas(
                self.frame,
                bg='snow',
                width=self.cwidth,
                height=self.cheight,
                highlightthickness=1
            )
            self.veg.grid(row=r, column=c)
            # 绘制灰色边框
            self.veg.create_rectangle(
                1, 1,
                self.cwidth,
                self.cheight,
                outline='snow4',
                width=1
            )

            # Pizza 的名称
            self.veg.create_text(
                160, 20,
                font=("Helvetica 15 normal"),
                fill='Dodgerblue2',
                text=item.name
            )

            # Pizza 的图片
            self.imgs.append(ImageTk.PhotoImage(Image.open(item.img)))
            self.veg.create_image(160, 160, image=self.imgs[i])

            # Pizza 的描述
            self.veg.create_text(
                160, 295,
                justify=CENTER,
                anchor=CENTER,
                font=("Helvetica 10 normal"),
                fill='dim gray',
                text=item.content
            )
            self.l.append(self.veg)

            # 画一个红色方框
            self.veg2 = Canvas(
                self.veg,
                bg='firebrick1',
                highlightthickness=1
            )
            self.veg2.place(
                x=2, y=320,
                width=self.cwidth-2,
                height=80
            )

            # 显示价格
            self.veg2.create_text(
                75, 40,
                font=("Helvetica 32 bold"),
                fill='snow',
                text='{}{}'.format(money, item.price)
            )

            # 左侧的减号：点击后数量-1
            self.minus = Button(
                self.veg2,
                bg=color['warning'],
                relief=FLAT,
                fg='white',
                text='-',
                font=("Sans 12 bold")
            )
            self.minus.place(x=150, y=10, width=20, height=20)
            self.minus.bind(
                "<Button-1>",
                partial(self.minus_pizza, self.minus, item.id, False)
            )

            # 数量，默认为0，单份不超过5个，总数也不能超过5个
            self.amount = Entry(
                self.veg2,
                bg='azure',
                textvariable=self.user_cart.get(item.id),
                relief=FLAT,
                justify='center'
            )
            self.amount.place(x=175, y=10, width=75, height=20)
            # self.carts[item.id] = self.amount
            # 购物车商品默认为0

            # 右侧的加号：点击后数量+1
            self.plus = Button(
                self.veg2,
                bg=color['warning'],
                fg='white',
                relief=FLAT,
                text='+',
                font=("Sans 12 bold"))
            self.plus.bind(
                "<Button-1>", partial(self.plus_pizza, self.plus, item.id, False)
            )
            self.plus.place(x=255, y=10, width=20, height=20)

            # 加入购物车
            self.cartBtn = Button(
                self.veg2,
                bg=color['warning'],
                relief=FLAT,
                fg='white',
                text='ADD TO CART',
                font=("Helvetica 11 bold")
            )
            self.cartBtn.bind(
                '<Button-1>',
                partial(self.add_to_cart, self.cartBtn, item.id)
            )
            self.cartBtn.place(x=150, y=40, width=127, height=30)
           

    def show_gourmet_pizzas(self):
        ''' 点击进入精品 Pizza '''
        self.flush()
        self.create_header()

        # 获取所有的精品 Pizza
        gourmet_pizzas = [p for p in pizzas if p.type == 'gourmet']

        mh = 250           # 定义精品 pizza 的高度
        hh = mh * (len(gourmet_pizzas)+1)

        self.frame.config(width=WIDTH-30, height=hh)
        self.canva = Canvas(
            self.frame, bd=-2, bg='white',
            width=WIDTH-30,
            height=hh,
            highlightthickness=1
        )

        self.canva.place(x=0, y=0)
        self.imgs = []
        self.ms = []
        # meal 1 ##
        # 显示精品 pizza 图片
        # item = pizzas['gourmet']['list'][0]

        for i, item in enumerate(gourmet_pizzas):
            # 显示Pizza图片
            self.imgs.append(ImageTk.PhotoImage(Image.open(item.img)))
            self.canva.create_image(300, 200+i*mh, image=self.imgs[i])

            # 显示精品 Pizza 的名称及介绍
            Label(
                self.canva,
                text=item.name,
                font=('Sans 18 bold'),
                justify='left',
                bg='white'
            ).place(x=600, y=84+i*mh)
            
            # Pizza 的介绍
            Label(
                self.canva,
                text=item.content,
                justify='left',
                anchor='nw',
                font=('Helvetica 12 normal'),
                bg='white'
            ).place(x=600, y=110+i*mh, width=400, height=100)

            # 价格
            Label(
                self.canva,
                text='{}{}'.format(money, item.price),
                font=('Helvetica 18 bold'),
                bg='orange2',
                fg='white'
            ).place(x=600, y=200+i*mh, width=50, height=35)

            # 左侧的减号：点击后数量-1
            minus = Button(
                self.canva,
                bg=color['warning'],
                relief=FLAT,
                fg='white',
                text='-',
                font=("Sans 12 bold")
            )
            minus.place(x=50+750, y=200+i*mh, width=20, height=20)
            minus.bind(
                "<Button-1>",
                partial(self.minus_pizza, minus, item.id, False)
            )

            # 数量，默认为0，单份不超过5个，总数也不能超过5个
            amount = Entry(
                self.canva,
                bg='azure',
                bd=2,
                textvariable=self.user_cart.get(item.id),
                relief=FLAT,
                justify='center'
            )
            amount.place(x=75+750, y=200+i*mh, width=75, height=20)
            # 购物车商品默认为0

            # 右侧的加号：点击后数量+1
            plus = Button(
                self.canva,
                bg=color['warning'],
                fg='white',
                relief=FLAT,
                text='+',
                font=("Sans 12 bold")
            )
            plus.bind(
                "<Button-1>", partial(self.plus_pizza, plus, item.id, False))
            plus.place(x=155+750, y=200+i*mh, width=20, height=20)

            # 加入购物车
            self.ms.append(
                Label(
                    self.canva,
                    text='ADD TO CART',
                    bg='firebrick2',
                    fg='snow',
                    font=('Sans 15 bold')
                )
            )
            self.ms[i].place(x=800, y=264+i*mh, width=160, height=33)
            self.ms[i].bind(
                '<Button-1>',
                partial(self.add_to_cart, self.ms[i], item.id)
            )


    def payment_window(self, val, event):  
        # Payment window
        self.flush()
        self.create_header()
        # self.f.place(x=0, y=0)
        self.frame.config(
            width=WIDTH-30,
            height=HEIGHT-100,
            bg='white'
        )
        self.canva = Canvas(
            self.frame,
            bd=-2,
            bg='white',
            width=WIDTH-30,
            height=HEIGHT-100,
            highlightthickness=1
        )  # 1000
        self.canva.place(x=0, y=0)
        
        # 在订单页面计算每一个id对应的数量购物车中的价钱
        self.temp_price = {}

        # 下单人信息
        Label(
            self.frame,
            text='PLEASE CHECK THE FOLLOWING DETAILS\n TO COMPLETE YOUR ORDER',
            font=('Helvetica 11 bold'),
            bg='white',
            fg='grey19'
        ).place(x=30, y=50)

        e = Entry(self.frame, bg='gray99')  # NAME   ##
        e.insert(0, self.NAME)
        e.place(x=55, y=105, width=250, height=28)

        e = Entry(self.frame, bg='gray99')  # Email   ##
        e.insert(0, self.mail)
        e.place(x=55, y=145, width=250, height=28)

        self.tel = Entry(self.frame, bg='gray99')  # PHONE NO   ##
        self.tel.insert(0, 'Phone No*: ')
        self.tel.place(x=55, y=185, width=250, height=28)

        self.canva.create_rectangle(
            14, 38, 365, 245, 
            width=2,
            outline='deep sky blue'
        )  # rectangle  ##

        # 接收地址
        Label(self.frame, text='YOUR DELIVERY ADDRESS', font=(
            'Helvetica 11 bold'), bg='white', fg='grey19').place(x=530, y=50)
        Label(self.frame, text='House No', bg='white').place(x=460, y=105)
        Label(self.frame, text='Street/Society ',
              bg='white').place(x=460, y=145)
        Label(self.frame, text='City', bg='white').place(x=460, y=185)

        self.he = Entry(self.frame, bg='gray99')  # HOUSE Entry field   ##
        self.he.place(x=550, y=105, width=210, height=28)
        # SOCIETY Entry field   ##
        self.se = Entry(self.frame, bg='gray99')
        self.se.place(x=550, y=145, width=210, height=28)
        self.ce = Entry(self.frame, bg='gray99')  # CITY Entry field   ##
        self.ce.place(x=550, y=185, width=210, height=28)
        self.canva.create_rectangle(
            14+435, 43, 360+440+25, 245, width=2, outline='deep sky blue')  # rectangle  ##

        # 订单资料
        Label(
            self.frame, 
            text='ORDER DETAILS', 
            font=(
            'Helvetica 11 bold'), 
            bg='white', fg='grey19'
        ).place(x=1020, y=50)
        Label(
            self.frame, 
            text='Pizzas\' price', 
            bg='white').place(
            x=936, y=110)  # TOTAL LABEL
        self.payment_pizzas_price = Label(
            self.frame, 
            text='\u0024 '+str(self.TOTAL),
              bg='white'
        )
        self.payment_pizzas_price.place(x=1084, y=110)
        
        # 快递费
        Label(self.frame, text='Delivery fee', bg='white').place(
            x=936, y=150)  # GST LABEL
        self.payment_delivery_fee = Label(
            self.frame, 
            text='{}{}'.format(money, delivery_fee),
            bg='white')
        self.payment_delivery_fee.place(x=1084, y=150)

        # 总价
        Label(
            self.frame, 
            text='TOTAL', 
            bg='turquoise1', 
            font=('bold 10')
        ).place(x=936, y=190)  # TOTAL LABEL

        self.payment_total = Label(
            self.frame, 
            text=str(delivery_fee+self.TOTAL),
            bg='white', 
            font=('bold 10')
        )
        self.payment_total.place(x=1084, y=190)

        self.canva.create_rectangle(
            894, 
            38, 
            1275, 
            245, 
            width=2, 
            outline='deep sky blue'
        )  # rectangle  ##

        # 绘制一个红色的矩形
        self.canva.create_rectangle(
            50, 288, 950, 318, 
            fill='brown3', 
            outline='white', 
            width=2
        )

        Label(self.canva, text='YOUR CART DETAILS', font=('Sans 12 bold'),
              fg='snow', bg='brown3').place(x=60, y=295, width=300, height=20)
        
        # 订单详情的表头：名称，数量，总价
        Label(
            self.canva,
            text='Item',
            font=('Sans 12 bold'),
            fg='gray2', bg='white'
        ).place(x=100, y=370)

        Label(
            self.canva,
            text='Type',
            font=('Sans 12 bold'),
            fg='gray2',
            bg='white'
        ).place(x=500, y=370)

        Label(
            self.canva,
            text='Amount',
            font=('Sans 12 bold'),
            fg='gray2',
            bg='white'
        ).place(x=650, y=370)

        Label(
            self.canva,
            text='Price',
            anchor='e',
            font=('Sans 12 bold'),
            fg='gray2',
            bg='white'
        ).place(x=830, y=370)

        # 获取购物车中实际的条目
        user_carts = {c: self.user_cart[c] for c in self.user_cart if int(self.user_cart[c].get()) > 0}

        # 绘制直线
        self.canva.create_line(
            100, 415,           # 起始点坐标
            900, 415,           # 结束点坐标
            width = 2,
            fill='gray2'
        )
        i = 0
        # 以标签方式绘制订单详情
        for i, c in enumerate(user_carts):
            a = int(self.user_cart[c].get())
            print('当前id={}数量为{}'.format(c, a))
            item = self.get_pizza('id', c)[0]
            # 订单名称
            Label(
                self.canva,
                text=item.name,
                font=('Sans 11 bold'),
                bg='white',
                fg='gray4'
            ).place(x=100, y=430+40*i)

            # 类型
            Label(
                self.canva,
                text=item.type,
                bg='white',
                font=('Helvetica 11 bold italic')
            ).place(x=500, y=432+40*i)

            # 数量
            # 左侧的减号：点击后数量-1
            minus = Button(
                self.canva,
                bg=color['warning'],
                relief=FLAT,
                fg='white',
                text='-',
                font=("sans 11 bold")
            )
            minus.place(x=650, y=432+40*i, width=20, height=20)
            minus.bind(
                "<Button-1>",
                partial(self.minus_pizza, minus, item.id, True)
            )
            # 数量，默认为0，单份不超过5个，总数也不能超过5个
            amount = Entry(
                self.canva,
                bg='azure',
                bd=2,
                textvariable=self.user_cart.get(item.id),
                relief=FLAT,
                justify='center'
            )
            amount.place(x=675, y=432+40*i, width=50, height=20)
            # 右侧的加号：点击后数量+1
            plus = Button(
                self.canva,
                bg=color['warning'],
                fg='white',
                relief=FLAT,
                text='+',
                font=("sans 12 bold"))
            plus.place(x=730, y=432+40*i, width=20, height=20)
            plus.bind(
                "<Button-1>", 
                partial(self.plus_pizza, plus, item.id, True)
            )

            # 单项总价
            self.temp_price[c] = Label(
                self.canva,
                anchor='e',
                text='{}{}'.format(money, item.price*a),
                font=('Times 11 bold'),
                bg='white'
            )
            self.temp_price[c].place(x=850, y=430+40*i)

        
        # 合计总价
        Label(
            self.canva,
            text='Delivery fee',
            font=('Sans 12 bold'),
            bg='white',
            fg='gray2'
        ).place(x=100, y=445+40*(i+1))

        self.delivery_fee_ = Label(
            self.canva,
            anchor='e',
            text='{}{}'.format(money, delivery_fee),
            font=('Sans 12 bold'),
            bg='white',
            fg='gray2'
        )
        self.delivery_fee_.place(x=850, y=445+40*(i+1))

        # 绘制直线
        self.canva.create_line(100, 475+40*(i+1), 900, 475+40*(i+1),
            width = 2,
            fill='gray2'
        )

        # 合计总价
        Label(
            self.canva,
            text='TOTAL',
            font=('Sans 12 bold'),
            bg='white',
            fg='gray2'
        ).place(x=100, y=460+40*(i+2))

        self.total_price = Label(
            self.canva,
            anchor='e',
            text='{}{}'.format(money, self.TOTAL+delivery_fee),
            font=('Sans 12 bold'),
            bg='white',
            fg='gray2'
        )
        self.total_price.place(x=850, y=460+40*(i+2))

        # 下单按钮
        self.po = Label(
            self.canva,
            text='Place Order',
            bg='firebrick3',
            fg='snow',
            font=('Sans 12 bold')
        )
        self.po.place(x=830, y=460+40*(i+3), width=120, height=40)
        self.po.bind(
            '<Button-1>',
            lambda val='1': self.place_order('1')
        )

    def place_order(self, val):
        ''' 点击下单 '''

        # 获取具体地址、街道、城市等信息
        house_no = self.he.get()
        street = self.se.get()
        city = self.ce.get()
        tel = self.tel.get()
        total = self.TOTAL + delivery_fee

        # 如果未填写地址信息，提示用户填写
        if not len(house_no) or not len(street) or not len(city):
            messagebox.showinfo(
                'Missing Details', 
                'Please provide address details for successelful delivery of your order.'
            )
        else:
            message = 'Dear {}, your order has been successelfully placed.\nIt will be delivered to {}, {}, {} in under an hour.\nThank you !'.format(self.NAME, house_no, street, city)
            messagebox.showinfo('Order placed', message)

            # 获取购物车中实际的条目
            user_carts = {c: self.user_cart[c] for c in self.user_cart if int(self.user_cart[c].get()) > 0}

            # 创建订单
            # 1. 根据购物车创建每个pizza的购买信息
            items = [Item(c, self.NAME, self.get_pizza(id, c)[0], int(user_carts[c].get()), int(user_carts[c].get()) * self.get_pizza(id, c)[0].price) for c in user_carts]
            # 一个订单由多个Items 构成
            order = Order(len(orders)+1, self.NAME, self.NAME, self.mail, tel, items, house_no, street, city, self.TOTAL, delivery_fee, total, datetime.now())
            
            # 一个用户可以有多个订单，orders是实际存在内存中的用户订单数据，此处可以写文件
            orders.append(order)

            # 清空购物车
            for c in user_carts:
                self.user_cart[c].set(0)
            self.TOTAL = 0
            self.ITEMS = 0

            # 跳转到订单页面
            self.orders()


    def orders(self):
        ''' 查看所有订单信息 '''

        self.flush()
        self.create_header()

        # self.f.place(x=0, y=0)
        self.frame.config(
            width=WIDTH-30,
            height=HEIGHT-100,
            bg='white'
        )
        self.canva = Canvas(
            self.frame,
            bd=-2,
            bg='white',
            width=WIDTH-30,
            height=HEIGHT-100,
            highlightthickness=1
        )  # 1000
        self.canva.place(x=0, y=0)

        Label(
            self.canva, 
            text='You have the following orders, select one and double-click to view details', 
            font=(
            'Helvetica 11 bold'), 
            bg='white', fg='grey19'
        ).place(x=20, y=20)

        # 方案 以表格绘制，key为列名，value为显示宽度
        columns = {
            'ID':50, 
            'Item':150, 
            'Time':200, 
            'Amount':100, 
            'Price':100,
            'Address':200,
            'Name':100,
            'Tel':150,
            'Email':150
        }
        self.treeview = ttk.Treeview(
            self.canva, 
            height=18,
            show="headings", 
            columns=list(columns.keys())
        )  # 表格
        self.treeview.place(x=20, y=60)

        for tc in columns: 
            self.treeview.column(tc, width=columns[tc], anchor='center')
            self.treeview.heading(tc, text=tc)

        # self.treeview.column('ID', width=50, anchor='w')
        # self.treeview.column('Item', width=200, anchor='center')
        # self.treeview.column('Time', width=200, anchor='center')
        # self.treeview.column('Amount', width=100, anchor='center')
        # self.treeview.column('Price', width=100, anchor='center')
        # self.treeview.column('Address', width=200, anchor='center')
        # self.treeview.column('Name', width=100, anchor='center')
        # self.treeview.column('Tel', width=200, anchor='center')
        # self.treeview.column('Email', width=100, anchor='center')

        # 绘制列
        # for cc in columns:
        #     self.treeview.heading(cc, text=cc)
        
        # self.treeview.pack(side=LEFT, fill=BOTH)
        for i, c in enumerate(orders):
            self.treeview.insert('', i, values=(
                    c.id, 
                    '{}...'.format(c.items[0].pizza.name), 
                    c.time.strftime('%Y-%m-%d %H:%M'), 
                    len(c.items), 
                    '{}{}'.format(money,c.total),
                    '{},{},{}'.format(c.house_no,c.street,c.city),
                    c.name,
                    c.tel,
                    c.email)
            )

        # 双击显示详情
        self.treeview.bind('<Double-1>', self.show_order)
        # 单击显示详情
        # self.treeview.bind('<Button-1>', self.show_order)

        for col in columns:  # 绑定函数，使表头可排序
            self.treeview.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(self.treeview, _col, False))


    def treeview_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题


    def show_order(self, event):
        ''' 查看订单的具体信息 '''

        self.flush()
        self.create_header()

        # self.f.place(x=0, y=0)
        self.frame.config(
            width=WIDTH-30,
            height=HEIGHT-100,
            bg='white'
        )
        self.canva = Canvas(
            self.frame,
            bd=-2,
            bg='white',
            width=WIDTH-30,
            height=HEIGHT-100,
            highlightthickness=1
        )  # 1000
        self.canva.place(x=0, y=0)

        for item in self.treeview.selection():
            item_text = self.treeview.item(item, "values")
            #print(item_text[0:2])  # 输出所选行的值
        # column= self.treeview.identify_column(event.x)# 列
        # row = self.treeview.identify_row(event.y)  # 行
        val = item_text[0:1]
        id = int(val[0])
        order = self.get_order('id', id)[0]

    
        Label(
            self.canva, 
            text='ORDER DETAILS', 
            font=(
            'Helvetica 11 bold'), 
            bg='white', fg='grey19'
        ).place(x=20, y=20)

        # 方案1： 以表格绘制
        columns = ['Item', 'Type', 'Amount', 'Price']
        treeview = ttk.Treeview(self.canva, height=18, show="headings", columns=columns)  # 表格
        treeview.place(x=20, y=70)

        treeview.column('Item', width=300, anchor='w')
        treeview.column('Type', width=200, anchor='center')
        treeview.column('Amount', width=150, anchor='center')
        treeview.column('Price', width=150, anchor='center')

        for cc in columns:
            treeview.heading(cc, text=cc)

        # treeview.pack(side=LEFT, fill=BOTH)
        for i, c in enumerate(order.items):
            item = self.get_pizza('id', c.pizza.id)[0]
            amount = c.amount
            price = c.price
            treeview.insert('', i, values=(item.name, item.type, amount, '{}{}'.format(money,price) ))

        for col in columns:  # 绑定函数，使表头可排序
            treeview.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(treeview, _col, False))


        # 订单资料
        Label(
            self.canva, 
            text='ORDER INFO', 
            font=(
            'Helvetica 11 bold'), 
            bg='white', 
            fg='grey19'
        ).place(x=936, y=20)

        Label(
            self.canva, 
            text='Order ID: {}'.format(order.id), 
            bg='white'
        ).place(x=936, y=70)  # TOTAL LABEL

        Label(
            self.canva, 
            text='Pizzas\' price: {}{}'.format(money, order.total), 
            bg='white'
        ).place(x=936, y=110)  # TOTAL LABEL
        
        # 快递费
        Label(
            self.canva, 
            text='Delivery fee: {}{}'.format(money, delivery_fee), 
            bg='white'
        ).place(x=936, y=150) 

        # 总价
        Label(
            self.canva, 
            text='Total: {}{}'.format(money, delivery_fee+order.total), 
            bg='white'
        ).place(x=936, y=190)  # TOTAL LABEL

        # 下单人姓名
        Label(
            self.canva, 
            text='Customer: '+order.name, 
            bg='white'
        ).place(x=936, y=230)
        # 下单人地址
        Label(
            self.canva, 
            text='Delivery Address: {}, {}, {}'.format(order.house_no, order.street, order.city), 
            bg='white'
        ).place(x=936, y=270)
        # 下单人电话
        Label(
            self.canva, 
            text='Tel '+ order.tel, 
            bg='white'
        ).place(x=936, y=310)
        # 下单人邮箱
        Label(
            self.canva, 
            text='Email: '+order.email, 
            bg='white'
        ).place(x=936, y=350)
        # 下单时间
        Label(
            self.canva, 
            text='Order time: '+order.time.strftime('%Y-%m-%d %H:%M'), 
            bg='white'
        ).place(x=936, y=390)


    def minus_pizza(self, minus, id, auto, event):
        ''' 购物车数量+1 '''
        # 购物车原来就有的个数
        n = int(self.user_cart[id].get())
        print('点击加入购物车', id, n, 1)
        tt = n - 1 if n >= 1 else 0
        print(tt)
        self.user_cart[id].set(tt)
        if auto: self.update_cart(id, auto)

    def plus_pizza(self, plus, id, auto, event):
        ''' 购物车数量+1 '''
        # 购物车原来就有的个数
        n = int(self.user_cart[id].get())
        print('点击加入购物车', id, n, 1)
        tt = n + 1 if n <= int(max_cart_item)-1 else int(max_cart_item)
        self.user_cart[id].set(tt)
        if auto: self.update_cart(id, auto)

    def add_to_cart(self, cartBtn, id, event):
        ''' 加入购物车 '''
        # 获取当前id 的 Pizza 在购物车里有多少件
        num = int(self.user_cart.get(id).get())
        print('点击加入购物车', id, num)
        if num == 0:
            num = 1
        self.user_cart[id].set(num)
        self.update_cart(id)

    def update_cart(self, id, order_page=False):
        '''
        @description: 更新购物车中当前 Pizza 的数量
        @param : id：Pizza的ID，order_page表示是不是结算页面，只有在结算页面才更新页面中对应的价格信息
        @return: 
        '''
        # 获取当前购物车中Pizza的个数及总价
        self.ITEMS = sum([int(self.user_cart.get(c).get())for c in self.user_cart])
        self.TOTAL = sum([int(self.user_cart.get(c).get()) * self.get_pizza('id', c)[0].price for c in self.user_cart])

        self.tl2.config(text=str(self.ITEMS))
        self.tl.config(text='{}{}{}'.format(
            'TOTAL=', 
            money, 
            self.TOTAL
        ))  
        # 更新购物车页面总价
        if order_page: 
            self.total_price.config(text='{}{}'.format(money,self.TOTAL))
            self.temp_price[id].config(text='{}{}'.format(money,int(self.user_cart.get(id).get()) * self.get_pizza('id', id)[0].price))
            self.payment_pizzas_price.config(text='{}{}'.format(money, self.TOTAL))
            self.payment_total.config(text='{}{}'.format(money, delivery_fee+self.TOTAL))
        # total amount

x = Main()
del(s)
