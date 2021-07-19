import pyxel
import random

class Background:
    def __init__(self,current):
        self.stars=((65,13),(75,200),(48,108),(130,30),(164,100),(180,5),(195,155),(233,70),(150,185))
        self.bigStars=((60,40),(100,50),(180,25),(80,100),(200,150),(230,130),(160,80),(30,150))
        self.bigStars2=((20,45),(140,95),(75,180))
        self.smallStars=((10,40),(15,104),(22,60),(26,80),(28,30),(32,82),(32,33),(36,84),(47,64),(70,40),(80,80))
        self.count = 0
        self.shootingStar_x = 80
        self.shootingStar_y = 100
        self.shootingStarDraw = False
        self.shootingStarTime = 0
        self.shootingStarFrame = 0
        self.shootingStarFlow = ((0,0),(0,5),(0,11),(2,18),(5,20),(13,21),(17,22),(23,23))
        self.current = current
        self.m_x = 0
        self.m_y = 0

    def update(self):
        self.count += 1
        self.update_stars()


    def draw(self):
        self.draw_stars()
        pyxel.bltm(self.m_x,self.m_y-1900,self.current,0,0,256,256,4)

    def update_stars(self):
        #600フレームに一回流れ星を描写
        if self.count % 600 == 599:
            self.shootingStarDraw = True
        if self.shootingStarDraw:
            if self.count%2 == 0:
                self.shootingStarFrame += 1
            if self.shootingStarFrame ==8:
                self.shootingStarFrame=0
                self.shootingStar_x = random.randint(25,240)
                self.shootingStar_y = random.randint(0,192)
                self.shootingStarDraw = False
    def draw_stars(self):
        #月
        pyxel.circ(215, 22, 15, 15)
        pyxel.circ(210, 24, 10, 4)
        #星
        for i in self.stars:
            pyxel.pset(i[0],i[1],15)
            if self.count%100 <= 20 or self.count%100>=90:
                pyxel.pset(i[0]+1,i[1],7)
                pyxel.pset(i[0]-1,i[1],7)
                pyxel.pset(i[0],i[1]+1,7)
                pyxel.pset(i[0],i[1]-1,7)
            if self.count%100 <= 10:
                pyxel.pset(i[0]+1,i[1],8)
                pyxel.pset(i[0]-1,i[1],8)
                pyxel.pset(i[0],i[1]+1,8)
                pyxel.pset(i[0],i[1]-1,8)
        #小さい星
        for i in self.smallStars:
            pyxel.pset(i[0],i[1],6)
            if self.count%150 <= 10:
                pyxel.pset(i[0],i[1],7)
        #流れ星
        if self.shootingStarDraw:
            pyxel.line(self.shootingStar_x-self.shootingStarFlow[self.shootingStarFrame][0],\
                self.shootingStar_y+self.shootingStarFlow[self.shootingStarFrame][0]\
                    ,self.shootingStar_x-self.shootingStarFlow[self.shootingStarFrame][1],\
                        self.shootingStar_y+self.shootingStarFlow[self.shootingStarFrame][1],15)
            
        #大きい星
        for i in self.bigStars:
            pyxel.pset(i[0],i[1],15)
            if self.count%120 <= 40 or self.count%120>=110:
                pyxel.pset(i[0]+1,i[1],8)
                pyxel.pset(i[0]-1,i[1],8)
                pyxel.pset(i[0],i[1]+1,8)
                pyxel.pset(i[0],i[1]-1,8)
            if self.count%120 <= 30:
                pyxel.pset(i[0]+2,i[1],7)
                pyxel.pset(i[0]-2,i[1],7)
                pyxel.pset(i[0],i[1]+2,7)
                pyxel.pset(i[0],i[1]-2,7)
                
        for i in self.bigStars2:
            pyxel.pset(i[0],i[1],15)
            if self.count%120 >= 60:
                pyxel.pset(i[0]+1,i[1]+1,8)
                pyxel.pset(i[0]-1,i[1]+1,8)
                pyxel.pset(i[0]+1,i[1]-1,8)
                pyxel.pset(i[0]-1,i[1]-1,8)
            if self.count%120 >= 80 and self.count%120 <=100:
                pyxel.pset(i[0]+2,i[1]+2,7)
                pyxel.pset(i[0]-2,i[1]+2,7)
                pyxel.pset(i[0]+2,i[1]-2,7)
                pyxel.pset(i[0]-2,i[1]-2,7)
