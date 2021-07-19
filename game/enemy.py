import pyxel

import random

from effect import *
from item import Bullet
from player import *

enemy_list=[]

def CollisionDetectionAttack(p,bg):
    for enemy in enemy_list:
        for attack in attack_list:
            if (
                attack.x + attack.w > bg.m_x+enemy.x
                and bg.m_x+enemy.x + enemy.w > attack.x
                and attack.y + attack.h > bg.m_y+enemy.y
                and bg.m_y+enemy.y + enemy.h > attack.y
            ):
                if enemy.invincibleTime == 0:
                    enemy.hp -= attack.atk
                    enemy.invincibleTime =30
                    if enemy.hp > 0:
                        Slash(bg,enemy.x+random.randint(0,enemy.w-2),enemy.y+random.randint(0,enemy.h-2))

def enemySet(bg, p, ef, stage):
    enemy_list.clear()
    if stage.current == 0:
        Turret(bg,p,ef,260,12)
        Turret2(bg,p,ef,300,100)
        MoveLeftAndRightTurret(bg,p,ef,770,-50)
        MoveLeftAndRightTurret(bg,p,ef,870,-50)
        MoveLeftAndRightTurret(bg,p,ef,1000,-50)
        TrackingTurret(bg,p,ef,1410,-150)
    elif stage.current == 1:
        MoveLeftAndRightTurret(bg,p,ef,80,80)
        Turret(bg,p,ef,120,100)
        Turret(bg,p,ef,140,100)
        Turret(bg,p,ef,160,100)
        Turret(bg,p,ef,180,100)
        Turret(bg,p,ef,200,100)
        TrackingTurret(bg,p,ef,201,100)
    elif stage.current == 2:
        TrackingTurret(bg,p,ef,200,100)
    elif stage.current == 3:
        pass
        

class Enemy(object):
    def __init__(self,bg,p,ef,x,y):
        self.bg = bg
        self.x = x
        self.y = y
        self.hp = 0
        self.w = 0
        self.h = 0
        self.p = p
        self.ef = ef
        self.alive = True
        self.invincibleTime = 0
        enemy_list.append(self)

    def update(self):
        if self.invincibleTime > 0:
            self.invincibleTime -= 1

    def draw(self):
        pass

class Turret(Enemy):
    def __init__(self, bg, p, ef, x, y):
        super().__init__(bg, p, ef, x, y)
        self.w = 7
        self.h = 8
        self.hp = 10
    def update(self):
        super().update()
        if self.bg.count %30 == 0:
            Bullet(self.bg,self.p,self.ef,self.x+3,self.y+6,2,40,1)
        if self.hp <= 0:
            self.alive = False
            explosion(self.bg,self.x+2,self.y-2)
            pyxel.play(0,8)
    def draw(self):
        pyxel.blt(self.bg.m_x+self.x,self.bg.m_y+self.y,2,0,248,self.w,self.h,4)

class Turret2(Enemy):
    def __init__(self, bg, p, ef, x, y):
        super().__init__(bg, p, ef, x, y)
        self.w = 7
        self.h = 8
        self.hp = 10
    def update(self):
        super().update()
        if self.bg.count %30 == 0:
            Bullet(self.bg,self.p,self.ef,self.x+3,self.y,-2,40,1)
        if self.hp <= 0:
            self.alive = False
            explosion(self.bg,self.x+2,self.y-2)
            pyxel.play(0,8)
    def draw(self):
        pyxel.blt(self.bg.m_x+self.x,self.bg.m_y+self.y,2,0,248,self.w,-self.h,4)
class MoveLeftAndRightTurret(Turret):
    def update(self):
        if self.bg.count%100 < 50:
            self.x += 1
        else:
            self.x -= 1
        return super().update()

    def draw(self):
        if self.bg.count % 6 < 3:
            pyxel.blt(self.bg.m_x+self.x,self.bg.m_y+self.y,2,8,248,7,3,4)
        else:
            pyxel.blt(self.bg.m_x+self.x,self.bg.m_y+self.y,2,8,248,-7,3,4)
        pyxel.blt(self.bg.m_x+self.x,self.bg.m_y+self.y+3,2,8,251,7,5,4)

class TrackingTurret(MoveLeftAndRightTurret):
    def __init__(self, bg, p, ef, x, y):
        super().__init__(bg, p, ef, x, y)
        self.distance_x = 0
        self.distance_y = 0
        self.w = 15
        self.h = 12
        self.speed_x = 1
        self.speed_y = 1
        self.attackMode = False
        self.attackCount = 0
        self.standbyAttackCount = 0
        self.hp = 30

    def update(self):
        if self.standbyAttackCount > 0:
            self.standbyAttackCount -= 1
        if self.invincibleTime > 0:
            self.invincibleTime -= 1
        if self.hp <= 0:
            self.alive = False
            explosion(self.bg,self.x+2,self.y-2)
            pyxel.play(0,8)
        if not self.attackMode:
            self.distance_x = int(108 - (self.bg.m_x+self.x))
            self.distance_y = int(80 - (self.bg.m_y+self.y))
            if self.distance_x > 0:
                self.x += self.speed_x
            elif self.distance_x < 0:
                self.x -= self.speed_x
                
            if self.distance_y > 0:
                self.y += self.speed_y
            elif self.distance_y < 0:
                self.y -= self.speed_y

            if self.distance_x == 0 and self.distance_y == 0:
                self.standbyAttackCount += 2
                if self.standbyAttackCount == 60:
                    self.attackMode = True
        else:
            self.attackCount += 1
            if self.attackCount == 30:
                Bullet(self.bg,self.p,self.ef,self.x+7,self.y+9,2,17,3)
            elif self.attackCount == 80:
                self.attackCount = 0
                self.attackMode = False

    def draw(self):
        if self.bg.count % 6 < 3:
            pyxel.blt(self.bg.m_x+self.x-1,self.bg.m_y+self.y,2,8,248,7,3,4)
            pyxel.blt(self.bg.m_x+self.x+9,self.bg.m_y+self.y,2,8,248,7,3,4)
        else:
            pyxel.blt(self.bg.m_x+self.x-1,self.bg.m_y+self.y,2,8,248,-7,3,4)
            pyxel.blt(self.bg.m_x+self.x+9,self.bg.m_y+self.y,2,8,248,-7,3,4)
        pyxel.blt(self.bg.m_x+self.x,self.bg.m_y+self.y+3,2,16,248,16,8,4) 
        if self.attackMode:
            pyxel.pset(self.bg.m_x+self.x+7,self.bg.m_y+self.y-2,9)
            pyxel.line(self.bg.m_x+self.x+7,self.bg.m_y+self.y-4,self.bg.m_x+self.x+7,self.bg.m_y+self.y-6,9)

