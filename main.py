from tkinter import *
from PIL import ImageTk, Image
from math import *
import os

#http://www.michurin.net/online-tools/solar-system.html
#http://www.allplanets.ru/solar_sistem.htm


Menu_open = False

class planet():
    """
    Класс,который описывает планеты
    """
    def __init__(self,Planet, name, r, BIG, x=640, y=360):
        """
        Конструктор класса planet
        Args:
            x, y - координаты планеты
            Planet - изображение планеты, которое вращается вокруг солнца
            name - название планеты
            BIG - изображение планеты в меню
            r -радиус, для проверки выхода за границы окна программы
        """
        self.x = x
        self.y = y
        self.angle = 0  #переменная для перевода угла вращения планеты
        self.i = 0 #начальный угол вращения планеты

        self.BIG = BIG
        
        self.r = r//2
        self.title = str(name)
        self.Planet_sprite = canvas.create_image(self.x,self.y,image=Planet)
        
    def animate(self, Planet, rass, speed):
        """
        Метод анимирующий планеты путем их вращения вокруг солнца
        Args:
            Planet - изображение планеты, которое вращается
            rass - расстояние от точки вращения до этой планеты, используется для позиционирования 
            speed - скорость перемещения
        """
        global Menu_open, mnoz
        if Menu_open == False: #если меню с информацией о планетах закрыто, то планеты вращаются 
            canvas.delete(self.Planet_sprite)
            if self.i <= 360: # здесь мы ставим ограничения для значения угла, что-бы не получить ошибку.
                self.angle = self.i * (3.14 / 180) # перевод из градусов в радианы
                self.x = rass * cos(self.angle) + 0
                self.y = rass * sin(self.angle) + 360
                self.i += speed*mnoz #увеличиваем угол перемещения.
            else:
                self.i = speed*mnoz
                self.angle = self.i * (3.14 / 180) 
                self.x = rass * cos(self.angle) + 0
                self.y = rass * sin(self.angle) + 360
            if self.y > 720+self.r or 83 < self.i: # перемещаем планету наверх, когда она уйдет за края экрана
                self.i = -80          
            self.Planet_sprite = canvas.create_image(self.x,self.y,image=Planet) 
            canvas.tag_bind(self.Planet_sprite, "<1>", self.change) #привязываем левую кнопку мыши к планете. При нажатии вызываетя метод change класса planet
            root.after(10, self.animate, Planet,rass, speed) #повторяем анимацию
    def change(self,event):
        """
        Метод обрабатывающий нажатие на планеты. Он создает меню, где представлены сразу все планеты и информация о них
        """
        global Menu_p
        Menu_p = menu(Menu_BG, self) #создаем меню с информацией о планетах

    def cheking(self, event):
        """
        Метод обрабатывает вывод инофрмации об этой планете в меню
        """
        global Planet_Mercury_menu, Predidushaya_planeta
        #Ниже мы удаляем все, что было в меню
        canvas.delete(Menu_p.bigtitle)
        canvas.delete(Menu_p.bigsprite)
        canvas.delete(Menu_p.biginfo)
        canvas.delete(Menu_p.biginfo2)
        canvas.delete(self.sp)
        canvas.delete(self.rec)
        canvas.delete(self.spt)
        canvas.delete(Predidushaya_planeta.sp)
        canvas.delete(Predidushaya_planeta.rec)
        canvas.delete(Predidushaya_planeta.spt)
        #а теперь выводим информацию о выбранной планете, а также выделяем её в меню (меняя фон на белый)
        self.rec = round_rectangle(Menu_p.start_x+self.n*(Menu_p.start_s+Menu_p.start_ras), Menu_p.start_y, Menu_p.start_x+Menu_p.start_s+self.n*(Menu_p.start_s+Menu_p.start_ras), Menu_p.start_y+Menu_p.start_s, radius=20, fill="#ebebeb")
        self.sp = canvas.create_image(Menu_p.sp_sz_x+self.n*(Menu_p.start_s+Menu_p.start_ras), Menu_p.sp_sz_y,image=self.menu,anchor=CENTER)
        self.spt = canvas.create_text(Menu_p.tx_sz_x+self.n*(Menu_p.start_s+Menu_p.start_ras),Menu_p.tx_sz_y+6,text = self.title,anchor=CENTER,font = "Verdana 14", fill="#212121")
        Menu_p.bigtitle = canvas.create_text(320-220,26+340//3,text = self.title,anchor="nw",font = "Verdana 40 bold", fill="#e2e2e2")
        Menu_p.bigsprite = canvas.create_image(640, 98+340//2,image=self.BIG,anchor=CENTER)
        Menu_p.biginfo = canvas.create_text(320-220,30+340//2,text = self.info,anchor="nw",font = "Verdana 15", fill="#e2e2e2")        
        Menu_p.biginfo2 = canvas.create_text(320+510,30+340//2,text = self.info2,anchor="nw",font = "Verdana 13", fill="#e2e2e2")
        canvas.tag_bind(self.rec, "<Button-1>",self.cheking)
        canvas.tag_bind(self.sp, "<Button-1>",self.cheking)
        canvas.tag_bind(self.spt, "<Button-1>",self.cheking)
        
        if Predidushaya_planeta != self: #здесь мы исключаем повторное нажатие на уже выбранную планету 
            Predidushaya_planeta.rec = round_rectangle(Menu_p.start_x+Predidushaya_planeta.n*(Menu_p.start_s+Menu_p.start_ras), Menu_p.start_y, Menu_p.start_x+Menu_p.start_s+Predidushaya_planeta.n*(Menu_p.start_s+Menu_p.start_ras), Menu_p.start_y+Menu_p.start_s, radius=20, fill="#262626", stipple="gray50")
            Predidushaya_planeta.sp = canvas.create_image(Menu_p.sp_sz_x+Predidushaya_planeta.n*(Menu_p.start_s+Menu_p.start_ras), Menu_p.sp_sz_y,image=Predidushaya_planeta.menu,anchor=CENTER)
            Predidushaya_planeta.spt = canvas.create_text(Menu_p.tx_sz_x+Predidushaya_planeta.n*(Menu_p.start_s+Menu_p.start_ras),Menu_p.tx_sz_y+6,text = Predidushaya_planeta.title,anchor=CENTER,font = "Verdana 14", fill="#e2e2e2")
            canvas.tag_bind(Predidushaya_planeta.rec, "<Button-1>",Predidushaya_planeta.cheking)
            canvas.tag_bind(Predidushaya_planeta.sp, "<Button-1>",Predidushaya_planeta.cheking)
            canvas.tag_bind(Predidushaya_planeta.spt, "<Button-1>",Predidushaya_planeta.cheking)
            Predidushaya_planeta = self
        
class menu():
    """
    Класс отвественный за меню со списком всех планет и информацией о них
    """
    def __init__(self, bg, click_planet, x=640, y=360):
        """
        Конструктор класса menu
        Args:
            bg - фон меню планет
            click_planet - планета, по нажатию на которую было вызвано меню
            x, y - координаты фона меню планет 
        """
        global Menu_open, Planet_Mercury_menu, Planet_Earth_BIG, Mercury
        Menu_open = True
        self.x = x #координаты фона меню планет
        self.y = y
        self.Menu_BG = canvas.create_image(self.x,self.y,image=bg) #задаем фон меню
        
        global Predidushaya_planeta 
        Predidushaya_planeta = click_planet #выводим информацию о той планете, по которой нажали, и тем самым вызвали меню 

        #координаты для создания плиток
        self.start_x = start_x = 50 
        self.start_y = start_y = 530
        self.start_s = start_s = 130
        self.start_ras = start_ras = 20
        self.sp_sz_x = sp_sz_x = start_x+start_s//2
        self.sp_sz_y = sp_sz_y = start_y+start_s//4
        self.tx_sz_x = tx_sz_x = start_x+start_s//2
        self.tx_sz_y = tx_sz_y = start_y+start_s//2+start_s//4
        
        self.Back_button = canvas.create_text(start_x,start_y+start_s+25,text = '< Вернуться к модели',anchor=W,font = "Verdana 14", fill="#707070") #кнопка выхода из меню
        canvas.tag_bind(self.Back_button, "<1>", self.close) #при нажатии на кнопку выхода из меню выполняется метод close класса menu


        #Ниже мы создаем информацию о выбранной планете: большое изображение, название, информация
        self.bigsprite = canvas.create_image(640, 98+340//2,image=click_planet.BIG,anchor=CENTER)
        self.bigtitle = canvas.create_text(320-220,26+340//3,text = click_planet.title,anchor="nw",font = "Verdana 40 bold", fill="#e2e2e2")
        self.biginfo = canvas.create_text(320-220,30+340//2,text = click_planet.info,anchor="nw",font = "Verdana 15", fill="#e2e2e2")
        self.biginfo2 = canvas.create_text(320+510,30+340//2,text = click_planet.info2,anchor="nw",font = "Verdana 13", fill="#e2e2e2")

        #Ниже мы создаем "плитки", где находятся маленькие изображения планет и их названия.Также при нажатии на эти плитки вызывается метод cheking класса planet 
        Mercury.n = 0 #номер плитки, который используется при расчете её координат
        Mercury.rec, Mercury.sp, Mercury.spt = self.Plitki(Mercury.menu,'Меркурий', Mercury.n , start_x, start_y, start_s, start_ras, sp_sz_x, sp_sz_y, tx_sz_x, tx_sz_y)
        canvas.tag_bind(Mercury.rec, "<Button-1>",Mercury.cheking)
        canvas.tag_bind(Mercury.sp, "<Button-1>",Mercury.cheking)
        canvas.tag_bind(Mercury.spt, "<Button-1>",Mercury.cheking)
        Venus.n = 1
        Venus.rec, Venus.sp, Venus.spt = self.Plitki(Venus.menu,'Венера', Venus.n , start_x, start_y, start_s, start_ras, sp_sz_x, sp_sz_y, tx_sz_x, tx_sz_y)
        canvas.tag_bind(Venus.rec, "<Button-1>",Venus.cheking)
        canvas.tag_bind(Venus.sp, "<Button-1>",Venus.cheking)
        canvas.tag_bind(Venus.spt, "<Button-1>",Venus.cheking)
        Earth.n = 2
        Earth.rec, Earth.sp, Earth.spt = self.Plitki(Earth.menu,'Земля', 2 , start_x, start_y, start_s, start_ras, sp_sz_x, sp_sz_y, tx_sz_x, tx_sz_y)
        canvas.tag_bind(Earth.rec, "<Button-1>",Earth.cheking)
        canvas.tag_bind(Earth.sp, "<Button-1>",Earth.cheking)
        canvas.tag_bind(Earth.spt, "<Button-1>",Earth.cheking)
        Mars.n = 3
        Mars.rec, Mars.sp, Mars.spt = self.Plitki(Mars.menu,'Марс', 3 , start_x, start_y, start_s, start_ras, sp_sz_x, sp_sz_y, tx_sz_x, tx_sz_y)
        canvas.tag_bind(Mars.rec, "<Button-1>",Mars.cheking)
        canvas.tag_bind(Mars.sp, "<Button-1>",Mars.cheking)
        canvas.tag_bind(Mars.spt, "<Button-1>",Mars.cheking)
        Jupiter.n = 4
        Jupiter.rec, Jupiter.sp, Jupiter.spt = self.Plitki(Jupiter.menu,'Юпитер', 4 , start_x, start_y, start_s, start_ras, sp_sz_x, sp_sz_y, tx_sz_x, tx_sz_y)
        canvas.tag_bind(Jupiter.rec, "<Button-1>",Jupiter.cheking)
        canvas.tag_bind(Jupiter.sp, "<Button-1>",Jupiter.cheking)
        canvas.tag_bind(Jupiter.spt, "<Button-1>",Jupiter.cheking)
        Saturn.n = 5
        Saturn.rec, Saturn.sp, Saturn.spt = self.Plitki(Saturn.menu,'Сатурн', 5 , start_x, start_y, start_s, start_ras, sp_sz_x, sp_sz_y, tx_sz_x, tx_sz_y)
        canvas.tag_bind(Saturn.rec, "<Button-1>",Saturn.cheking)
        canvas.tag_bind(Saturn.sp, "<Button-1>",Saturn.cheking)
        canvas.tag_bind(Saturn.spt, "<Button-1>",Saturn.cheking)
        Uranus.n = 6
        Uranus.rec, Uranus.sp, Uranus.spt = self.Plitki(Uranus.menu,'Уран', 6 , start_x, start_y, start_s, start_ras, sp_sz_x, sp_sz_y, tx_sz_x, tx_sz_y)
        canvas.tag_bind(Uranus.rec, "<Button-1>",Uranus.cheking)
        canvas.tag_bind(Uranus.sp, "<Button-1>",Uranus.cheking)
        canvas.tag_bind(Uranus.spt, "<Button-1>",Uranus.cheking)
        Neptune.n = 7
        Neptune.rec, Neptune.sp, Neptune.spt = self.Plitki(Neptune.menu,'Нептун', 7 , start_x, start_y, start_s, start_ras, sp_sz_x, sp_sz_y, tx_sz_x, tx_sz_y)
        canvas.tag_bind(Neptune.rec, "<Button-1>",Neptune.cheking)
        canvas.tag_bind(Neptune.sp, "<Button-1>",Neptune.cheking)
        canvas.tag_bind(Neptune.spt, "<Button-1>",Neptune.cheking)

        canvas.delete(Predidushaya_planeta.sp)
        canvas.delete(Predidushaya_planeta.rec)
        canvas.delete(Predidushaya_planeta.spt)
        Predidushaya_planeta.rec = round_rectangle(self.start_x+Predidushaya_planeta.n*(self.start_s+self.start_ras), self.start_y, self.start_x+self.start_s+Predidushaya_planeta.n*(self.start_s+self.start_ras), self.start_y+self.start_s, radius=20, fill="#ebebeb")
        Predidushaya_planeta.sp = canvas.create_image(self.sp_sz_x+Predidushaya_planeta.n*(self.start_s+self.start_ras), self.sp_sz_y,image=Predidushaya_planeta.menu,anchor=CENTER)
        Predidushaya_planeta.spt = canvas.create_text(self.tx_sz_x+Predidushaya_planeta.n*(self.start_s+self.start_ras),self.tx_sz_y+6,text = Predidushaya_planeta.title,anchor=CENTER,font = "Verdana 14", fill="#212121")
        
    def Plitki(self, image_p, text_p, n, start_x, start_y, start_s, start_ras, sp_sz_x, sp_sz_y, tx_sz_x, tx_sz_y ):
        """
        Метод создающий плитки с названием планет и их маленькими изображениями 
        Args:
            n - номер плитки, используется для вычисления её координаты
            start_x, start_y, start_s, start_ras, sp_sz_x, sp_sz_y, tx_sz_x, tx_sz_y - координаты для создания плиток   
        Returns:
            my_rectangle - id-ишник (уникальный идентификатор) прямоугольника
            sprite - id-ишник (уникальный идентификатор) маленького изображения планеты
            sprite_text - id-ишник (уникальный идентификатор) названия планеты
        """
        my_rectangle = round_rectangle(start_x+n*(start_s+start_ras), start_y, start_x+start_s+n*(start_s+start_ras), start_y+start_s, radius=20, fill="#262626", stipple="gray50")
        sprite = canvas.create_image(sp_sz_x+n*(start_s+start_ras), sp_sz_y,image=image_p,anchor=CENTER)
        sprite_text = canvas.create_text(tx_sz_x+n*(start_s+start_ras),tx_sz_y+6,text = text_p,anchor=CENTER,font = "Verdana 14", fill="#e2e2e2")
        return my_rectangle, sprite, sprite_text
                   
    def close(self,event):
        """
        Метод обрабатывает операцию закрытия меню планет
        """
        global Menu_open,Menu_p, Predidushaya_planet
        canvas.delete(Menu_p.Menu_BG, Menu_p.biginfo)
        Menu_open = False #переменная говорит теперь о том, что меню закрыто

        #Удаляем все,что было в меню
        canvas.delete(Predidushaya_planeta.sp)
        canvas.delete(Predidushaya_planeta.rec)
        canvas.delete(Predidushaya_planeta.spt) 
        canvas.delete(Mercury.rec, Mercury.sp, Mercury.spt)
        canvas.delete(Venus.rec, Venus.sp, Venus.spt)
        canvas.delete(Earth.rec, Earth.sp, Earth.spt)
        canvas.delete(Mars.rec, Mars.sp, Mars.spt)
        canvas.delete(Jupiter.rec, Jupiter.sp, Jupiter.spt)
        canvas.delete(Saturn.rec, Saturn.sp, Saturn.spt)
        canvas.delete(Uranus.rec, Uranus.sp, Uranus.spt)
        canvas.delete(Neptune.rec, Neptune.sp, Neptune.spt)       
        canvas.delete(self.Back_button, self.bigtitle, self.bigsprite, self.biginfo, self.biginfo2)

        #Снова анимируем планеты
        Mercury.animate(Planet_Mercury, Mercury_rass, 0.1)
        Venus.animate(Planet_Venus, Mercury_rass+100, 0.074)
        Earth.animate(Planet_Earth, Mercury_rass+200, (0.1*29.76)/47.87)
        Mars.animate(Planet_Mars, Mercury_rass+300, (0.1*24.13)/47.87)
        Jupiter.animate(Planet_Jupiter, Mercury_rass+430, (0.1*13.07)/47.87)
        Saturn.animate(Planet_Saturn, Mercury_rass+590, (0.1*9.67)/47.87)
        Uranus.animate(Planet_Uranus, Mercury_rass+700, (0.1*6.84)/47.87)
        Neptune.animate(Planet_Neptune, Mercury_rass+810, (0.1*5.48)/47.87)
        
class speed_changer():
    """
    Класс ответственный за меню с кнопками регулирования скорости вращения планет
    """
    def __init__(self, Plus_im, Mins_im, x=1210, y=40):
        """
        Конструктор класса speed_changer
        Args:
            Plus_im - изображение для кнопки увеличения скорости
            Mins_im - изображение для кнопки уменьшения скорости
            x, y - координаты, относительно которых происходит размещение остальных элементов
        """
        self.x = x #координаты на основе которых определяется положения кнопок и надписи
        self.y = y
        self.round_rectangle = round_rectangle(self.x-105, self.y-25, self.x+55, self.y+65, fill="#262626", stipple="gray50")
        self.sc_text = canvas.create_text(self.x-25,self.y-10,text = 'Скорость вращения:',anchor=CENTER,font = "Verdana 8 bold", fill="#ebebeb")
        self.plus_sprite = canvas.create_image(self.x-55,self.y+30,image=Plus_im)
        self.mins_sprite = canvas.create_image(self.x+5,self.y+30,image=Mins_im)    
        canvas.tag_bind(self.plus_sprite, "<1>", self.plus_speed)
        canvas.tag_bind(self.mins_sprite, "<1>", self.mins_speed)
        
    def plus_speed(self,event):
        """
        Метод обрабатывает нажатие на конпку "plus_sprite" и соот-но операцию увеличения скорости вращение планет
        """
        global mnoz
        if mnoz <= 8:  
            mnoz = mnoz * 2
            
    def mins_speed(self,event):
        """
        Метод обрабатывает нажатие на конпку "mins_sprite" и соот-но операцию уменьшения скорости вращение планет
        """
        global mnoz
        if mnoz >= 2:
            mnoz = mnoz / 2

def Open_img(file, xsize, ysize):
    """
    Функция открытия изображения и изменение его размера
    Args:
        file - путь к изображению
        xsize - размер по x
        ysize - размер по y
    Returns:
        Planet - изображение с измененными размерами
    """
    Planet = Image.open(file)
    Planet = Planet.resize((xsize, ysize), Image.ANTIALIAS)
    Planet = ImageTk.PhotoImage(Planet)
    return Planet

def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
    """
    Функция создания прямоугольника с закругленными краями
    Args:
        x1, y1, x2, y2 - координаты начальной точки и конечной точки для создания прямоугольника
        radius - радиус закругления краев
    Returns:
        canvas.create_polygon - id-ишник (уникальный идентификатор) прямоугольника 
    """
    points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2,  x2-radius, y2,  x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)
        
"""
Настройки основного окна
"""
root = Tk()
root.geometry('1280x720')
root.title("Order 66")
"""
Проверка os и использование соответствующей иконки приложения
"""
if "nt" == os.name: #Если Windows - устанавливаем иконку icon.ico
    root.wm_iconbitmap(bitmap = "icon.ico")
else: #Иначе - устанавливаем икноку icon.xbm
    root.wm_iconbitmap(bitmap = "@icon.xbm")

root.resizable(False, False)
canvas = Canvas(root,width=1280,height=720)
canvas.pack()
pilImage = Image.open("bg.png")
image = pilImage.resize((1280, 720), Image.ANTIALIAS)
image = ImageTk.PhotoImage(image)
imagesprite = canvas.create_image(640,360,image=image)

# Размеры Меркурия. Все остальные планеты зависят от этих значений
size_x = 20
size_y = 20
Mercury_rass = 370
Mercury_x = 640

"""
Большие изображения планет, которые выводятся при нажатии по планете в меню
"""
Mercury_BIG = Open_img("Mercury.png", 340,340)
Venus_BIG = Open_img("Venus.png", 340,340)
Earth_BIG = Open_img("Earth.png", 340,340)
Mars_BIG = Open_img("Mars.png", 340,340)
Jupiter_BIG = Open_img("Jupiter.png", 340,340)
Saturn_BIG = Open_img("Saturn.png", 340,340)
Uranus_BIG = Open_img("Uranus.png", 340,340)
Neptune_BIG = Open_img("Neptune.png", 340,340)

#Создаем планеты
Planet = Open_img("Sun.png", 800 ,800)
Sun = planet(Planet,"Sun",800, Mercury_BIG, -100,360)

mnoz = 1 #глобальная переменная с помощью которой меняем сокрость вращения всех планет
Plus_im = Open_img("plus.png", 50 , 50) 
Mins_im = Open_img("mins.png", 50 , 50)
Sp_ch = speed_changer(Plus_im, Mins_im)

Mercury_speed = 0.1 #Скорость самой медленной планеты от которой зависят и скорости остальных планет

"""
Добавление изображений для планет, а также анимация движения и установка размеров 
""" 
Planet_Mercury = Open_img("Mercury.png", size_x,size_y) 
Mercury = planet(Planet_Mercury,"Меркурий", size_x, Mercury_BIG, Mercury_x, 360)
Mercury.animate(Planet_Mercury, Mercury_rass, Mercury_speed)

Planet_Venus = Open_img("Venus.png", int(size_x*2.45),int(size_y*2.45)) 
Venus = planet(Planet_Venus,"Венера", int(size_x*2.45), Venus_BIG, Mercury_x+100, 360)
Venus.animate(Planet_Venus, Mercury_rass+100, (Mercury_speed*35.02)/47.87)

Planet_Earth = Open_img("Earth.png", int(size_x*6378/2440),int(size_y*6378/2440)) 
Earth = planet(Planet_Earth,"Земля", int(size_x*6378/2440), Earth_BIG, Mercury_x+200, 360)
Earth.animate(Planet_Earth, Mercury_rass+200, (Mercury_speed*29.76)/47.87)

Planet_Mars = Open_img("Mars.png", int(size_x*3397/2440),int(size_y*3397/2440)) 
Mars = planet(Planet_Mars,"Марс", int(size_x*3397/2440), Mars_BIG, Mercury_x+300, 360)
Mars.animate(Planet_Mars, Mercury_rass+300, (Mercury_speed*24.13)/47.87)

Planet_Jupiter = Open_img("Jupiter.png", int(size_x*17872/2440),int(size_y*17872/2440)) 
Jupiter = planet(Planet_Jupiter,"Юпитер", int(size_x*17872/2440), Jupiter_BIG, Mercury_x+400, 360)
Jupiter.animate(Planet_Jupiter, Mercury_rass+430, (Mercury_speed*13.07)/47.87)

Planet_Saturn = Open_img("Saturn.png", int(size_x*18000/2440),int(size_y*18000/2440)) 
Saturn = planet(Planet_Saturn,"Сатурн", int(size_x*18000/2440), Saturn_BIG, Mercury_x+500, 360)
Saturn.animate(Planet_Saturn, Mercury_rass+590, (Mercury_speed*9.67)/47.87)

Planet_Uranus = Open_img("Uranus.png", int(size_x*6390/2440),int(size_y*6390/2440)) 
Uranus = planet(Planet_Uranus,"Уран", int(size_x*6390/2440), Uranus_BIG, Mercury_x+600, 360)
Uranus.animate(Planet_Uranus, Mercury_rass+700, (Mercury_speed*6.84)/47.87)

Planet_Neptune = Open_img("Neptune.png",  int(size_x*6190/2440),int(size_y*6190/2440))
Neptune = planet(Planet_Neptune,"Нептун", int(size_x*6190/2440), Neptune_BIG, Mercury_x+700, 360)
Neptune.animate(Planet_Neptune, Mercury_rass+810, (Mercury_speed*5.48)/47.87)

"""
Фон меню планет 
""" 
Menu_BG = Image.open("BG_Planet.png")
Menu_BG = Menu_BG.resize((1280, 720), Image.ANTIALIAS)
Menu_BG = ImageTk.PhotoImage(Menu_BG)

"""
Маленькие изображения планет в меню
"""
Mercury.menu = Open_img("Mercury.png", 100,100)
Venus.menu = Open_img("Venus.png", 100,100)
Earth.menu = Open_img("Earth.png", 100,100)
Mars.menu = Open_img("Mars.png", 100,100)
Jupiter.menu = Open_img("Jupiter.png", 100,100)
Saturn.menu = Open_img("Saturn.png", 150,150)
Uranus.menu = Open_img("Uranus.png", 100,100)
Neptune.menu = Open_img("Neptune.png", 100,100)

"""
Информация о планетах, отображаемая слева от их большого изображения
"""
Mercury.info = 'Ближайшая к Солнцу планета \nСолнечной системы, наименьшая\nиз планет земной группы.\nНазвана в честь древнеримского\nбога — быстрого Меркурия,\nпоскольку она движется по небу\nбыстрее других планет'
Venus.info = 'Вторая по удалённости\nот Солнца планета, наряду с\nМеркурием, Землёй и Марсом\nпринадлежащая к семейству\nпланет земной группы.\nНазвана в честь древнеримской\nбогини любви Венеры'
Earth.info = 'Третья по удалённости от Солнца\nпланета Солнечной системы.\nСамая плотная и пятая по\nдиаметру и массе среди всех\nпланет и крупнейшая среди\nпланет земной группы'
Mars.info = 'Четвёртая по удалённости от\nСолнца и седьмая по размерам\nпланета Солнечной системы.\nНазвана в честь Марса\n— древнеримского бога войны'
Jupiter.info = 'Крупнейшая планета, \nпятая по удалённости от Солнца.\nНаряду с Сатурном, Ураном и\nНептуном классифицируется\nкак газовый гигант'
Saturn.info = 'Шестая планета от Солнца и\nвторая по размерам планета\nпосле Юпитера. Сатурн, а\nтакже Юпитер, Уран и Нептун,\nявляются планетами-гигантами.'
Uranus.info = 'Планета седьмая по удалённости\nот Солнца, третья по диаметру\nи четвёртая по массе.\nНазвана в честь греческого\nбога неба Урана.'
Neptune.info = 'Восьмая и самая дальняя от\nЗемли планета. По диаметру\nнаходится на четвёртом месте,\nа по массе — на третьем.\nПланета была названа в честь\nримского бога морей.'

"""
Информация о планетах, отображаемая справа от их большого изображения
"""
Mercury.info2 = 'Большая полуось, млн.км:\n57,909\nСкорость движения по орбите, км/сек:\n47,87\nСредняя плотность, г/куб.см:\n5,43 \nСостав атмосферы:\nВодород, гелий, кислород, \nпары кальция, натрий, калий\nСредняя температура:\n167°'
Venus.info2 = 'Большая полуось, млн.км:\n108,21\nСкорость движения по орбите, км/сек:\n35,02\nСредняя плотность, г/куб.см:\n5,24 \nСостав атмосферы:\nУглекислый газ, азот, вода \nСредняя температура:\n464°'
Earth.info2 = 'Большая полуось, млн.км:\n149,60\nСкорость движения по орбите, км/сек:\n29,76\nСредняя плотность, г/куб.см:\n5,515 \nСостав атмосферы:\nАзот, кислород, аргон \nСредняя температура:\n15°'
Mars.info2 = 'Большая полуось, млн.км:\n227,94\nСкорость движения по орбите, км/сек:\n24,13\nСредняя плотность, г/куб.см:\n3,94 \nСостав атмосферы:\nУглекислый газ, азот, аргон \nСредняя температура:\n-65°'
Jupiter.info2 = 'Большая полуось, млн.км:\n778,41\nСкорость движения по орбите, км/сек:\n13,07\nСредняя плотность, г/куб.см:\n1,33  \nСостав атмосферы:\nВодород, гелий \nСредняя температура:\n-110°'
Saturn.info2 = 'Большая полуось, млн.км:\n14294\nСкорость движения по орбите, км/сек:\n9,67\nСредняя плотность, г/куб.см:\n0,69 \nСостав атмосферы:\nВодород, гелий \nСредняя температура:\n-140°'
Uranus.info2 = 'Большая полуось, млн.км:\n28710\nСкорость движения по орбите, км/сек:\n6,84\nСредняя плотность, г/куб.см:\n1,30 \nСостав атмосферы:\nВодород, гелий, метан \nСредняя температура:\n-195°'
Neptune.info2 = 'Большая полуось, млн.км:\n44983\nСкорость движения по орбите, км/сек:\n5,48\nСредняя плотность, г/куб.см:\n1,64 \nСостав атмосферы:\nВодород, гелий, метан \nСредняя температура:\n-225°'

root.mainloop()
