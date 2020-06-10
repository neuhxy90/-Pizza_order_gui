try:                        # for Python 3
    from tkinter import *
    from tkinter import messagebox
    # from tkinter.tix import *
except ImportError:         # for Python 2
    from Tkinter import *
    from Tkinter import messagebox
    from Tkinter.tix import *
from PIL import ImageTk, Image
from sqlite3 import *
import requests
import json  # for location
import smtplib  # for email
from email.mime.text import MIMEText
from email.header import Header
import math
from functools import partial  # for mouse events

# 定义主界面大小
WIDTH = 1366
HEIGHT = 768

# 定义程序的名称
TITLE = 'Heavenly Pizza GUI Ordering System'
# 定义一组颜色样式
COLOR = {
    'BACKGROUND':'linen',
    'SUCCESS':'green4',
    'INFO':'ivory2',
    'PRIMARY':'deep sky blue',
    'ERROR': 'tomato',
    'WARNING': 'orange'
}
# 定义用户找回密码配置的邮箱
MAIL = {
    'account':'carol.chen.cn@outlook.com',
    'password': '1qazxsw23edc',
    'port':587,
    'host': 'smtp.office365.com'
}
PIZZAS = {
    # 定义每一个pizza 展示大小
    'width':330,
    'height':429,
    # 常规 Pizza 数据
    'Regular pizzas':{
        'price':'$10',
        'list':[
            {
                'id':1,
                'name':'Margherita',
                'img': 'img/Margherita.jpg',
                'content':'Fresh tomato, mozzarella, fresh basil, parmesan'
            },
            {
                'id':2,
                'name':'Kiwi',
                'img': 'img/Kiwi.jpg',
                'content':'Bacon, egg, mozzarella'
            },
            {
                'id':3,
                'name':'Garlic',
                'img': 'img/Garlic.jpg',
                'content':'Mozzarella, garlic'
            },
            {
                'id':4,
                'name':'Cheese',
                'img': 'img/Cheese.jpg',
                'content':'Mozzarella, oregano'
            },
            {
                'id':5,
                'name':'Hawaiian',
                'img': 'img/Hawaiian.jpg',
                'content':'Ham, pineapple, mozzarella'
            },
            {
                'id':6,
                'name':'Mediterranean (vegan)',
                'img': 'img/Mediterranean (vegan).jpg',
                'content':'Lebanese herbs, olive oil, fresh tomatoes, olives, onion'
            }
        ]
    },
    # 精品 Pizza 数据
    'Gourmet pizzas':{
        'price':'$17',
        'list':[
            {
                'id':1,
                'name':'Meat',
                'img': 'img/Meat.jpg',
                'content':'Bacon, pancetta, ham, onion, pepperoni, mozzarella'
            },
            {
                'id':2,
                'name':'Chicken Cranberry',
                'img': 'img/Chicken Cranberry.jpg',
                'content':'Smoked chicken, cranberry, camembert mozzarella'
            },
            {
                'id':3,
                'name':'Satay Chicken',
                'img': 'img/Satay Chicken.jpg',
                'content':'Smoked chic, onions, capsicum, pine nuts, satay sauce, mozzarella Chilli flakes and dried basil'
            },
            {
                'id':4,
                'name':'Big BBQ Bacon',
                'img': 'img/Big BBQ Bacon.jpg',
                'content':'Smoky Bacon served on our classic marinara tomato sauce, heaped with mozzarella, topped off with a sweet and tangy BBQ drizzle'
            },
            {
                'id':5,
                'name':'Veggie',
                'img': 'img/Veggie.jpg',
                'content':'sweet red onion, mushroom, red capsicum & melting mozzarella with drizzles of our tangy roast capsicum drizzle, finished with a dash of oregano.'
            },
            {
                'id':6,
                'name':'Meatlovers',
                'img': 'img/Meatlovers.jpg',
                'content':'Spicy pepperoni, Italian sausage, succulent ham, seasoned ground beef and crispy bacon all piled onto classic marinara sauce and finished with cheesy mozzarella and a drizzle of BBQ sauce.'
            }
        ]
    }
}

# 主程序初始化
s = Tk()
s.title(TITLE)
s.geometry("1366x768")

