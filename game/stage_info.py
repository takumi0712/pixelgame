import pyxel
from background import Background
import math

class Stage:

    def __init__(self):
        self.maxStage = 4
        self.current = 0
        self.text_y = 0
        self.changeing = 0
        self.clearTheGame = False
        self.clearStage_list = []
        for i in range(self.maxStage):
            self.clearStage_list.append(False)
        self.bg = Background(7)

    def update(self):
        self.bg.update()
        if self.changeing ==  0:
            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
                if self.current != self.maxStage-1:
                    self.current += 1
                    self.changeing = -190
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
                if self.current != 0:
                    self.current -= 1
                    self.changeing = 190
            self.current = max(self.current,0)
            self.current = min(self.current,self.maxStage-1)
        else:
            if self.changeing >= 1:
                self.text_y += 10
                self.changeing -= 10
            elif self.changeing <= 1:
                self.text_y -= 10
                self.changeing += 10
    def draw(self):
        self.bg.draw_stars()
        pyxel.circ(210, 24, 10, 0)
        for i in range(self.maxStage):
            s = "STAGE {}".format(i+1)
            pyxel.blt(70,self.text_y+80+i*190,2,72,0,72,16,4)
            pyxel.blt(150,self.text_y+80+i*190,2,144+i*16,0,16,16,4)
            if self.clearStage_list[i]:
                s = "{}".format("\ CLEAR!! /")
                pyxel.text(96,self.text_y+70+i*190,s,11)
        if self.current != self.maxStage-1:
            pyxel.blt(112,178+math.sin(pyxel.frame_count* 0.05+3) * 2,2,16,48,16,8,4)
        if self.current != 0:
            pyxel.blt(112,8+math.sin(pyxel.frame_count* 0.05) * 2,2,16,48,16,-8,4)

    def clearStage(self):
        self.clearTheGame = False
        self.clearStage_list[self.current] = True