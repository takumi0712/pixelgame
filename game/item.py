from typing import Tuple
from effect import *
import pyxel
import math
import random

item_list = []
# stage1
POSION_LIST1=((65,80),(1080,-60))
VIRUS_LIST1=((40,80),(-140,80))

def itemSet(bg, player, ef, stage):
    item_list.clear()
    if stage.current == 0:
        for i in POSION_LIST1:
            Potion(bg,i[0],i[1],player, ef)
        for i in VIRUS_LIST1:
            Virus(bg,i[0],i[1],ef)
        launchPad(bg, 689, 69, player)
        Wormhole(bg, 1112, 0, ef, -1210, 230)
        Syringe(bg,80,80,player)
        ClearGate(bg,stage,player,1992,123)

def CollisionDetection(p,bg):
    for item in item_list:
            if (
                p.hitbox_x + p.hitbox_w > bg.m_x+item.x
                and bg.m_x+item.x + item.w > p.hitbox_x
                and p.hitbox_y + p.hitbox_h > bg.m_y+item.y
                and bg.m_y+item.y + item.h > p.hitbox_y
            ):
                item.action()
        
#############アイテム#############
class Item(object):
    def __init__(self, bg, x, y):
        self.alive = True
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.u = 0
        self.v = 0
        self.bg = bg
        item_list.append(self)
        self.random = random.randint(0,60)

    def update(self):
        pass

    def draw(self):
        pyxel.blt(self.bg.m_x+self.x,self.bg.m_y+self.y+math.sin((self.bg.count+self.random) * 0.05) * 2,2,self.u,self.v,self.w,self.h,4)

class Potion(Item):
    def __init__(self, bg, x, y, player, ef):
        super().__init__(bg, x, y)
        self.player = player
        self.u = 4
        self.v = 19
        self.w = 7
        self.h = 11
        self.ef = ef
    def action(self):
        pyxel.play(0,5)
        self.ef.healingTime = 5
        self.ef.virusTime = 0
        self.alive = False
        Healing(self.bg,self.x+2,self.y-10)

class Syringe(Item):
    def __init__(self, bg, x, y, player):
        super().__init__(bg, x, y)
        self.player = player
        self.u = 0
        self.v = 32
    def action(self):
        pyxel.play(0,5)
        self.player.hp += 5
        self.player.hp = min(self.player.hp,30)
        self.alive = False
        Healing(self.bg,self.x+2,self.y-10)


class Virus(Item):
    def __init__(self, bg, x, y, ef):
        super().__init__(bg, x, y)
        self.ef = ef
        self.u = 19
        self.v = 19
        self.w = 9
        self.h = 9
    def action(self):
        pyxel.play(0,7)
        self.ef.virusTime = 5
        self.alive = False

#############設置物#############

class ClearGate(Item):
    def __init__(self, bg, ss, p, x, y):
        super().__init__(bg, x, y)
        self.x = x+10
        self.ss = ss
        self.w = 2
        self.h = 1
        self.p = p

    def update(self):
        pass

    def action(self):
        if 0 < self.p.hitbox_x - (self.bg.m_x+self.x):
            self.p.p_speed = 0
            self.p.canMove = False
            ClearGateClose(self.bg,self.ss,self.x,self.y)
            self.alive = False

    def draw(self):
        pyxel.rect(self.bg.m_x+self.x-5,self.bg.m_y+self.y-23,26,24,0)
        pyxel.blt(self.bg.m_x+self.x-19,self.bg.m_y+self.y-23,2,224,16,16,24,4)
        pyxel.blt(self.bg.m_x+self.x+18,self.bg.m_y+self.y-23,2,240,16,16,24,4)

class Wormhole(Item):
    def __init__(self, bg, x, y, ef, wx, wy):
        super().__init__(bg, x, y)
        self.ef = ef
        self.u = 176
        self.wx = wx
        self.wy = wy
        self.w = 2
        self.h = 2
        self.warp = False
        self.count = 0
    def update(self):
        if self.count > 0:
            self.count -= 1
        if self.bg.count % 30 <= 10:
            self.u = 208
        elif self.bg.count % 30 <= 20:
            self.u = 192
        elif self.bg.count % 30 <= 30:
            self.u = 176
    def action(self):
        self.count+=2
        if self.count > 64:
                self.bg.m_x = self.wx
                self.bg.m_y = self.wy
                WormholeClose(self.bg,self.wx,self.wy)
                self.count = 0
    def draw(self):
        if self.count > 0:
            pyxel.rect(self.bg.m_x+self.x-7,self.bg.m_y+self.y-13,16,1,2)
            pyxel.rect(self.bg.m_x+self.x-7,self.bg.m_y+self.y-13,self.count//4,1,10)
        pyxel.blt(self.bg.m_x+self.x-7,self.bg.m_y+self.y-11,2,self.u,16,16,24,4)

class launchPad(Item):
    def __init__(self, bg, x, y, player):
        super().__init__(bg, x, y)
        self.u = 32
        self.v = 16
        self.player = player
        self.spring = False

    def update(self):
        if self.bg.count % 200 < 134:
            self.u = 32
        elif self.bg.count % 200 <= 137:
            self.u = 48
            self.spring = True
        elif self.bg.count % 200 <= 145:
            self.u = 64
        else:
            self.u = 80
            self.spring = False

    def action(self):
        if self.spring:
            self.player.vy = -4
    def draw(self):
        pyxel.blt(self.bg.m_x+self.x,self.bg.m_y+self.y,2,self.u,self.v,16,16,4)

#############敵の攻撃#############

class Bullet:
    def __init__(self, bg, p, ef, x, y, direction, lifespan, power):
        self.x = x
        self.y = y
        self.w = power+1
        self.h = power//2+1
        self.power = power
        self.alive = True
        self.direction = direction
        self.count = 0
        self.lifespan = lifespan
        self.bg = bg
        self.p = p
        self.ef = ef
        if abs(self.direction)==2:
            self.h,self.w = self.w,self.h
        if self.direction < 0:
            if abs(self.direction)==2:
                self.y -= self.h//2
            else:
                self.x -= self.w//2
        item_list.append(self)

    def action(self):
        self.alive = False
        self.p.hp -= self.power
        self.p.invincibleTime_set(30)
        self.ef.vibration_set(8,self.power//2+1)
        if self.power >= 10:
            pyxel.play(0, 2)
        elif self.power >= 5:
            pyxel.play(0, 1)
        else:
            pyxel.play(0, 0)
        Burst(self.bg,self.x,self.y)

    def update(self):
        if abs(self.direction)==1:
            self.x += 2*self.direction
        if abs(self.direction)==2:
            self.y += 2*(self.direction/2)
        self.count += 1
        if self.count > self.lifespan:
            self.alive = False

    def draw(self):
        pyxel.rect(self.bg.m_x+self.x,self.bg.m_y+self.y, self.w, self.h, 9)