class Main:
    def __init__(self):
        # 连接本地sqlite3数据库
        self.c = connect("mydata.db")
        self.cur = self.c.cursor()
        try:
            # 创建表 staff
            self.cur.execute(
                "create table staff(name varchar(50),user varchar(50),passw varchar(50),email varchar(50))")
        except:
            pass
        #####################       flush list []           #############################
        self.l = []  # It keeps all the widgets & destroys them whenever user moves to a new window
        ########################     GUI window             #############################
        self.scr = s
        self.scr.configure(bg='white')
        self.f = Frame(self.scr, bg='white')
        self.f.place(x=0, y=0, width=WIDTH, height=HEIGHT)

        # 初始化购物车内Pizza个数
        self.ITEMS = 0
        self.TOTAL = 0
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
        try:
            self.flush()
        except:
            pass
        self.f.config(bg=COLOR['BACKGROUND'])

        #   CANVAS  for image
        self.canvas = Canvas(self.f, bg=COLOR['BACKGROUND'], bd=-2)
        self.canvas.place(x=0, y=0, width=WIDTH, height=HEIGHT)  # previous height=125
        # self.img=ImageTk.PhotoImage(Image.open('img/background_.jpg'))
        # self.canvas.create_image(681,405,image=self.img)
        self.l.append(self.canvas)

        #   USERNAME label
        self.title = Label(self.f, bg=COLOR['BACKGROUND'], text='Sign in ' + TITLE, padx=10, anchor='center', font=('Georgia 14 bold'))
        self.title.place(x=WIDTH/2 - 200, y=50, width=600, height=25)
        self.l.append(self.title)

        #   USERNAME label
        self.username = Label(self.f, bg=COLOR['BACKGROUND'], text='Username', padx=10, anchor='e')
        self.username.place(x=WIDTH/2 - 110, y=130, width=110, height=25)
        self.l.append(self.username)

        #  USERNAME entry_field
        self.un_entry = Entry(self.f, bg='azure', justify='center')
        self.un_entry.place(x=WIDTH/2, y=130, width=200, height=25)
        self.l.append(self.un_entry)

        #   PASSWORD label
        self.passw = Label(self.f, bg=COLOR['BACKGROUND'], text='Password', padx=10,  anchor='e')
        self.passw.place(x=WIDTH/2 - 110, y=175, width=110, height=25)
        self.l.append(self.passw)

        #   PASSWORD entry_field
        self.p_entry = Entry(self.f, show="*", bg='azure', justify='center')
        self.p_entry.place(x=WIDTH/2, y=175, width=200, height=25)
        self.l.append(self.p_entry)

        # 去注册按钮
        self.r = Button(self.f, bg=COLOR['INFO'], text='Create an account >>', command=self.register)
        self.r.place(x=WIDTH/2 - 100, y=270, width=150, height=28)
        self.l.append(self.r)

        # 登录按钮
        self.submit = Button(self.f, bg=COLOR['SUCCESS'], fg='snow', text='Sign in',command=lambda: self.result("login"))
        self.submit.place(x=WIDTH/2 + 100, y=270, width=100, height=28)
        self.l.append(self.submit)

    
    def register(self):
        '''
        [注册界面] 
        -------------------------------------------------
        用户点击登录界面的 [Sign up] 的时候调用，包括账号、
        密码，邮箱等，用户点击 [Sign up] 后进入 登录界面，
        如果已有账户，点击 [Sign in] 进入登录界面
        '''
        try:
            self.flush()
        except:
            pass
        self.f.config(bg=COLOR['BACKGROUND'])

        #   CANVAS  for image
        self.canvas = Canvas(self.f, bg=COLOR['BACKGROUND'], bd=-2)
        # previous height=125
        self.canvas.place(x=0, y=0, width=WIDTH, height=HEIGHT)
        # self.img=ImageTk.PhotoImage(Image.open('img/background.jpg'))
        # self.canvas.create_image(681,405,image=self.img)
        self.l.append(self.canvas)

        #   USERNAME label
        self.title = Label(self.f, bg=COLOR['BACKGROUND'], text='Sign up ' + TITLE, padx=10, anchor='center', font=('Georgia 14 bold'))
        self.title.place(x=WIDTH/2 - 200, y=50, width=600, height=25)
        self.l.append(self.title)

        #   NAME label
        self.Name = Label(self.f, bg=COLOR['BACKGROUND'], text='Name', padx=10, anchor='e')
        self.Name.place(x=WIDTH/2 - 110, y=100, width=110, height=25)
        self.l.append(self.Name)

        #   NAME entry
        self.N_entry = Entry(self.f)
        self.N_entry.place(x=WIDTH/2, y=100, width=200, height=25)
        self.l.append(self.N_entry)

        #   USERNAME label
        self.name = Label(self.f, bg=COLOR['BACKGROUND'], text='Userame', padx=10, anchor='e')
        self.name.place(x=WIDTH/2 - 110, y=140, width=110, height=25)
        self.l.append(self.name)

        #  USERNAME entry_field
        self.n_entry = Entry(self.f)
        self.n_entry.place(x=WIDTH/2, y=140, width=200, height=25)
        self.l.append(self.n_entry)

        #   PASSWORD label
        self.plabel = Label(self.f, bg=COLOR['BACKGROUND'], text='Password', padx=10, anchor='e')
        self.plabel.place(x=WIDTH/2 - 110, y=180, width=110, height=25)
        self.l.append(self.plabel)

        #   PASSWORD entry_field
        self.p_entry = Entry(self.f, show="*")
        self.p_entry.place(x=WIDTH/2, y=180, width=200, height=25)
        self.l.append(self.p_entry)

        #   PASSWORD2 label
        self.plabel2 = Label(self.f, bg=COLOR['BACKGROUND'], text='Retype password', padx=10, anchor='e')
        self.plabel2.place(x=WIDTH/2 - 140, y=220, width=140, height=25)
        self.l.append(self.plabel2)

        #   PASSWORD entry_field
        self.p_entry2 = Entry(self.f, show="*")
        self.p_entry2.place(x=WIDTH/2, y=220, width=200, height=25)
        self.l.append(self.p_entry2)

        #   EMAIL field
        self.e_mail = Label(self.f, bg=COLOR['BACKGROUND'], text="Your email", padx=10, anchor='e')
        self.e_mail.place(x=WIDTH/2 - 110, y=260, width=110, height=25)
        self.l.append(self.e_mail)

        #   EMAIL entry_field
        self.e_entry = Entry(self.f)
        self.e_entry.place(x=WIDTH/2, y=260, width=200, height=25)
        self.l.append(self.e_entry)

        #   REGISTER button
        self.rbutton = Button(self.f, bg=COLOR['SUCCESS'], fg='snow', text='Sign up',command=lambda: self.result("register"))
        self.rbutton.place(x=WIDTH/2 + 90, y=320, width=110, height=31)
        self.l.append(self.rbutton)


        # 返回登录按钮
        self.r = Button(self.f, bg=COLOR['INFO'], text='<< Back to Sign in', command=self.login)
        self.r.place(x=WIDTH/2 - 100, y=320, width=130, height=31)
        self.l.append(self.r)
        self.scr.mainloop()


    def flush(self):
        '''
        flush() function destroys all the widgets of the frame 
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
                    messagebox.showinfo("Invalid credentials.", "Username %r doesn't exist.\nPlease 'register' to continue." % (
                        self.un_entry.get()))  # wrong username
                    self.__init__()
                else:  # username exists, check for correct password now
                    self.MAIL = list(self.cur.execute(
                        "select email from staff where user=%r" % (self.un_entry.get())))[0][0]
                    self.NAME = list(self.cur.execute(
                        "select name from staff where user=%r" % (self.un_entry.get())))[0][0]
                    print(self.NAME)
                    # checking for correct password
                    x = self.cur.execute(
                        "select count(*) from staff where passw=%r" % (self.p_entry.get()))
                    # correct password, grant access to order.
                    if list(x)[0][0]:
                        self.create_order('1')
                    else:                  # wrong password
                        messagebox.showinfo(
                            "Wrong password", "Please enter a valid password\nForgot password ?")
                        self.rbutton = Button(
                            self.scr, text='Recover my password', command=self.recover_password, padx=10, anchor='center', relief='flat', bg=COLOR['WARNING'])
                        self.rbutton.place(x=WIDTH/2, y=220, width=150, height=30)
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
            mail = list(self.cur.execute("select email from staff where user=%r and name=%r" % (self.un_entry.get(), self.NAME)))[0][0]
            print('email id is ', mail)
            self.mail = mail
            password = list(self.cur.execute(
                "select passw from staff where name=%r" % (self.NAME)))[0][0]
            server = smtplib.SMTP(MAIL['host'], MAIL['port'])
            server.starttls()
            print('connected to outlook')
            server.login(MAIL['account'], MAIL['password'])
            print('logged in')

            receivers = [mail]
            Subject = 'Recover password for %s' % TITLE
            Content = 'Hello '+self.NAME+',\n\nYour password for '+TITLE+' is '+''+password+''
            msg = MIMEText(Content, 'plain', 'utf-8')
            # msg['From'] = Header(MAIL['account'], 'utf-8') 
            msg['To'] = Header('', 'utf-8')
            msg['Subject'] = Header(Subject, 'utf-8')
            print(msg)
            server.sendmail(MAIL['account'], receivers, msg.as_string())
            
            print('mail sent')
            server.close()
            messagebox.showinfo('Info', 'Dear '+self.NAME+', your password has been sent to ' + mail+'\nPlease try again using the correct password.')
        except smtplib.SMTPException as e:
            print(e)
            messagebox.showinfo(
                'Erro', "Your password couldn't be sent. Please check your internet connection.")
        self.flush()
        self.__init__()


    def myfunction(self, event):
        # 'width' & 'height' are actual scrollable frame size.
        self.canvas.configure(scrollregion=self.canvas.bbox(
            "all"), width=WIDTH-15, height=HEIGHT)

    def func(self, val):
        if self.dict[val][1]['R'] == 0 and self.dict[val][1]['M'] == 0 and self.dict[val][1]['L'] == 0:
            messagebox.showinfo(
                'Message', 'Please select a size before adding pizza to the cart')
        else:  # some size has been selected...
            if self.__labels__[int(val)]['text'] == 'REMOVE':  # remove from cart
                self.dict[val][2] = False
                if self.dict[val][1]['R'] == 1:
                    self.dict[val][1]['R'] = 0
                    self.P['R'] -= 1
                    self.TOTAL -= 205
                    self.ITEMS -= 1
                    self.__R__[int(val)].set(0)
                if self.dict[val][1]['M'] == 1:
                    self.dict[val][1]['M'] = 0
                    self.P['M'] -= 1
                    self.TOTAL -= 385
                    self.ITEMS -= 1
                    self.__M__[int(val)].set(0)
                if self.dict[val][1]['L'] == 1:
                    self.dict[val][1]['L'] = 0
                    self.P['L'] -= 1
                    self.TOTAL -= 595
                    self.ITEMS -= 1
                    self.__L__[int(val)].set(0)
                self.__labels__[int(val)].config(
                    text='ADD TO CART', fg='white')
            else:  # add to cart
                self.dict[val][2] = True
                if self.dict[val][1]['R'] == 1:
                    self.P['R'] += 1
                    self.TOTAL += 205
                    self.ITEMS += 1
                if self.dict[val][1]['M'] == 1:
                    self.P['M'] += 1
                    self.TOTAL += 385
                    self.ITEMS += 1
                if self.dict[val][1]['L'] == 1:
                    self.P['L'] += 1
                    self.TOTAL += 595
                    self.ITEMS += 1
                self.__labels__[int(val)].config(
                    text='REMOVE', fg='SpringGreen2')
            self.tl2.config(text=str(self.ITEMS))
            self.tl.config(text='TOTAL='+str(self.TOTAL) +
                           ' \u0024')  # total amount

    def drink_cart(self, val, price):
        if self.__labels2__[int(val)]['text'] == 'REMOVE':  # remove from cart
            self.D[val][0] = False
            self.TOTAL -= self.D[val][2]
            self.ITEMS -= 1
            self.__labels2__[int(val)].config(
                text='ADD TO CART', bg='light sea green', fg='white')
        else:  # ADD TO CART ##
            self.D[val][0] = True
            self.TOTAL += self.D[val][2]
            self.ITEMS += 1
            self.__labels2__[int(val)].config(
                text='REMOVE', bg='light sea green', fg='black')
        self.tl2.config(text=str(self.ITEMS))  # ITEMS ##
        self.tl.config(text='TOTAL='+str(self.TOTAL)+' \u0024')  # total amount

    def meals_func(self, val, price):
        if self.__labels3__[int(val)]['text'] == 'REMOVE':  # remove from cart
            self.M[val][0] = False
            self.TOTAL -= self.M[val][2]
            self.ITEMS -= 1
            self.__labels3__[int(val)].config(
                text='ADD TO CART', bg='firebrick2', fg='gold')
        else:  # ADD TO CART
            self.M[val][0] = True
            self.TOTAL += self.M[val][2]
            self.ITEMS += 1
            self.__labels3__[int(val)].config(
                text='REMOVE', bg='firebrick2', fg='black')
        self.tl2.config(text=str(self.ITEMS))  # ITEMS ##
        self.tl.config(text='TOTAL='+str(self.TOTAL)+' \u0024')  # total amount

    def cbR(self, R, val):  # checkbutton functions
        if R.get():  # only 'set' when label reads 'ADD TO CART'
            if self.__labels__[int(val)]['text'] == 'ADD TO CART':
                self.__R__[int(val)].set(1)
                self.dict[val][1]['R'] = 1
            else:  # label reads 'REMOVE', then another checkbox has been clicked.
                self.__R__[int(val)].set(0)
        else:
            if self.__labels__[int(val)]['text'] == 'ADD TO CART':
                self.__R__[int(val)].set(0)
                self.dict[val][1]['R'] = 0
            else:
                self.__R__[int(val)].set(1)

    def cbM(self, M, val):
        if M.get():
            if self.__labels__[int(val)]['text'] == 'ADD TO CART':
                self.__M__[int(val)].set(1)
                self.dict[val][1]['M'] = 1
            else:
                self.__M__[int(val)].set(0)
        else:
            if self.__labels__[int(val)]['text'] == 'ADD TO CART':
                self.__M__[int(val)].set(0)
                self.dict[val][1]['M'] = 0
            else:
                self.__M__[int(val)].set(1)

    def cbL(self, L, val):
        if L.get():
            if self.__labels__[int(val)]['text'] == 'ADD TO CART':
                self.__L__[int(val)].set(1)
                self.dict[val][1]['L'] = 1
            else:
                self.__L__[int(val)].set(0)
        else:
            if self.__labels__[int(val)]['text'] == 'ADD TO CART':
                self.__L__[int(val)].set(0)
                self.dict[val][1]['L'] = 0
            else:
                self.__L__[int(val)].set(1)

    def entry(self, wel, color, event):                          # <<<<<< HOVERING >>>>>>
        self.wel.configure(background=color, foreground='white')

    def exit_(self, wel, color, event):
        self.wel.configure(background=color, foreground='red')

    def entryP(self, pizza_label, color, event):
        self.pizza_label.configure(background=color, foreground='white')

    def exitP(self, pizza_label, color, event):
        self.pizza_label.configure(background=color, foreground='white')

    # def entryD(self, drinks_label, color, event):
    #     self.drinks_label.configure(background=color, foreground='red')

    # def exitD(self, drinks_label, color, event):
    #     self.drinks_label.configure(background=color, foreground='white')

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
        ''' PARENT frame will <<NOT>> be destroyed '''
        self.canvas = Canvas(self.f, bd=-2)
        ''' canvas will also <<NOT>> be destroyed '''
        self.frame = Frame(self.canvas, bd=-2, bg='white')
        self.myscrollbar = Scrollbar(
            self.f, orient=VERTICAL, command=self.canvas.yview)  # SCROLL BAR   ####
        self.canvas.configure(yscrollcommand=self.myscrollbar.set)
        self.myscrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.pack(side=LEFT)
        self.canvas.create_window((0, 0), window=self.frame)
        self.frame.bind("<Configure>", self.myfunction)

        # 建立顶部菜单栏
        self.head = Canvas(self.scr, bd=-2, bg='white')  # head canvas ######
        self.head.place(x=0, y=0, width=WIDTH, height=59)
        self.l.append(self.head)

        # WELCOME LABEL ##
        self.wel = Label(self.head, 
                    text='Welcome, '+self.NAME, 
                    fg='red',
                    bg='white', 
                    font=('Serif 12 bold'))  
        
        self.wel.place(x=6, y=4, width=200, height=44)
        self.wel.bind('<Enter>', partial(self.entry, self.wel, 'red'))
        self.wel.bind('<Leave>', partial(self.exit_, self.wel, 'white'))
        self.l.append(self.wel)
        # self.head.create_rectangle(5, 3, 106, 54, outline='red', fill='white')

        #   Logout button
        self.logout_btn = Button(self.scr, text='Logout', bg=COLOR['WARNING'], command=self.logout)
        self.logout_btn.place(x=200+20, y=4, width=90, height=44)
        self.l.append(self.logout_btn)

        # 常规 Pizza
        # self.pizza_logo = PhotoImage(
        #     file='img/pizza_logo.png')  # pizza logo  ##
        # self.head.create_image(460+20, 29, image=self.pizza_logo)
        self.pizza_label = Label(self.head, text='Regular pizzas', bg='red', fg='snow', font=('Helvetica 12 bold'))
        self.pizza_label.place(x=423+20, y=4, width=150, height=44)
        self.pizza_label.bind('<Button-1>', lambda val='1': self.show_regular_pizzas())
        self.pizza_label.bind('<Enter>', partial(self.entryP, self.pizza_label, 'coral'))
        self.pizza_label.bind('<Leave>', partial(self.exitP, self.pizza_label, 'red'))
        self.l.append(self.pizza_label)
        # self.head.create_oval(405+20, 9, 441+20, 51, fill='red', outline='red', width=2)
        # self.head.create_oval(405+150+20, 9, 441+150+20, 51, fill='red', outline='red', width=2)

        # 精品 Pizza
        self.meals_label = Label(self.scr, text='Gourmet pizzas', bg='red', fg='snow', padx=10, font=('Helvetica 12 bold'))
        self.meals_label.place(x=695+20, y=4, width=150, height=44)
        self.meals_label.bind('<Button-1>', lambda val='1': self.show_gourmet_pizzas())
        self.meals_label.bind('<Enter>', partial(self.entryM, self.meals_label, 'coral'))
        self.meals_label.bind('<Leave>', partial(self.exitM, self.meals_label, 'red'))
        self.l.append(self.meals_label)
        # self.head.create_oval(682-5+20, 9, 718-5+20, 51,
        #                       fill='red', outline='red', width=2)
        # self.head.create_oval(682+150-5+20, 9, 718+150-5+20,
        #                       51, fill='red', outline='red', width=2)

        # 头部右侧购物车
        self.pay = Label(self.scr, text='Checkout', fg='medium aquamarine',
                         bg='snow', font=('Sans 12 bold'))  # checkout logo ##
        self.pay.place(x=985, y=8, height=42, width=100)
        self.pay.bind('<Button-1>', lambda val='1': self.payment_window('1'))
        self.pay.bind('<Enter>', partial(
            self.entryC, self.pay, 'medium aquamarine'))
        self.pay.bind('<Leave>', partial(self.exitC, self.pay, 'white'))
        self.l.append(self.pay)

        self.head.create_rectangle(
            984, 7, 1085, 50, fill='white', outline='medium aquamarine')
        
        # 购物车小图片
        self.cart = PhotoImage(file='img/cart2.png')  # cart logo ##
        self.head.create_image(1140, 33, image=self.cart)
        # self.l.append(self.cart)

        # 购物车里有几件Pizza
        self.tl2 = Label(self.head, bg='yellow', fg='black',
                         text=self.ITEMS, font=('Sans 11'))  # NO OF ITEMS ##
        self.tl2.place(x=1141, y=8, width=17, height=15)
        self.head.create_oval(
            1137, 5, 1162, 25, fill='yellow', outline='yellow')
        self.l.append(self.tl2)

        # 统计最终价格
        self.tl = Label(self.scr, bg='brown1', fg='white', text='TOTAL=%d \u0024' % (
            self.TOTAL))  # run 'TOTAL AMOUNT' on a thread  ####
        self.tl.place(x=1240, y=8, width=95, height=31)
        self.l.append(self.tl)

        

        self.__labels__ = ['0']  # list to store label objects ####




    def create_order(self, val):
        self.flush()
        self.show_regular_pizzas()


    def show_regular_pizzas(self):
        ''' 显示普通 Pizza '''
        self.flush()
        self.create_header()

        # specifications of a 'CANVAS'
        self.cwidth = PIZZAS['width']+1  # canvas width
        self.cheight = PIZZAS['height']+1  # canvas height

        self.cbg = 'snow'  # canvas bg color
        self.ncolor = 'Dodgerblue2'  # name color
        self.nfont = ("Helvetica 15 normal")  # name font description
        self.dcolor = 'dim gray'  # desciption color
        self.dfont = ("Helvetica 10 normal")  # descr. font description
        self.sizecolor = 'snow'
        self.sizefont = ("Helvetica 12 normal")
        self.rec_color = 'snow4'
        self.cbg2 = 'firebrick1'


        self.frame.config(width=WIDTH-15, height=HEIGHT)
        self.canva = Canvas(self.frame, bd=-2, bg='white',
                            width=WIDTH-15, height=HEIGHT, highlightthickness=1)
        self.canva.place(x=0, y=0)
        self.cc = 4                     # 定义每行显示4个
        self.imgs = []                  # 存储所有的 pizza 图片

        for i, pizza in enumerate(PIZZAS['Regular pizzas']['list']):
            # 当前Pizza 所在的行和列计算
            r = int(i/self.cc)
            c = i % self.cc
            # 先画一个大框
            self.veg = Canvas(self.frame, bg=self.cbg, width=self.cwidth, height=self.cheight, highlightthickness=1)
            self.veg.grid(row=r, column=c)
            self.veg.create_rectangle(1, 1, PIZZAS['width'], PIZZAS['height'], outline=self.rec_color, width=1)
            
            # Pizza 的名称
            self.veg.create_text(161, 29, font=self.nfont,
                                fill=self.ncolor, text=pizza['name'])
            # Pizza 的图片
            self.imgs.append(ImageTk.PhotoImage(Image.open(pizza['img'])))
            self.veg.create_image(162, 172, image=self.imgs[i])
            
            # Pizza 的描述
            self.veg.create_text(160, 322, justify=CENTER, anchor=CENTER, font=self.dfont, fill=self.dcolor,text=pizza['content'])
            self.l.append(self.veg)

            self.veg2 = Canvas(self.veg, bg=self.cbg2, highlightthickness=1)
            self.veg2.place(x=2, y=341, width=self.cwidth-3, height=88)
            # 显示价格
            self.veg2.create_text(155, 18, font=self.sizefont, fill=self.sizecolor,
                                text=PIZZAS['Regular pizzas']['price'])
            # 复选框
            Checkbutton(self.veg2, 
                        bg=self.cbg2, 
                        relief=FLAT, 
                        ).place(x=98, y=5)
            # 加入购物车
            self.label1 = Label(self.veg2, 
                                bg=COLOR['WARNING'], 
                                fg='white',
                                text='ADD TO CART', 
                                font=("Sans 12 bold"))
            self.label1.bind("<Button-1>", lambda val=pizza['id']: self.func(pizza['id']))
            self.label1.place(x=94, y=40, width=110, height=30)
            self.__labels__.append(self.label1)
            self.veg2.create_oval(
                77, 33, 220, 76, fill=COLOR['WARNING'], outline=COLOR['WARNING'], width=0)

            # self.R1.set(self.dict['1'][1]['R'])

        # for d in self.dict:
        #     if self.dict[d][2] == True:
        #         self.__labels__[int(d)].config(
        #             text='REMOVE', fg='SpringGreen2')

        
    def show_gourmet_pizzas(self):
        ''' 点击进入精品 Pizza '''
        self.flush()
        self.create_header()

        # specifications of a 'CANVAS'
        self.cwidth = PIZZAS['width']+1  # canvas width
        self.cheight = PIZZAS['height']+1  # canvas height

        self.cbg = 'snow'  # canvas bg color
        self.ncolor = 'Dodgerblue2'  # name color
        self.nfont = ("Helvetica 15 normal")  # name font description
        self.dcolor = 'dim gray'  # desciption color
        self.dfont = ("Helvetica 10 normal")  # descr. font description
        self.sizecolor = 'snow'
        self.sizefont = ("Helvetica 12 normal")
        self.rec_color = 'snow4'
        self.cbg2 = 'firebrick1'

        mh = 250           # 定义精品 pizza 的高度
        hh = mh * (len(PIZZAS['Gourmet pizzas']['list'])+1)

        self.frame.config(width=WIDTH-15, height=hh)
        self.canva = Canvas(self.frame, bd=-2, bg='white',
                            width=WIDTH-15, height=hh, highlightthickness=1)

        self.canva.place(x=0, y=0)
        self.imgs = []
        self.ms = []
        # meal 1 ##
        # 显示精品 pizza 图片
        # item = PIZZAS['Gourmet pizzas']['list'][0]

        for i,item in enumerate(PIZZAS['Gourmet pizzas']['list']):
            # 显示Pizza图片
            self.imgs.append(ImageTk.PhotoImage(Image.open(item['img'])))  
            self.canva.create_image(300, 200+i*mh, image=self.imgs[i])
            
            # 显示精品 Pizza 的名称及介绍
            Label(self.canva, 
                    text=item['name'], 
                    font=('Sans 18 bold'), 
                    justify='left',
                    bg='white').place(x=600, y=84+i*mh)

            Label(self.canva, 
                text=item['content'], 
                justify='left',
                anchor = 'nw',
                font=('Helvetica 12 normal'),
                bg='white').place(x=600, y=110+i*mh, width=400, height=100)
            
            # self.canva.create_polygon(190, 260, 390, 260, 420, 300, 220, 300, fill='firebrick2', width=2)
            # 加入购物车
            self.ms.append(Label(self.canva, text='ADD TO CART',
                            bg='firebrick2', fg='gold', font=('Sans 15 bold')))
            self.ms[i].place(x=800, y=264+i*mh, width=160, height=33)
            self.ms[i].bind('<Button-1>', lambda val=item['id'],
                            price=PIZZAS['Gourmet pizzas']['price']: self.meals_func(item['id'], price))

            Label(self.canva, text=PIZZAS['Gourmet pizzas']['price'], font=('Helvetica 18 bold'), bg='orange2',
                    fg='white').place(x=800, y=200+i*mh, width=50, height=35)

        


        # for m in self.M:
        #     if self.M[m][0] == True:  # previously selected meal
        #         self.__labels3__[int(m)].config(
        #             text='REMOVE', bg='firebrick2', fg='black')


    def payment_window(self, val):  # Payment window       #####
        if(self.P['R'] == 0 and self.P['M'] == 0 and self.P['L'] == 0):
            messagebox.showinfo("No pizzas selected.",
                                "Please make an order to continue")
        else:
            self.flush()
            self.create_header()
            # self.f.place(x=0,y=0)
            self.frame.config(width=1336, height=1410,
                              bg='white')  # prev height=1200
            self.canva = Canvas(self.frame, bd=-2, bg='white',
                                width=1336, height=1410, highlightthickness=1)  # 1000
            self.canva.place(x=0, y=0)

            Label(self.frame, text='PLEASE CHECK THE FOLLOWING DETAILS\n TO COMPLETE YOUR ORDER', font=(
                'Helvetica 11 bold'), bg='white', fg='grey19').place(x=30, y=50)
            e = Entry(self.frame, bg='gray99')  # NAME   ##
            e.insert(0, self.NAME)
            e.place(x=55, y=105, width=250, height=28)
            e = Entry(self.frame, bg='gray99')  # EMAIL   ##
            e.insert(0, self.MAIL)
            e.place(x=55, y=145, width=250, height=28)
            e = Entry(self.frame, bg='gray99')  # PHONE NO   ##
            e.insert(0, 'Phone No*')
            e.place(x=55, y=185, width=250, height=28)
            self.canva.create_rectangle(
                14, 38, 365, 245, width=2, outline='deep sky blue')  # rectangle  ##

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

            # self.loc = PhotoImage(file='img/loc.png')
            # self.loc_logo = Label(self.canva, image=self.loc, bg='white')
            # self.loc_logo.place(x=772, y=177, width=37, height=42)
            # self.loc_logo.bind(
            #     '<Button-1>', lambda val='1': self.detect_loc('1'))
            # self.dl = Label(self.canva, text='Detect City')
            # self.dl.place(x=760, y=220)
            # self.dl.bind('<Button-1>', lambda val='1': self.detect_loc('1'))

            Label(self.frame, text='ORDER DETAILS', font=(
                'Helvetica 11 bold'), bg='white', fg='grey19').place(x=1020, y=50)
            Label(self.frame, text='Net Price', bg='white').place(
                x=936, y=110)  # TOTAL LABEL
            Label(self.frame, text='\u0024 '+str(self.TOTAL),
                  bg='white').place(x=1084, y=110)
            Label(self.frame, text='GST', bg='white').place(
                x=936, y=150)  # GST LABEL
            Label(self.frame, text='\u0024 '+str(math.ceil(0.18 *
                                                           self.TOTAL)), bg='white').place(x=1084, y=150)
            Label(self.frame, text='TOTAL', bg='turquoise1', font=(
                'bold 10')).place(x=936, y=190)  # TOTAL LABEL
            Label(self.frame, text=str(math.ceil(0.18*self.TOTAL)+self.TOTAL),
                  bg='white', font=('bold 10')).place(x=1084, y=190)
            self.canva.create_rectangle(
                894, 38, 1275, 245, width=2, outline='deep sky blue')  # rectangle  ##

            self.canva.create_rectangle(
                50, 288, 900, 358, fill='brown3', outline='white', width=2)
            Label(self.canva, text='YOUR CART DETAILS', font=('Sans 21 bold'),
                  fg='snow', bg='brown3').place(x=60, y=295, width=300, height=55)
            Label(self.canva, text='Item', font=('Sans 17 bold'),
                  fg='gray53', bg='white').place(x=180, y=370)
            Label(self.canva, text='Price', font=('Sans 17 bold'),
                  fg='gray53', bg='white').place(x=760, y=370)

            i = 0  # first check for PIZZAS ################
            self.pizza_logo2 = PhotoImage(file='img/pizza_logo2.png')
            self.drinks_logo2 = PhotoImage(file='img/drinks_logo2.png')
            self.meals_logo2 = ImageTk.PhotoImage(
                Image.open('img/meals_logo2.jpg'))
            for p in self.dict:
                if self.dict[p][1]['R'] == 1 or self.dict[p][1]['M'] == 1 or self.dict[p][1]['L'] == 1:
                    size = ''
                    price = 0
                    if self.dict[p][1]['R'] == 1:
                        size += ' R'
                        price += 205
                    if self.dict[p][1]['M'] == 1:
                        size += ' M'
                        price += 385
                    if self.dict[p][1]['L'] == 1:
                        size += ' L'
                        price += 595
                    self.canva.create_oval(
                        50, 430+60*i, 82, 466+60*i, fill='brown3', outline='gold', width=4)
                    if i >= 9:
                        Label(self.canva, text=str(i+1), bg='brown3', fg='snow',
                              font=('Sans 10 bold')).place(x=56, y=437+60*i)
                    else:
                        Label(self.canva, text=str(i+1), bg='brown3', fg='snow',
                              font=('Sans 10 bold')).place(x=60, y=437+60*i)
                    Label(self.canva, text=self.dict[p][0], font=(
                        'Sans 15 bold'), bg='white', fg='gray4').place(x=100, y=430+60*i)  # name
                    self.canva.create_image(
                        450, 440+60*i, image=self.pizza_logo2)  # logo ####
                    Label(self.canva, text=size, font=('Helvetica 11 bold italic')).place(
                        x=550, y=432+60*i)  # size ##
                    Label(self.canva, text='\u0024 '+str(price),
                          font=('Times 15 bold'), bg='white').place(x=766, y=430+60*i)
                    i += 1

            for d in self.D:  # drinks #################
                if self.D[d][0] == True:
                    self.canva.create_oval(
                        50, 430+60*i, 82, 466+60*i, fill='brown3', outline='gold', width=4)
                    if i >= 9:
                        Label(self.canva, text=str(i+1), bg='brown3', fg='snow',
                              font=('Sans 10 bold')).place(x=56, y=437+60*i)
                    else:
                        Label(self.canva, text=str(i+1), bg='brown3', fg='snow',
                              font=('Sans 10 bold')).place(x=60, y=437+60*i)
                    Label(self.canva, text=self.D[d][1], font=(
                        'Sans 15 bold'), bg='white', fg='gray4').place(x=100, y=430+60*i)  # name
                    self.canva.create_image(
                        450, 440+60*i, image=self.drinks_logo2)  # logo ####
                    Label(self.canva, text='\u0024 '+str(self.D[d][2]), font=(
                        'Times 15 bold'), bg='white').place(x=766, y=430+60*i)
                    i += 1

            for m in self.M:  # meals ##############
                if self.M[m][0] == True:
                    self.canva.create_oval(
                        50, 430+60*i, 82, 466+60*i, fill='brown3', outline='gold', width=4)
                    if i >= 9:
                        Label(self.canva, text=str(i+1), bg='brown3', fg='snow',
                              font=('Sans 10 bold')).place(x=56, y=437+60*i)
                    else:
                        Label(self.canva, text=str(i+1), bg='brown3', fg='snow',
                              font=('Sans 10 bold')).place(x=60, y=437+60*i)
                    Label(self.canva, text=self.M[m][1], font=(
                        'Sans 15 bold'), bg='white', fg='gray4').place(x=100, y=430+60*i)  # name
                    self.canva.create_image(
                        450, 440+60*i, image=self.meals_logo2)  # logo ####
                    Label(self.canva, text='\u0024 '+str(self.M[m][2]), font=(
                        'Times 15 bold'), bg='white').place(x=766, y=430+60*i)
                    i += 1

            Label(self.canva, text='TOTAL', font=('Sans 17 bold'),
                  bg='white', fg='gray2').place(x=100, y=430+60*i)
            Label(self.canva, text='\u0024 '+str(self.TOTAL), font=('Sans 17 bold'),
                  bg='white', fg='gray2').place(x=760, y=430+60*i)

            self.po = Label(self.canva, text='Place Order',
                            bg='firebrick3', fg='gold', font=('Sans 15 bold'))
            self.po.bind('<Button-1>', lambda val='1': self.place_order('1'))
            self.po.place(x=1100, y=400, width=130, height=40)


    def place_order(self, val):
        if not len(self.he.get()) or not len(self.se.get()) or not len(self.ce.get()):
            messagebox.showinfo(
                'Missing Details', 'Please provide address details for successelful delivery of your order.')
            self.payment_window('1')
        else:
            messagebox.showinfo('Order placed', 'Dear '+self.NAME+' ,your order has been successelfully placed.\nIt will be delivered to ' +
                                self.he.get()+','+self.se.get()+','+self.ce.get()+' in under an hour.\nThank you !')

x = Main()
del(s)
