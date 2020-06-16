# -*- coding: utf-8 -*-
'''
@Descripttion: 
@Version: 
@Author: neuhxy
@Date: 2020-06-16 16:44:46
@LastEditors: neuhxy
@LastEditTime: 2020-06-16 16:48:01
'''


# 定义所有的Pizzas数据
pizzas_data = [
    {
        'id': 1,
        'name': 'Margherita',
        'img': 'img/Margherita.jpg',
        'price': 10,
        'type': 'regular',
        'content': 'Fresh tomato, mozzarella, fresh basil, parmesan'
    },
    {
        'id': 2,
        'name': 'Kiwi',
        'img': 'img/Kiwi.jpg',
        'price': 10,
        'type': 'regular',
        'content': 'Bacon, egg, mozzarella'
    },
    {
        'id': 3,
        'name': 'Garlic',
        'img': 'img/Garlic.jpg',
        'price': 10,
        'type': 'regular',
        'content': 'Mozzarella, garlic'
    },
    {
        'id': 4,
        'name': 'Cheese',
        'img': 'img/Cheese.jpg',
        'price': 10,
        'type': 'regular',
        'content': 'Mozzarella, oregano'
    },
    {
        'id': 5,
        'name': 'Hawaiian',
        'img': 'img/Hawaiian.jpg',
        'price': 10,
        'type': 'regular',
        'content': 'Ham, pineapple, mozzarella'
    },
    {
        'id': 6,
        'name': 'Mediterranean (vegan)',
        'img': 'img/Mediterranean (vegan).jpg',
        'price': 10,
        'type': 'regular',
        'content': 'Lebanese herbs, olive oil, fresh tomatoes, olives, onion'
    },
    {
        'id': 7,
        'name': 'Meat',
        'img': 'img/Meat.jpg',
        'price': 17,
        'type': 'gourmet',
        'content': 'Bacon, pancetta, ham, onion, pepperoni, mozzarella'
    },
    {
        'id': 8,
        'name': 'Chicken Cranberry',
        'img': 'img/Chicken Cranberry.jpg',
        'price': 17,
        'type': 'gourmet',
        'content': 'Smoked chicken, cranberry, camembert mozzarella'
    },
    {
        'id': 9,
        'name': 'Satay Chicken',
        'img': 'img/Satay Chicken.jpg',
        'price': 17,
        'type': 'gourmet',
        'content': 'Smoked chic, onions, capsicum, pine nuts, satay sauce, mozzarella Chilli flakes and dried basil'
    },
    {
        'id': 10,
        'name': 'Big BBQ Bacon',
        'img': 'img/Big BBQ Bacon.jpg',
        'price': 17,
        'type': 'gourmet',
        'content': 'Smoky Bacon served on our classic marinara tomato sauce, heaped with mozzarella, topped off with a sweet and tangy BBQ drizzle'
    },
    {
        'id': 11,
        'name': 'Veggie',
        'img': 'img/Veggie.jpg',
        'price': 17,
        'type': 'gourmet',
        'content': 'sweet red onion, mushroom, red capsicum & melting mozzarella with drizzles of our tangy roast capsicum drizzle, finished with a dash of oregano.'
    },
    {
        'id': 12,
        'name': 'Meatlovers',
        'img': 'img/Meatlovers.jpg',
        'price': 17,
        'type': 'gourmet',
        'content': 'Spicy pepperoni, Italian sausage, succulent ham, seasoned ground beef and crispy bacon all piled onto classic marinara sauce and finished with cheesy mozzarella and a drizzle of BBQ sauce.'
    }
]


class Pizza:
    '''
    Pizza 类
    '''
    def __init__(self, id, name,type, img, price, content):
        self.id = id
        self.name = name
        self.type = type
        self.img = img
        self.price = price
        self.content = content
    
    # def get_pizza(self, key, value):
    #     ''' 根据条件查找pizza数据 '''
    #     keys = self.__dict__
    #     print(keys)
    #     return [p for p in pizzas if keys['p.{}'.format(key)] == value]



class Order:
    '''
    @description: 
    @param : 
    @return: 
    '''
    def __init__(self, id, uid, name, email, tel, items, house_no, street, city, pizzas_price, delivery_fee, total, time):
        self.id = id                        # 订单ID
        self.uid = uid                      # 客户ID
        self.name = name                    # 客户姓名
        self.email = email                  # 客户邮箱
        self.tel = tel                      # 客户电话
        self.items = items                  # Pizza信息
        self.house_no = house_no            # 房间号 
        self.street = street                # 街道
        self.city = city                    # 城市
        self.pizzas_price = pizzas_price    # Pizza 总价
        self.delivery_fee = delivery_fee    # 配送费
        self.total = total                  # 订单总价
        self.time = time                    # 下单时间



class Item:
    '''
    @description: 
    @param : 
    @return: 
    '''
    def __init__(self, id, uid, pizza, amount, price):
        self.pizza = pizza
        self.amount = amount
        self.price = price
