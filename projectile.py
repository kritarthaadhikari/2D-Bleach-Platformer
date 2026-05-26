import pygame
import setup as st
import player as pl

projectiles = []

class Projectile(pygame.Rect):
    def __init__(self,x,y,width,height,facing):
        super().__init__(x,y,width,height)
        self.vel= 15
        self.count=0
        self.getsugatenshou=False
        self.direction= facing
        self.hitEnemies= [] #stores hollows that have been hit and prevents repeated hits
        self.shot={
            "bankai":{
                "shotRight": st.getsugatenshoProjectileRight,
                "shotLeft": st.getsugatenshoProjectileLeft
            },
            "shikai":{
                "shotRight": st.slashright,
                "shotLeft": st.slashLeft
            }
        }
    
    def draw(self,win, scroll=0,player=None):
        framesPerImg=3
        sprite=None
        if self.getsugatenshou :
            limit= 3*len(self.shot[player.mode]["shotRight"])
            if self.direction==1:
                sprite= self.shot[player.mode]["shotRight"][self.count//framesPerImg]
            else:
                sprite= self.shot[player.mode]["shotLeft"][self.count//framesPerImg]
            if self.count+1>=limit:
                self.count=0
                self.getsugatenshou=False
                self.kill()
            self.count+=1 
        win.blit(sprite, (self.x - scroll,self.y))
        #pygame.draw.rect(win, (255,0,0),self,2) for hitbox

    def move(self,player):
        if player.mode=="bankai":
            self.x+= self.direction*self.vel*2
        else:
            self.x+= self.direction*self.vel
        # Note: We pass win from the main loop to this method later
    
    def kill(self):
        if self in projectiles[:]:
            projectiles.remove(self)
    
class Cero(Projectile):
    def __init__(self, x, y, width, height, facing):
        super().__init__(x, y, width, height, facing)
        self.vel=30
        self.cero=False
    
    def draw(self,win):
        framesPerImg=3
        sprite=None
        if self.cero:
            limit=len(st.ceroRight)*framesPerImg
            if self.direction==1:
                sprite=st.ceroRight[self.count//framesPerImg]
            else:
                sprite=st.ceroLeft[self.count//framesPerImg]
            if self.count+1>=limit:
                self.count=0
                self.cero=False
                self.kill()
            else:
                self.count+=1
        win.blit(sprite,(self.x,self.y))

    def move(self):
        self.x+=self.direction*self.vel

    def kill(self):
        super().kill()

    
