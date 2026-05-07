import pygame
import setup as st
import projectile as pr
class Player:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.feet_y = y  
        self.y_offset= 0
        self.vel = 5
        self.walkCount = 0 #movement
        self.stanceCount = 0 #stance init
        self.stanceFinal = 0 #stance continuation
        self.stancephase = 0 #T/F for stance
        self.jumpCount = 11 #jump parameter
        self.spjumpCount = 0 #jump 
        self.facing = 1 #direction
        self.dashTimer = 10 #dash duration
        self.hitbox = pygame.Rect(self.x+10, self.feet_y-4,50, 52 )
        self.getHitCount = 0 #getting hit
        self.stationaryPhase = False #getting hit continuation T/F
        self.stationaryPhaseCount = 0 #getting hit continuation
        self.downCount = 0 #knocked out 
        self.health = 120
        self.signatureCount = 0
        self.staminaGauge = 100
        self.ultimateGauge = 160
        self.comboIndex=0 #for combo attacks
        self.comboTimer=5 #Time allowed for followup attack
        self.comboQueued= False
        self.mode= "shikai" #shikai or bankai mode
        self.action="idle" #current action state
        self.incrementalFactor= 1 #bankai impact increase factor
        self.animations= {
            "shikai":{
                "walkRight": st.walkRight,
                "walkLeft": st.walkLeft,
                "stanceRight": st.stanceRight,
                "stanceLeft": st.stanceLeft,
                "stanceFinalRight": st.stanceFinalRight,
                "stanceFinalLeft": st.stanceFinalLeft,
                "jumpRight": st.jumpRight,
                "jumpLeft": st.jumpLeft,
                "dashRight": st.dashRight,
                "dashLeft": st.dashLeft,
                "attackRight": st.attackRight,
                "attackLeft": st.attackLeft,
                "IdleHitRight": st.IdleHitRight,
                "IdleHitLeft": st.IdleHitLeft,
                "HitRight": st.HitRight,
                "HitLeft": st.HitLeft,
                "standUpRight": st.standUpRight,
                "standUpLeft": st.standUpLeft,
                "getsugatenshoRight": st.getsugatenshoRight,
                "getsugatenshoLeft": st.getsugatenshoLeft,
                "attackFollowUpRight": st.attackFollowUpRight,
                "attackFollowUpLeft": st.attackFollowUpLeft,
                "transformRight": st.shikaiTransformRight,
                "transformLeft": st.shikaiTransformLeft
            },
            "bankai":{
                "walkRight": st.bankaiWalkRight,
                "walkLeft": st.bankaiWalkLeft,
                "stanceRight": st.bankaiStanceRight,
                "stanceLeft": st.bankaiStanceLeft,
                "stanceFinalRight": st.bankaiStanceRight,
                "stanceFinalLeft": st.bankaiStanceLeft,
                "jumpRight": st.bankaiJumpRight,
                "jumpLeft": st.bankaiJumpLeft,
                "dashRight": st.bankaiDashRight,
                "dashLeft": st.bankaiDashLeft,
                "HitRight": st.bankaiHitRight,
                "HitLeft": st.bankaiHitLeft,
                "attackRight": st.bankaiAttackRight,
                "attackLeft": st.bankaiAttackLeft,
                "IdleHitRight": st.bankaiIdleHitRight,
                "IdleHitLeft": st.bankaiIdleHitLeft,
                "standUpRight": st.bankaistandUpRight,
                "standUpLeft": st.bankaistandUpLeft,
                "getsugatenshoRight": st.bankaiGetsugatenshoRight,
                "getsugatenshoLeft": st.bankaiGetsugatenshoLeft,
                "attackFollowUpRight": st.bankaiFollowUpRight,
                "attackFollowUpLeft": st.bankaiFollowUpLeft,
                "transformRight": st.bankaiTransformRight,
                "transformLeft": st.bankaiTransformLeft 
            }
        }
        self.bankai=False
        self.bankaiCount=0
        self.attackCount = 0 #attack
        self.dashCount = 0 #dash
        self.right = False
        self.left = False
        self.hollowattack=[]
        self.damage=200

    def activateBankai(self):
        self.mode= "bankai"
        self.vel=6
        self.damage=500
        self.stanceCount=0
        self.stanceFinal=0
        self.incrementalFactor=2
        self.dashCount=0
        self.attackCount=0
        self.signatureCount=0
        self.jumpCount=11
        self.spjumpCount=0
        self.bankai=True
        self.ultimateGauge=0
        self.staminaGauge/=2
        st.bankaiSound.play(0)
        self.draw(st.win)
        
    def draw(self, win, scroll=0):
        framesPerImg = 3
        limit=0
        sprite = st.jumpLeft[0]
        if self.bankai:
            limit=len(self.animations[self.mode]["transformRight"])*4
            if self.facing==1:
                sprite= self.animations[self.mode]["transformRight"][self.bankaiCount//4]
            else:
                sprite= self.animations[self.mode]["transformLeft"][self.bankaiCount//4]
            if self.mode=="bankai":
                if 16<=self.bankaiCount<=24:
                    st.win.blit(st.bankai, (self.x-self.facing*70 + scroll, self.feet_y- st.bankai.get_height()+50))
                if 24<=self.bankaiCount<=32:
                    st.win.blit(st.tl,(self.x-self.facing*(50 + scroll), self.feet_y- st.tl.get_height()+40))
                    st.win.blit(st.tr,(self.x+self.facing*(50 - scroll), self.feet_y-st.tr.get_height()+40))
                    # st.win.blit(st.br,(self.x+self.facing*70,self.feet_y+st.br.get_height()-60))
                    # st.win.blit(st.bl,(self.x-self.facing*70,self.feet_y+st.bl.get_height()-60))
                    # st.win.blit(st.br2, (self.x+self.facing*70,self.feet_y+st.br2.get_height()))
            
            if self.bankaiCount+1>= limit:
                self.bankaiCount=0
                self.bankai=False
            self.bankaiCount+=1
        if not self.bankai:
            if self.action=="idle" and self.action != "jump" and self.action not in ["attacking", "combo", "signature"]:
                self.stancephase=0
                if self.action=="dashing": #dashing animation
                    if self.facing==1:
                        limit= len(self.animations[self.mode]["dashRight"])*framesPerImg
                        sprite = self.animations[self.mode]["dashRight"][self.dashCount//framesPerImg]
                    else:
                        limit = len(self.animations[self.mode]["dashLeft"]) *framesPerImg
                        sprite = self.animations[self.mode]["dashLeft"][self.dashCount//framesPerImg]
                    self.dashCount += 1
                    if self.dashCount +1>= limit:
                        self.dashCount = 0
                    self.dashTimer-=1
                    if self.dashTimer<=0:
                        self.action="idle"
                        self.dashCount=0
                        self.dashTimer=10

                elif self.action != "knockeddown": #movement animation
                    if self.left:
                        limit = len(self.animations[self.mode]["walkLeft"]) * framesPerImg
                        sprite = self.animations[self.mode]["walkLeft"][self.walkCount // framesPerImg]
                    elif self.right:
                        limit = len(self.animations[self.mode]["walkRight"]) * framesPerImg
                        sprite = self.animations[self.mode]["walkRight"][self.walkCount // framesPerImg]
                    self.walkCount += 1
                    if self.walkCount +1 >= limit:
                        self.walkCount = 0
                else: #Standing back up animation
                    self.stationaryPhase= False
                    if self.facing==1:
                        limit= len(self.animations[self.mode]["standUpRight"])* framesPerImg
                        sprite= self.animations[self.mode]["standUpRight"][self.downCount// framesPerImg]
                    else:
                        limit= len(self.animations[self.mode]["standUpLeft"])* framesPerImg
                        sprite= self.animations[self.mode]["standUpLeft"][self.downCount// framesPerImg]
                    if self.downCount+1 >=limit:
                        self.downCount=0
                        self.down= False
                        if not self.gotHit:
                            self.stationaryPhase=False
                        
                    self.downCount+=1
            elif self.action=="jump": #jump animation
                if self.facing==1:
                    limit = len(self.animations[self.mode]["jumpRight"])* framesPerImg
                    sprite= self.animations[self.mode]["jumpRight"][self.spjumpCount//framesPerImg]
                else:
                    limit = len(self.animations[self.mode]["jumpLeft"])* framesPerImg
                    sprite= self.animations[self.mode]["jumpLeft"][self.spjumpCount//framesPerImg]
                if self.spjumpCount +1>= limit:
                    self.spjumpCount=0
                self.spjumpCount += 1
            elif self.stationaryPhase:  #continuously getting hit animation
                if self.facing==-1:
                    limit= len(self.animations[self.mode]["IdleHitLeft"])*framesPerImg
                    sprite= self.animations[self.mode]["IdleHitLeft"][self.stationaryPhaseCount// framesPerImg]
                else:
                    limit= len(self.animations[self.mode]["IdleHitRight"])*framesPerImg
                    sprite= self.animations[self.mode]["IdleHitRight"][self.stationaryPhaseCount// framesPerImg]
                if self.stationaryPhaseCount+1>= limit:
                    self.stationaryPhaseCount=0
                    self.down= True
                self.stationaryPhaseCount+=1
                
            elif self.gotHit: #falling and getting hit animation
                if self.facing==1:
                    limit= len(self.animations[self.mode]["HitRight"])*framesPerImg
                    sprite= self.animations[self.mode]["HitRight"][self.getHitCount//framesPerImg]
                else:
                    limit= len(self.animations[self.mode]["HitLeft"])*framesPerImg
                    sprite= self.animations[self.mode]["HitLeft"][self.getHitCount//framesPerImg]
                if self.getHitCount+1>=limit:
                    self.getHitCount=0
                    self.gotHit= False
                    self.stationaryPhase= True
                    self.down= True
                    self.stationaryPhaseCount=0
                self.getHitCount+=1
            elif self.action=="attacking" or self.action=="signature":
                if self.action=="signature": #getsugatensho launch animation
                    limit= len(self.animations[self.mode]["getsugatenshoRight"])*framesPerImg
                    if self.facing==1:
                        sprite= self.animations[self.mode]["getsugatenshoRight"][self.signatureCount// framesPerImg]
                    else:
                        sprite= self.animations[self.mode]["getsugatenshoLeft"][self.signatureCount// framesPerImg]
                    if 32>=self.signatureCount>=12:
                        st.win.blit(st.getsugatensho, (self.x-self.facing*(50 + scroll), self.feet_y- st.getsugatensho.get_height()+40))
                    self.signatureCount+=1
                    if self.signatureCount+1>=limit:
                        self.signatureCount=0
                        self.action="idle"

                else: #normal attack animation
                    self.x+= self.facing//2
                    limit= len(self.animations[self.mode]["attackRight"])*framesPerImg
                    if self.facing==1:
                        sprite= self.animations[self.mode]["attackRight"][self.attackCount// framesPerImg]
                    else:
                        sprite= self.animations[self.mode]["attackLeft"][self.attackCount// framesPerImg]
                    self.attackCount+=1

                    if self.attackCount+1 >= limit:
                        self.attackCount=0
                        self.action="idle"
                        if self.comboQueued:
                            self.comboQueued = False
                            self.action="combo"
                            self.attackCount = 0

            elif self.action=="combo":
                    self.x+= self.facing
                    self.y_offset-=1
                    limit= len(self.animations[self.mode]["attackFollowUpRight"])*framesPerImg
                    if self.facing==1:
                        sprite= self.animations[self.mode]["attackFollowUpRight"][self.attackCount//framesPerImg]
                    else:
                        sprite= self.animations[self.mode]["attackFollowUpLeft"][self.attackCount//framesPerImg]
                    self.attackCount+=1
                    if self.attackCount+1 >=limit:
                        self.attackCount=0
                        self.comboIndex=0   
                        self.comboTimer=5
                        self.y_offset=0
                        self.action="idle"
            
            else:
                if self.stancephase==0: #stance during no input
                    if self.facing==-1:
                        limit = len(self.animations[self.mode]["stanceLeft"]) * framesPerImg
                        sprite = self.animations[self.mode]["stanceLeft"][self.stanceCount // framesPerImg]
                    elif self.facing==1:
                        limit = len(self.animations[self.mode]["stanceRight"]) * framesPerImg
                        sprite = self.animations[self.mode]["stanceRight"][self.stanceCount // framesPerImg]
                    if self.stanceCount +1>= limit:
                        self.stanceCount=0
                        self.stancephase=1
                    self.stanceCount += 1
                else: #continued stance when idle
                    if self.facing==-1:
                        limit = len(self.animations[self.mode]["stanceFinalLeft"]) * framesPerImg
                        sprite = self.animations[self.mode]["stanceFinalLeft"][self.stanceFinal // framesPerImg]
                    else:
                        limit = len(self.animations[self.mode]["stanceFinalRight"]) * framesPerImg
                        sprite = self.animations[self.mode]["stanceFinalRight"][self.stanceFinal // framesPerImg]
                    self.stanceFinal+=1
                    if self.stanceFinal+1>= limit:
                        self.stanceFinal=0
                        self.stanceCount=0

        self.hitbox= pygame.Rect(self.x+10, self.feet_y-4,50, 52 )
        
        draw_x= self.x
        if not self.mode=="bankai" or  ((self.animations['bankai']['stanceRight'][0] and self.facing==1)and (self.action not in ["attacking", "combo"])
                                        or((self.mode=="bankai" and (self.action in ["attacking", "combo"]) and self.facing==-1))):
            if self.signature and self.facing==-1 or self.mode=="bankai":
                draw_x= self.x -sprite.get_width()+50
        
        sprite_height = sprite.get_height()
        draw_y = self.feet_y - sprite_height+self.y_offset+50
        win.blit(sprite, (draw_x - self.facing*scroll, draw_y))

    def hit(self):
        self.health-=1
        if not self.stationaryPhase:
            self.interrupt()
            self.gotHit=True
            self.stationaryPhase= False

    def interrupt(self):
        self.action="idle"
        self.attackCount = 0
        self.comboQueued=False
        self.comboTimer=5
        self.comboIndex=0
        self.y_offset = 0
        pr.projectiles.clear()   # only reset animation, not physics
        self.signature= False
        self.signatureCount=0