#pyhton 3.8.8
# pyxel 1.4.3

# 操作方法　
#  左に移動 = A
#  右に移動 = D
#  ダッシュ = AorD + shift
#  スライディング = ダッシュ中に control
#  しゃがみ = S
#  左クリック = 攻撃
#  ジャンプ = space
#  ジャンプ攻撃 = ジャンプ中に左クリック


import pyxel
from enum import Enum

from background import Background
from player import *
import message
from stage_info import Stage
from pause import PauseModal
import item
import enemy
import effect


#ゲームモード状態
class GameMode(Enum):
    START          = 1
    GAMEPLAY       = 2
    STAGESELECT    = 3

class App:
    def __init__(self):
        # 初期化
        pyxel.init(240, 192, caption="pixelsword",
        palette=[0x000000,
                 0xdcdcdc, 
                 0x4b4b4b, 
                 0x171717, 
                 0x1e2430,
                 0x414855, 
                 0x49505f, 
                 0x676487, 
                 0xb4b2e0, 
                 0xeb00f5, 
                 0xc1f0f9,
                 0x00faff, 
                 0xffecee, 
                 0xccc7e4,
                 0xf49b39,
                 0xffffff],
                fps=60,
                fullscreen=False,
                quit_key=pyxel.KEY_F4
                 )
        pyxel.mouse(True) 
        # ゲームモード初期化
        self.game_mode = GameMode.START

        self.count = 0
        self.ss = Stage()
        self.ps = PauseModal()
        # イメージバンク読み込み
        try:
            pyxel.load("assets/resource.pyxres")
            pyxel.image(1).load(0,0,"assets/player.png")
            pyxel.image(2).load(0,0,"assets/anything.png")
        except:
            pyxel.quit()

        # please press enter を点滅させる
        self.colCount = 0
        # 実行
        pyxel.run(self.update, self.draw)

    def update(self):
        self.count += 1

        if self.game_mode == GameMode.START:
            # please press enter を点滅させる
            self.colCount = self.colCount + 1
            if self.colCount % 64 <= 32:
                self.isTitleTextDraw = True
            else:
                self.isTitleTextDraw = False
            
            # エンター押したらシーン切り替え
            if pyxel.btnr(pyxel.KEY_ENTER) or pyxel.btnr(pyxel.MOUSE_LEFT_BUTTON):
                self.game_mode = GameMode.STAGESELECT

        if self.game_mode == GameMode.STAGESELECT:
            
            self.ss.update()
            if pyxel.btnp(pyxel.KEY_ENTER) or pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                self.bg = Background(self.ss.current)
                self.ef = effect.ScreenEffect(self.bg)
                self.player1 = Player(self.ss.current,self.bg)
                # self.player1 = God(self.ss.current,self.bg)
                enemy.enemySet(self.bg,self.player1,self.ef,self.ss)
                item.itemSet(self.bg,self.player1,self.ef,self.ss)
                self.game_mode = GameMode.GAMEPLAY

        if self.game_mode == GameMode.GAMEPLAY:

            if not self.ps.pause:
                self.bg.update()
                item.CollisionDetection(self.player1,self.bg)
                enemy.CollisionDetectionAttack(self.player1,self.bg)
                self.ef.update(self.player1)
                update_list_onscreen(self.bg,enemy.enemy_list)
                update_list(item.item_list)
                update_list(effect.effect_list)
                update_list(attack_list)
                cleanup_list(enemy.enemy_list)
                cleanup_list(item.item_list)
                cleanup_list(effect.effect_list)
                cleanup_list(attack_list)
                if self.player1.alive:
                    if self.ss.clearTheGame:
                        self.ss.clearStage()
                        self.game_mode = GameMode.STAGESELECT
                    self.player1.update()
                    if pyxel.btnp(pyxel.KEY_ESCAPE):
                        pyxel.play(0,4)
                        self.ps.__init__()
                        self.ps.pause = True
                else:
                    if pyxel.btnp(pyxel.KEY_ENTER) or pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                        self.ef.__init__(self.bg)
                        item.itemSet(self.bg,self.player1,self.ef,self.ss)
                        enemy.enemySet(self.bg,self.player1,self.ef,self.ss)
                        self.bg.m_y = 0
                        self.bg.m_x = 0
                        self.player1.__init__(self.ss.current,self.bg)
                        self.bg.__init__(self.ss.current)
            else:
                self.ps.update()
                if self.ps.gamemodeChange:
                    self.game_mode = GameMode.STAGESELECT

            

    def draw(self):

        if self.game_mode == GameMode.START:
            # 画面を消去
            pyxel.cls(0)
            pyxel.blt(10,40,2,32,88,224,32,4)
            # 描画
            if self.isTitleTextDraw:
                pyxel.text(85,130,"please press enter",15)

        if self.game_mode == GameMode.STAGESELECT:
            pyxel.cls(0)
            self.ss.draw()

        if self.game_mode == GameMode.GAMEPLAY:
            pyxel.cls(4)
            self.bg.draw()
            draw_list(enemy.enemy_list)
            draw_list(item.item_list)
            draw_list(attack_list)
            self.player1.draw()
            draw_list(effect.effect_list)
            self.ef.draw()

            if not self.player1.alive:
                message.draw_gameover()
            if self.ps.pause:
                self.ps.draw()
            

def update_list(list):
    for elem in list:
        elem.update()

############描画画面＋縦横左右16pixel分の範囲だけupdate############
def update_list_onscreen(bg,list):
    for elem in list:
        if (bg.m_x + elem.x > -16
            and 272 > bg.m_x+elem.x
            and bg.m_y + elem.y > -16
            and 208 > bg.m_y + elem.y
        ):
            elem.update()

def draw_list(list):
    for elem in list:
        elem.draw()

def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
        else:
            i += 1

if __name__ == '__main__':
    App()   