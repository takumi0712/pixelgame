from effect import Healing
import pyxel
from enum import Enum
import math

attack_list = []

# プレイヤー状態
class PlayerState(Enum):
    STAND          = 1
    WALK           = 2
    JUMP           = 3
    DIE            = 4
    FALL           = 5
    SQUAT          = 6
    SLIDING        = 7
    JUMPATTACK     = 8
    ATTACK1        = 9


class Player:

    p_walkImg = ((0,0),(0,24),(0,48),(0,72),(0,96),(0,120),(0,144),(0,168),(0,192),(0,216))
    p_standImg = ((24,0),(24,24),(24,48),(24,72))
    p_jumpattackImg = ((168,24,24,1,0,5),(168,24,24,1,0,5),(192,32,32,9,-2,-22))
    p_attack1Img = ((56,24),(80,24),(104,24),(128,32),(152,32))
    def __init__(self,referenceMap,bg):
        self.player_state = PlayerState.STAND # プレイヤー状態初期化
        self.p_img = 0 # プレイヤーの画像
        self.p_img2 = 0
        self.p_imgPosition = 0
        self.p_x = 100 #プレイヤー初期ｘ座標
        self.p_y = 100 #プレイヤー初期ｙ座標
        self.p_direction = 1 #プレイヤー方向
        self.p_detectionPosition = 14
        self.count = 0 #キーボード入力時間カウント
        self.vy = 0 # Y方向の速度
        self.gravity = 0.1
        self.inversion = 1
        self.m_xblock = 0
        self.m_yblock = 0
        self.p_speed = 0
        self.p_maxSpeed = 2
        self.jumpCount = 0
        self.alive = True
        self.hp = 30
        self.stamina = 59
        self.hpColor = 11
        self.hasStamina = True
        self.hitbox_x = 0
        self.hitbox_y = 0
        self.hitbox_w = 0
        self.hitbox_h = 0
        self.slidingCount = 0
        self.referenceMap = referenceMap
        self.bg = bg
        self.invincibleTime = 0
        self.attack1Count = 0
        self.jumpattackCount = -1
        self.atk = 10
        self.canMove = False

    def update(self):
        # 1/60秒毎に1ずつ増える
        self.count += 1
        if self.count == 30:
            self.canMove = True
        # スタミナ回復
        self.stamina += 0.1
        self.stamina = min(self.stamina,59)
        self.stamina = max(self.stamina,0)
        self.hasStamina = True

        # hitbox
        if self.player_state == PlayerState.WALK:
            self.hitbox_x,self.hitbox_y = 110,106
            self.hitbox_w,self.hitbox_h = 14,18
        elif self.player_state == PlayerState.STAND:
            self.hitbox_x,self.hitbox_y = 112,103
            self.hitbox_w,self.hitbox_h = 11,21
        elif self.player_state == PlayerState.SQUAT:
            self.hitbox_x,self.hitbox_y = 109,109
            self.hitbox_w,self.hitbox_h = 16,15
            self.stamina +=0.1
        elif self.player_state == PlayerState.SLIDING:
            self.hitbox_x,self.hitbox_y,self.hitbox_w,self.hitbox_h = 0,0,0,0
        elif self.player_state == PlayerState.JUMP:
            self.hitbox_x,self.hitbox_y = 112,102
            self.hitbox_w,self.hitbox_h = 10,22
        elif self.player_state == PlayerState.FALL:
            self.hitbox_x,self.hitbox_y = 110,103
            self.hitbox_w,self.hitbox_h = 13,21
        elif self.player_state == PlayerState.JUMPATTACK:
            self.hitbox_x,self.hitbox_y = 109,107
            self.hitbox_w,self.hitbox_h = 16,17
        elif self.player_state == PlayerState.ATTACK1:
            if self.p_direction == 1:
                self.hitbox_x,self.hitbox_y = 102,109
                self.hitbox_w,self.hitbox_h = 15,15
            else:
                self.hitbox_x,self.hitbox_y = 115,109
                self.hitbox_w,self.hitbox_h = 15,15
        if self.invincibleTime > 0:
            self.hitbox_x,self.hitbox_y,self.hitbox_w,self.hitbox_h = 0,0,0,0
            self.invincibleTime -= 1

        ############### 押し戻し処理###############
        #上
        if pyxel.tilemap(self.referenceMap).get(self.m_xblock+15,self.m_yblock+250) >=192 or pyxel.tilemap(self.referenceMap).get(self.m_xblock+14,self.m_yblock+250) >=192:
            if self.vy < 0:
                self.vy = 0
                self.jumpCount = 0
        
        if self.p_speed < 0:
            # 右
            if pyxel.tilemap(self.referenceMap).get(self.m_xblock+15,self.m_yblock+252) >=192:
                self.bg.m_x += 1
            if pyxel.tilemap(self.referenceMap).get(self.m_xblock+16,self.m_yblock+252) <192 and pyxel.tilemap(self.referenceMap).get(self.m_xblock+16,self.m_yblock+251) <192 and pyxel.tilemap(self.referenceMap).get(self.m_xblock+16,self.m_yblock+250) <192:
                self.bg.m_x += self.p_speed
            else:
                if 4-(self.bg.m_x%8) < 0:
                    self.bg.m_x += self.p_speed
                else:
                    self.p_speed = 0
                    self.bg.m_x += 4-(self.bg.m_x%8)
        else:
            #左
            if pyxel.tilemap(self.referenceMap).get(self.m_xblock+14,self.m_yblock+252) >=192:
                self.bg.m_x -= 1
            if pyxel.tilemap(self.referenceMap).get(self.m_xblock+13,self.m_yblock+252) <192 and pyxel.tilemap(self.referenceMap).get(self.m_xblock+13,self.m_yblock+251) <192 and pyxel.tilemap(self.referenceMap).get(self.m_xblock+13,self.m_yblock+250) <192:
                self.bg.m_x += self.p_speed
            else:
                if (self.bg.m_x%8)-6 < 0:
                    self.bg.m_x += self.p_speed
                else:
                    self.p_speed = 0
                    self.bg.m_x -= (self.bg.m_x%8)-6

        # 速度を更新
        self.bg.m_y -= self.vy
        if not self.player_state == PlayerState.JUMPATTACK:
            if self.vy > 0:
                self.player_state = PlayerState.FALL
            elif self.vy < 0:
                self.player_state = PlayerState.JUMP

        # スピードの範囲
        self.p_speed = max(self.p_speed,-self.p_maxSpeed)
        self.p_speed = min(self.p_speed,self.p_maxSpeed)

        # スピード減衰
        if self.player_state == PlayerState.STAND:
            self.p_speed = 0
        elif self.player_state == PlayerState.JUMP or self.player_state == PlayerState.FALL:
            if self.p_speed > 0 :
                self.p_speed -= 0.04
            elif self.p_speed < 0:
                self.p_speed += 0.04
        elif self.player_state == PlayerState.WALK:
            if self.p_speed > 0:
                self.p_speed -= 0.1
            elif self.p_speed < 0:
                self.p_speed += 0.1

        self.m_xblock = self.bg.m_x/-8
        self.m_yblock = self.bg.m_y/-8

        if pyxel.tilemap(self.referenceMap).get(self.m_xblock+self.p_detectionPosition,self.m_yblock+253)>=192 or pyxel.tilemap(self.referenceMap).get(self.m_xblock+self.p_detectionPosition+self.p_direction,self.m_yblock+253)>=192:
            self.vy = 0
            if self.bg.m_y%8 != 0:
                self.bg.m_y += 8-(self.bg.m_y%8)
                self.bg.m_y = math.floor(self.bg.m_y)
            if self.player_state != PlayerState.SLIDING and self.player_state != PlayerState.ATTACK1:
                self.player_state = PlayerState.STAND
        else:
            self.vy += self.gravity
        

        if self.canMove:
            # ジャンプ
            if pyxel.btnp(pyxel.KEY_SPACE, 1, 1) or pyxel.btnp(pyxel.GAMEPAD_1_B, 1, 1):
                if self.player_state == PlayerState.STAND:
                    if self.stamina >= 10:
                        self.vy = -2
                        self.jumpCount = self.count
                        self.player_state = PlayerState.JUMP
                        self.stamina -= 4
                    else:
                        self.hasStamina = False
                if self.player_state == PlayerState.JUMP:
                    if self.jumpCount+20 > self.count:
                        self.vy = -2
            if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.GAMEPAD_1_B):
                self.jumpCount-=20

            #　下
            if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
                if self.player_state == PlayerState.STAND:
                    self.player_state = PlayerState.SQUAT
                    self.p_speed = 0
            # コントロールキー
            if pyxel.btn(pyxel.KEY_CONTROL) or pyxel.btn(pyxel.GAMEPAD_1_LEFT_SHOULDER):
                if abs(self.p_speed) >= 1.5 and self.player_state == PlayerState.STAND:
                    if self.stamina >= 15:
                        self.stamina -= 15
                        self.player_state = PlayerState.SLIDING
                    else:
                        self.hasStamina = False

            # 左右
            if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD_1_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
                if self.player_state == PlayerState.STAND:
                    self.player_state = PlayerState.WALK
                if self.player_state == PlayerState.JUMP or self.player_state == PlayerState.FALL:
                    self.p_speed -= 0.08*self.p_direction
            if self.player_state != PlayerState.SLIDING \
                and self.player_state != PlayerState.ATTACK1 \
                    and self.player_state != PlayerState.JUMPATTACK:
                if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
                    self.p_direction = 1
                if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
                    self.p_direction = -1
            if self.player_state == PlayerState.WALK:
                self.p_speed -= 0.2*self.p_direction
                if pyxel.btn(pyxel.KEY_SHIFT) or pyxel.btn(pyxel.GAMEPAD_1_A):
                    self.stamina -= 0.12
                    if self.stamina > 5:
                        self.p_maxSpeed = 2
                    else:
                        self.hasStamina = False
                        self.p_maxSpeed = 0.8
                else:
                    self.p_maxSpeed = 1

            # 左クリック
            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                if self.player_state == PlayerState.STAND or self.player_state == PlayerState.WALK:
                    if self.stamina >= 10:
                        self.stamina -= 6
                        self.player_state = PlayerState.ATTACK1
                        self.attack1Count = 0
                        attack(self,self.p_direction * 9 + 109,100,14,24,20,self.atk)
                        pyxel.play(0,9)
                    else:
                        self.hasStamina = False
                elif self.player_state == PlayerState.JUMP or self.player_state == PlayerState.FALL:
                    if self.stamina >= 10:
                        self.stamina -= 6
                        if self.jumpattackCount == -1:
                            self.player_state = PlayerState.JUMPATTACK
                            self.jumpattackCount = 0
                    else:
                        self.hasStamina = False

        # アニメーション
        if self.player_state == PlayerState.WALK:
            if abs(self.p_speed) >= 2:
                if self.count % 4 == 0:
                    self.p_img += 1
            else:
                if self.count % 5 == 0:
                    self.p_img += 1
            if self.p_img == 9:
                self.p_img = 0

        if self.player_state == PlayerState.STAND:
            if self.p_img2 == 3:
                self.inversion = -1
            elif self.p_img2 == 0:
                self.inversion = 1
            if self.count % 8 == 0:
                    self.p_img2 += 1 * self.inversion

        if self.player_state == PlayerState.SLIDING:
            self.p_speed = -3*self.p_direction
            if self.count%4 == 3:
                self.slidingCount += 1
            if self.slidingCount >= 8:
                self.slidingCount = 0
                self.player_state = PlayerState.STAND

        if self.player_state == PlayerState.ATTACK1:
            if self.attack1Count < 30:
                if self.attack1Count < 10:
                    self.p_speed = 2*-self.p_direction
                else:
                    self.p_speed = 0
                self.attack1Count +=1
            else:
                self.player_state = PlayerState.STAND
                self.attack1Count = 0
                
        if self.jumpattackCount >= 0:
            self.jumpattackCount +=1
            if self.jumpattackCount == 6:
                attack(self,self.p_direction * 19 + 107,98,14,28,10,self.atk)
                pyxel.play(0,9)
            elif self.jumpattackCount == 25:
                self.player_state = PlayerState.FALL
            elif self.jumpattackCount > 50:
                self.jumpattackCount =-1
            

        # 画像の左右のずれ修正
        if self.p_direction == 1:
            self.p_imgPosition = 0
            self.p_detectionPosition = 14
        else:
            self.p_imgPosition = 10
            self.p_detectionPosition = 15

        # 落下したとき
        if self.bg.m_y < -16:
            self.alive = False

        # HPの処理
        if self.hp <= 5:
            self.hpColor = 9
            if self.hp <=0 :
                self.alive = False
        else:
            self.hpColor = 11

    
    def draw(self):
        if self.invincibleTime > 0 or self.player_state == PlayerState.SLIDING:
            if self.count%2 < 1:
                self.draw_player()
        else:
            self.draw_player()
        pyxel.text(3,5,"HP",15)
        for i in range(30):
            pyxel.rect(2*i+12,5,1,5,2)
        for i in range(self.hp):
            pyxel.rect(2*i+12,5,1,5,self.hpColor)
        for i in range(59):
            pyxel.rect(i+12,11,1,2,2)
        if not self.hasStamina:
            for i in range(59):
                pyxel.rect(i+12,11,1,2,9)
        for i in range(int(self.stamina)):
            pyxel.rect(i+12,11,1,2,10)


    def draw_player(self):
        if self.player_state == PlayerState.WALK:
            pyxel.blt(self.p_x+self.p_imgPosition, self.p_y,1, self.p_walkImg[self.p_img][0], self.p_walkImg[self.p_img][1], self.p_direction * 24,24,4)
        if self.player_state == PlayerState.STAND:
            pyxel.blt(self.p_x+self.p_imgPosition, self.p_y,1, self.p_standImg[self.p_img2][0], self.p_standImg[self.p_img2][1], self.p_direction * 24,24,4)
        if self.player_state == PlayerState.JUMP:
            if abs(self.p_speed) >= 1.5:
                pyxel.blt(self.p_x+self.p_imgPosition, self.p_y,1, 24,168, self.p_direction * 24,24,4)
            else:
                pyxel.blt(self.p_x+self.p_imgPosition, self.p_y,1, 24,120, self.p_direction * 24,24,4)
        if self.player_state == PlayerState.FALL:
            if abs(self.p_speed) >= 1:
                if self.vy > 1.5:
                    pyxel.blt(self.p_x+self.p_imgPosition, self.p_y,1, 24, 192, self.p_direction * 24,24,4)
                else:
                    pyxel.blt(self.p_x+self.p_imgPosition, self.p_y,1, 24, 216, self.p_direction * 24,24,4)
            else:
                pyxel.blt(self.p_x+self.p_imgPosition, self.p_y,1, 24, 144, self.p_direction * 24,24,4)
        if self.player_state == PlayerState.SQUAT:
            pyxel.blt(self.p_x+self.p_imgPosition+(self.p_direction*2), self.p_y,1, 24, 96, self.p_direction * 24,24,4)

        if self.player_state == PlayerState.SLIDING:
            if self.slidingCount < 2:
                pyxel.blt(self.p_x+self.p_imgPosition+(self.p_direction*2), self.p_y,1, 48, 0, self.p_direction * 24,24,4)
            elif self.slidingCount%2 == 0:
                pyxel.blt(self.p_x+self.p_imgPosition+(self.p_direction*2), self.p_y+8,1, 48, 24, self.p_direction * 32,16,4)
            else:
                pyxel.blt(self.p_x+self.p_imgPosition+(self.p_direction*2), self.p_y+8,1, 48, 40, self.p_direction * 32,16,4)
        if self.player_state == PlayerState.ATTACK1:
            if self.attack1Count//2 < 4:
                pyxel.blt(self.p_x,self.p_y,1, 48, self.p_attack1Img[self.attack1Count//2][0],self.p_direction * self.p_attack1Img[self.attack1Count//2][1],24,4)
            else:
                pyxel.blt(self.p_x,self.p_y+8,1, 48, 152,self.p_direction * 32,16,4)
        if self.player_state == PlayerState.JUMPATTACK:
            if self.jumpattackCount//4 < 3:
                if self.p_direction == 1:
                    pyxel.blt(self.p_x + self.p_jumpattackImg[self.jumpattackCount//4][3],self.p_y+ self.p_jumpattackImg[self.jumpattackCount//4][4],1, 48, self.p_jumpattackImg[self.jumpattackCount//4][0],self.p_direction * self.p_jumpattackImg[self.jumpattackCount//4][1],self.p_jumpattackImg[self.jumpattackCount//4][2],4)
                else:
                    pyxel.blt(self.p_x + self.p_jumpattackImg[self.jumpattackCount//4][3] + self.p_jumpattackImg[self.jumpattackCount//4][5],self.p_y+ self.p_jumpattackImg[self.jumpattackCount//4][4],1, 48, self.p_jumpattackImg[self.jumpattackCount//4][0],self.p_direction * self.p_jumpattackImg[self.jumpattackCount//4][1],self.p_jumpattackImg[self.jumpattackCount//4][2],4)
            else:
                if self.p_direction == 1:
                    pyxel.blt(self.p_x+4,self.p_y+8,1, 48, 224,self.p_direction * 24,24,4)
                else:
                    pyxel.blt(self.p_x+6,self.p_y+8,1, 48, 224,self.p_direction * 24,24,4)

    def invincibleTime_set(self,time):
        self.invincibleTime = time
    


class attack:
    def __init__(self,p,x,y,w,h,lifspan,atk):
        self.p = p
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.lifespan = lifspan
        self.atk = atk
        self.alive = True
        attack_list.append(self)

    def update(self):
        self.lifespan -= 1
        if self.lifespan < 0:
            self.alive = False

    def draw(self):
        pass
