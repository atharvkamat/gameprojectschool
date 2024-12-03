import pygame
import math
from random import randint
colour_list = []
pygame.init()

x,y = 20,20

#display
screenWidth = 800
screenHeight = 800
win = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("prototype")

#player
playerWidth = 40
playerHeight = 40
vel = pygame.math.Vector2(x,y)
playerVect = pygame.math.Vector2(screenWidth//2,screenHeight//2)
playerDirection = pygame.math.Vector2(0,1)
radius = 40
#colors
red = (255,0,0)
white = (255,255,255)

#clock
clock = pygame.time.Clock()
fps = 60

#angleCalcforGun
angle = 0
angleSpeed = 0.085

#gun
gunLength = 20
gunWidth = 20

#bullet
bulletsaa = []
bulletSpeed = 10
shootCooldown = 0

#hero
class hero(pygame.sprite.Sprite):
    def __init__(self, col, x, y):
        pygame.sprite.Sprite.__init__(self)
        rectcentre = pygame.Vector2((x,y))
        self.image = pygame.Surface((50,50))
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.time = 4000

    def update(self,enemypos):
        pos = pygame.Vector2(self.rect.center)
        B = enemypos- pos
        if B.x ==0 and B.y == 0:
            pass
        else:
            angle = math.atan2(B.y,B.x)
            v = 2
            self.rect.move_ip(v*math.cos(angle),v*math.sin(angle))
#bullet
class projectile(pygame.sprite.Sprite):
    def __init__(self,col,x,y,angle):
        pygame.sprite.Sprite.__init__(self)
        rectcentre = pygame.Vector2((x,y))
        self.image = pygame.Surface((20,20))
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.center = pygame.Vector2(x, y)
        self.angle = angle
        self.time = 2000
    def update(self,sc,sh):
        v = 20
        self.rect.move_ip(v*math.cos(self.angle),v*math.sin(self.angle))
        if self.rect.center[0]<0 or self.rect.center[0]>sc:
            self.kill()
        if self.rect.center[1]<0 or self.rect.center[1]>sh:
            self.kill()




enemy_slain = 0
#them squares:
squares = pygame.sprite.Group()
square = hero((255,255,255),0,0)
squares.add(square)

#them bullets:
bullets = pygame.sprite.Group()

#method to get parent center
def getParentCentre(playerVect,playerWidth,playerHeight):
    return (playerVect[0]+12, playerVect[1]+15)
#to get gun center
def getGunCenter(gunVect,gunWidth,gunLength):
    return(gunVect[0],gunVect[1])

        
run = True
while run:
    clock.tick(fps)
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    win.fill((0,0,0))
    #input
    #movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        playerVect.x -= vel.x
    if keys[pygame.K_a] and keys[pygame.K_s]:
        playerVect.normalize()
    if keys[pygame.K_d] and keys[pygame.K_s]:
        playerVect.normalize()
    if keys[pygame.K_a] and keys[pygame.K_w]:
        playerVect.normalize()
    if keys[pygame.K_d] and keys[pygame.K_w]:
        playerVect.normalize()
    if keys[pygame.K_d]:
        playerVect.x += vel.x
    if keys[pygame.K_w]:
        playerVect.y -= vel.y
    if keys[pygame.K_s]:
        playerVect.y += vel.y
     

    #border control
    if playerVect.x <= 0:
        playerVect.x = 960
    elif playerVect.x >= 960:
        playerVect.x = 0
    
    if playerVect.y <= 0:
        playerVect.y = 760
    elif playerVect.y >= 760:
        playerVect.y = 0

    
    
    #acquiring center of player
    center = getParentCentre(playerVect,playerWidth,playerHeight)

    #gun position
    gunX = center[0] + math.cos(angle) * radius + playerDirection.x
    gunY = center[1] + math.sin(angle) * radius + playerDirection.y

    gunVect = pygame.math.Vector2(int(gunX),int(gunY))

    #mouse,gun correction:
    mouseAngle= math.atan2(mouse_pos.y,mouse_pos.x)
    gunAngle = math.atan2(gunVect.y,gunVect.x)
    mouse_gun_rel_vector = mouse_pos-gunVect
    mouse_gun_rel_angle = math.atan2(mouse_gun_rel_vector.y,mouse_gun_rel_vector.x)
    gunX = center[0]+ (math.cos(mouse_gun_rel_angle)*radius)
    gunY = center[1]+(math.sin(mouse_gun_rel_angle)*radius)
    gunVect = pygame.math.Vector2(int(gunX),int(gunY))
    #input for gun movement
    if keys[pygame.K_l]:
        angle += angleSpeed
    if keys[pygame.K_j]:
        angle -= angleSpeed
    

    #calc of angle to get direction that the gun is facing 
    newAngle = mouse_gun_rel_angle

    
    dx = math.cos(newAngle) #trigonometry shi
    dy = math.sin(newAngle)
    bulletDir = newAngle #normalises the vector 

    #input for shooting gun
    
    
    if pygame.mouse.get_pressed()[0]== True and shootCooldown <= 0:
        gunCenter = gunVect# to get gun center
        bullet = projectile((255,255,255),gunCenter.x,gunCenter.y,newAngle)
        bullets.add(bullet)
        print("fired",newAngle) 
        shootCooldown = 15
    shootCooldown -= 1
     
    #drawing the objects
    player = pygame.draw.rect(win,red,(playerVect.x,playerVect.y,playerWidth,playerHeight))
    gun = pygame.draw.circle(win,white,(int(gunX),int(gunY)),10,10)
    squares.draw(win)
    squares.update(center)
    bullets.draw(win)
    bullets.update(screenWidth,screenHeight)
    no_of_squares = len(squares.sprites())
    if no_of_squares<4:
        h = 4-no_of_squares
        for i in range(h):
            for k in range(3):
                h = randint(1,255)
                colour_list.append(h)
            x = randint(1,screenWidth)
            y = randint(1,screenHeight)
            square = hero(tuple(colour_list),x,y)
            squares.add(square)
            colour_list = []
    #colisiion:
    coli = pygame.sprite.groupcollide(bullets, squares,True, True)#number of enemy slain not counting properly idk why
    if coli == True:
        enemy_slain += 1
    pygame.display.update()
pygame.quit()



