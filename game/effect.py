import random
import pyxel

effect_list = []
statusEffect =[]

############画面エフェクト###############

class ScreenEffect:
    def __init__(self,bg):
        self.vibrationTime = 0
        self.virusTime = 0
        self.healingTime = 0
        self.pwoer = 2
        self.bg = bg


    def update(self,p):
        self.vibration(p)
        self.item(p)
        self.update_statusEffect()

    def update_statusEffect(self):
        statusEffect.clear()
        if 0 < self.virusTime:
            statusEffect.append(216)
        if 0 < self.healingTime:
            statusEffect.append(208)
            

    def draw(self):
        cnt = 0
        for i in statusEffect:
            pyxel.blt(74+cnt,4,2,i,248,8,8,4)
            cnt += 8 

    def vibration(self,p):
        if 0 < self.vibrationTime:
            if self.vibrationTime%4==0:
                self.bg.m_x += self.pwoer
                p.p_x += self.pwoer
            elif self.vibrationTime%4==2:
                self.bg.m_x -= self.pwoer
                p.p_x -= self.pwoer
        self.vibrationTime -= 1

    def item(self,p):
        if 0 < self.virusTime:
            if p.count%180 == 0:
                p.hp -= 1
                self.vibrationTime = 8
                self.pwoer = 1
                self.virusTime -= 1
        if 0 < self.healingTime:
            if p.count%180 == 0:
                p.hp += 1
                p.hp = min(p.hp,30)
                self.healingTime -= 1

    def vibration_set(self,time,pwoer):
        self.vibrationTime = time
        self.pwoer = pwoer


#############エフェクト#############

class Effect(object):
    def __init__(self,bg,x,y):
        self.x = x
        self.y = y
        self.bg = bg
        self.alive = True
        self.lifespan = 0
        effect_list.append(self)

    def update(self):
        self.lifespan -= 1
        if self.lifespan == 0:
            self.alive = False

    def draw(self):
        pass

class ClearGateClose(Effect):
    def __init__(self, bg,ss, x, y):
        super().__init__(bg, x, y)
        self.ss = ss
        self.lifespan = 1
        self.count = 0
        self.gateClose = 0
        self.lamp_y = 0
    def update(self):
        self.count += 1
        if self.gateClose < 12:
            if self.count % 3 == 0:
                self.gateClose += 1
        if self.count > 110:
            if self.count % 5 == 4:
                self.lamp_y -= 16
        if self.count == 400:
            self.ss.clearTheGame = True
            self.alive = False

    def draw(self):
        pyxel.blt(self.bg.m_x+self.x-19+self.gateClose,self.bg.m_y+self.y-23,2,224,16,16,24,4)
        pyxel.blt(self.bg.m_x+self.x+18-self.gateClose,self.bg.m_y+self.y-23,2,240,16,16,24,4)
        if self.count > 100:
            pyxel.rect(self.bg.m_x+self.x-18,self.bg.m_y+self.y-38+self.lamp_y,5,7,10)
            pyxel.rect(self.bg.m_x+self.x-17,self.bg.m_y+self.y-37+self.lamp_y,3,5,11)
            pyxel.rect(self.bg.m_x+self.x+27,self.bg.m_y+self.y-38+self.lamp_y,5,7,10)
            pyxel.rect(self.bg.m_x+self.x+28,self.bg.m_y+self.y-37+self.lamp_y,3,5,11)
        if self.count > 200:
            pyxel.rect(0,58,256,23,0)
            pyxel.blt(76,60,2,16,32,80,16,4)

class Burst(Effect):
    def __init__(self,bg,x,y):
        super().__init__(bg, x, y)
        self.lifespan = 3
        self.x += self.bg.m_x
        self.y += self.bg.m_y

    def draw(self):
        pyxel.circb(self.x,self.y,1+3-self.lifespan,9)

class Slash(Effect):
    def __init__(self,bg,x,y):
        super().__init__(bg, x, y)
        self.lifespan = 0
        if random.random() >= 0.5:
            self.random_w = 1
        else:
            self.random_w = -1
        if random.random() >= 0.5:
            self.random_h = 1
        else:
            self.random_h = -1


    def update(self):
        if self.bg.count % 2 == 0:
            self.lifespan += 1
        if self.lifespan == 4:
            self.alive = False

    def draw(self):
        pyxel.blt(self.bg.m_x+self.x-8,self.bg.m_y+self.y-4,2,192+(16*self.lifespan),64,16*self.random_w,16*self.random_h,4)

class Healing(Effect):
    def __init__(self,bg,x,y):
        super().__init__(bg, x, y)
        self.lifespan = 20


    def draw(self):
        pyxel.circ(self.bg.m_x+self.x,self.bg.m_y+self.lifespan + self.y,1,11)
        pyxel.circ(self.bg.m_x+self.x+3,self.bg.m_y+self.lifespan + self.y+4,1,11)
        pyxel.pset(self.bg.m_x+self.x+5,self.bg.m_y+self.lifespan + self.y+1,11)

class WormholeClose(Effect):
    def __init__(self,bg,x,y):
        super().__init__(bg, x, y)
        self.lifespan = 0

    def update(self):
        if self.bg.count % 2 == 0:
            self.lifespan += 1
        if self.lifespan == 7:
            self.alive = False

    def draw(self):
        pyxel.blt(108,100,2,192-(self.lifespan*16),16,16,24,4)


class explosion(Effect):
    def __init__(self,bg,x,y):
        super().__init__(bg, x, y)
        self.lifespan = 0

    def update(self):
        if self.bg.count % 2 == 0:
            self.lifespan += 1
        if self.lifespan == 7:
            self.alive = False

    def draw(self):
        if self.lifespan < 2:
            pyxel.blt(self.bg.m_x+self.x,self.bg.m_y+self.y,2,128+(self.lifespan*16),40,16,16,4)
        else:
            pyxel.blt(self.bg.m_x+self.x-3,self.bg.m_y+self.y-4,2,112+(self.lifespan*24),40,24,24,4)