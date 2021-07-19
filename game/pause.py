import pyxel

pauseContents = ("RESUME","SELECT SCREEN","QUIT THE GAME")

class PauseModal:
    def __init__(self):
        self.selecting = 0
        self.pause = False
        self.x = -100
        self.y = 100
        self.count = 0
        self.out = False
        self.gamemodeChange = False

    def update(self):
        if self.count < 60:
            self.count += 1
            self.x = int(fade(self.count,-100,170,60))
        else:
            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S) and not self.out:
                self.selecting += 1
                pyxel.play(0,6)
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W) and not self.out:
                self.selecting -= 1
                pyxel.play(0,6)
            self.selecting = max(self.selecting,0)
            self.selecting = min(self.selecting,len(pauseContents)-1)

            if pyxel.btnp(pyxel.KEY_ESCAPE):
                self.out = True
                pyxel.play(0,3)

            if pyxel.btnp(pyxel.KEY_ENTER) or pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                pyxel.play(0,3)
                if self.selecting == 0:
                    self.out = True
                elif self.selecting == 1:
                    self.pause = False
                    self.gamemodeChange = True
                elif self.selecting == 2:
                    pyxel.quit()
            if self.out:
                self.count += 1
                self.x = int(fade(self.count,-100,170,50))
                if self.count > 110:
                    self.pause = False
    
    def draw(self):
        pyxel.blt(self.x+14,self.y-30,2,0,0,72,16,4)
        pyxel.rect(self.x+17,self.y+1,66,30,0)
        pyxel.line(self.x+16,self.y,self.x+84,self.y,0)
        for i in range(len(pauseContents)):
            pyxel.line(self.x+14,self.y+2+10*i,self.x+85,self.y+2+10*i,0)
            pyxel.line(self.x+17,self.y+3+10*i,self.x+82,self.y+3+10*i,0)
            pyxel.line(self.x+15,self.y+4+10*i,self.x+84,self.y+4+10*i,0)
            pyxel.line(self.x+16,self.y+5+10*i,self.x+83,self.y+5+10*i,0)
            pyxel.line(self.x+14,self.y+6+10*i,self.x+85,self.y+6+10*i,0)
            pyxel.line(self.x+16,self.y+7+10*i,self.x+83,self.y+7+10*i,0)
            pyxel.line(self.x+15,self.y+8+10*i,self.x+84,self.y+8+10*i,0)
            pyxel.line(self.x+13,self.y+10+10*i,self.x+83,self.y+10+10*i,0)
            pyxel.line(self.x+16,self.y+11+10*i,self.x+84,self.y+11+10*i,0)
            if self.selecting == i:
                pyxel.line(self.x+20,self.y+6+i*10,self.x+21+len(pauseContents[i])*4,self.y+5+i*10,9)
                pyxel.line(self.x+19,self.y+7+i*10,self.x+20+len(pauseContents[i])*4,self.y+6+i*10,9)
            pyxel.text(self.x+21,self.y+2+i*10,pauseContents[i],8)
            pyxel.text(self.x+20,self.y+2+i*10,pauseContents[i],15)

def fade(time, begin, change, duration):
  return -change * (( time / duration - 1)**4- 1) + begin
