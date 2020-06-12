from tkinter import *
from PIL import ImageTk, Image
class Main:
    def __init__(self, parent):
        
        WIDTH = 1366
        HEIGHT = 768
        num_cols = 4
        num_rows = 2
        
        regular_name = ['Margherita', 'Kiwi', 'Garlic', 'Cheese', 'Hawaiian', 'Mediterranean (vegan)']
        regular_img = ['img/Kiwi.jpg', 'img/Kiwi.jpg', 'img/Garlic.jpg', 'img/Cheese.jpg',
                       'img/Hawaiian.jpg', 'img/Mediterranean (vegan).jpg']
        gourment_name = ['Meat', 'Chicken Cranberry', 'Satay Chicken', 'Big BBQ Bacon', 'Veggie', 'Meatlovers']
        gourment_img = ['img/Meat.jpg', 'img/Chicken Cranberry.jpg', 'img/Satay Chicken.jpg', 'img/Big BBQ Bacon.jpg'
   , 'img/Veggie.jpg', 'img/Meatlovers.jpg']

        #创建顶部工具栏的frame
        self.frame1 = Frame(parent, bg="linen", padx=30, width = WIDTH, height = 30)
        self.frame1.grid(row = 0, columnspan = 7)
        #welcome label
        welcome_label = Label(self.frame1, text = "Welcome, ", bg = "linen")
        welcome_label.grid(row=0, column=0, sticky = W, pady = 1)
        #logout button
        logout_btn = Button(self.frame1, text = "Log out", bg = "linen")
        logout_btn.grid(row=0, column=1, sticky = W, pady = 1)
        #regular pizza menu button
        regular_btn = Button(self.frame1, text = "Regular pizzas ", bg = "linen")
        regular_btn.grid(row=0, column=2, sticky = W, pady = 1)
        #gourmet pizza menu button
        gourmet_btn = Button(self.frame1, text = "Gourmet pizzas", bg = "linen")
        gourmet_btn.grid(row=0, column=3, sticky = W, pady = 1)
        #check out button
        checkout_btn = Button(self.frame1, text = "Checkout", bg = "linen")
        checkout_btn.grid(row=0, column=4, sticky = W, pady = 1)
        #cart button
        cart_btn = Button(self.frame1, text = "CART", bg = "linen")
        cart_btn.grid(row=0, column=5, sticky = W, pady = 1)
        #total button
        total_label = Label(self.frame1, text = "Total = ", bg = "linen")
        total_label.grid(row=0, column=6, sticky = W, pady = 1)

    
        #工具栏下方的整个frame        
        self.frame2 = Frame(parent, bg="linen", width = WIDTH, height = 500)
        self.frame2.grid(row = 1, columnspan = 4)
        #每个商品的小frame
        self.product_frame = []
        for i in range(len(regular_name)):
            self.product_frame.append(Frame(self.frame2, bg="linen", width = WIDTH, height = 50))
        frame_count = 0
        for c in range(num_cols):
            for r in range(num_rows):
                if frame_count < len(regular_name):
                    self.product_frame[frame_count].grid(row = r, column = c)
                    frame_count += 1
        #每个pizza的名字和图片
        self.name_label = ['']*len(regular_name)
        self.img_label = []
        for i in range(len(regular_name)):
             self.name_label[i] = Label(self.product_frame[i], text = regular_name[i])
             self.name_label[i].grid(row = 0, column = 0, sticky = 'e', pady = 5)
            
             self.img_label[i] = Label(self.product_frame[i], image = PhotoImage(file = regular_img[i]))
             self.img_label[i].grid(row = 2, column = 1)     
        
#main
if __name__ == '__main__':
    root = Tk()
    buttons = Main(root)
    root.title ("Heavenly Pizza GUI Ordering System")
    root.mainloop()