import setup as st
import pygame
import projectile as pj
class Aizen:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox= pygame.Rect(self.x+10, self.y-4, 74, 74)
        self.health=800
        self.vel=6
        self.walkCount=0
        self.facing=-1
        self.idleCount=0
        self.action="idle" #idle, sec_idle, walk, attack, hit, death
        self.attackCount=0
        self.hitCount=0

    def draw(self, win):
        self.hitbox= pygame.Rect(self.x+10, self.y-4, 74, 74)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
        framesPerImg=3
        if self.action=="idle":
            limit=len(st.AizenStanceRight)*framesPerImg
            if self.facing==-1:
                sprite=st.AizenStanceLeft[self.idleCount//framesPerImg] 
            else:
                sprite=st.AizenStanceRight[self.idleCount//framesPerImg]
            if self.idleCount+1>=limit: 
                self.idleCount=0
                self.action="sec_idle"
            else:
                self.idleCount+=1    
        elif self.action=="sec_idle":
            limit=len(st.AizenStanceMiddleLeft)*framesPerImg
            if self.facing==-1:
                sprite=st.AizenStanceMiddleLeft[self.idleCount//framesPerImg] 
            else:
                sprite=st.AizenStanceMiddleRight[self.idleCount//framesPerImg]
            if self.idleCount+1>=limit: 
                self.idleCount=0
                self.action="third_idle"
            else:
                self.idleCount+=1
        elif self.action=="third_idle": 
            limit=len(st.AizenStanceFinalLeft)*framesPerImg
            if self.facing==-1:
                sprite=st.AizenStanceFinalLeft[self.idleCount//framesPerImg] 
            else:
                sprite=st.AizenStanceFinalRight[self.idleCount//framesPerImg]
            if self.idleCount+1>=limit: 
                self.idleCount=0
                self.action="final_idle"
            else:
                self.idleCount+=1
        elif self.action=="cero":
            limit=len(st.AizenCeroRight)*framesPerImg
            if self.facing==1:
                sprite=st.AizenCeroRight[self.attackCount//framesPerImg]
            else:
                sprite=st.AizenCeroLeft[self.attackCount//framesPerImg]
            if self.attackCount+1>=limit:
                self.attackCount=0
                self.action="idle"
        elif self.action=="attack":
            limit=len(st.AizenattackRight)*framesPerImg
            if self.facing==1:
                sprite=st.AizenattackRight[self.attackCount//framesPerImg]
            else:
                sprite=st.AizenattackLeft[self.attackCount//framesPerImg]
            if self.attackCount+1>=limit:
                self.attackCount=0
                self.action="jump_attack"
            else:
                self.attackCount+=1
        elif self.action=="jump_attack":
            limit=len(st.AizenJumpAttackLeft)*framesPerImg
            if self.facing==1:
                sprite=st.AizenJumpAttackRight[self.attackCount//framesPerImg]
            else:
                sprite=st.AizenJumpAttackLeft[self.attackCount//framesPerImg]
            if self.attackCount+1>=limit:
                self.attackCount=0
                self.action="combo_attack"
        elif self.action=="combo_attack":
            limit=len(st.AizensecondAttackLeft)*framesPerImg
            if self.facing==1:
                sprite=st.AizensecondAttackRight[self.attackCount//framesPerImg]
            else:
                sprite=st.AizensecondAttackLeft[self.attackCount//framesPerImg]
            if self.attackCount+1>=limit:
                self.attackCount=0
                self.action="idle"
            else:
                self.attackCount+=1
        elif self.action=="teleport":
            limit=len(st.AizenTeleportLeft)*framesPerImg
            if self.facing==1:
                sprite=st.AizenTeleportRight[self.idleCount//framesPerImg]
            else:
                sprite=st.AizenTeleportLeft[self.idleCount//framesPerImg]
            if self.idleCount+1>=limit:
                self.idleCount=0
                self.action="idle"
            else:
                self.idleCount+=1
        elif self.action=="walk":
            limit=len(st.AizenRunRight)*framesPerImg
            if self.facing==1:
                sprite=st.AizenRunRight[self.walkCount//framesPerImg]
            else:
                sprite=st.AizenRunLeft[self.walkCount//framesPerImg]
            if self.walkCount+1>=limit:
                self.walkCount=0
            else:
                self.walkCount+=1
        elif self.action=="hit":
            limit=len(st.AizenHitLeft)*framesPerImg
            if self.facing==1:
                sprite=st.AizenHitRight[self.hitCount//framesPerImg]
            else:
                sprite=st.AizenHitLeft[self.hitCount//framesPerImg]
            if self.hitCount+1>=limit:
                self.hitCount=0
            else:
                self.hitCount+=1
        elif self.action=="dash":
            limit=len(st.AizenDashLeft)*framesPerImg
            if self.facing==1:
                sprite=st.AizenDashRight[self.idleCount//framesPerImg]
            else:
                sprite=st.AizenDashLeft[self.idleCount//framesPerImg]
            if self.idleCount+1>=limit:
                self.idleCount=0
            else:
                self.idleCount+=1
        else:
            limit=len(st.AizenFinalIdleRight)*framesPerImg
            if self.facing==-1:
                sprite=st.AizenFinalIdleLeft[self.idleCount//framesPerImg]
            else:
                sprite=st.AizenFinalIdleRight[self.idleCount//framesPerImg]
            if self.idleCount+1>=limit:
                self.idleCount=0
                self.action="final_idle"
        win.blit(sprite, (self.x, self.y))

    

        


