import pygame

# initialize pygame, required at the begining of every pygame program
pygame.init()

# window dimension
win_width = 500
win_height = 480

# window I will draw on
win = pygame.display.set_mode((win_width, win_height))

# load images
walkRight = [pygame.image.load('pics/R1.png'), pygame.image.load('pics/R2.png'), pygame.image.load('pics/R3.png'), pygame.image.load('pics/R4.png'), pygame.image.load('pics/R5.png'), pygame.image.load('pics/R6.png'), pygame.image.load('pics/R7.png'), pygame.image.load('pics/R8.png'), pygame.image.load('pics/R9.png')]
walkLeft = [pygame.image.load('pics/L1.png'), pygame.image.load('pics/L2.png'), pygame.image.load('pics/L3.png'), pygame.image.load('pics/L4.png'), pygame.image.load('pics/L5.png'), pygame.image.load('pics/L6.png'), pygame.image.load('pics/L7.png'), pygame.image.load('pics/L8.png'), pygame.image.load('pics/L9.png')]
bg = pygame.image.load('pics/bg.jpg')
char = pygame.image.load('pics/standing.png')

# window caption
pygame.display.set_caption("Tutorial")

# game clock (FPS)
clock = pygame.time.Clock()

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 7
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
    
    def draw(self, win):
        # drawing character
        if not(self.standing):
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x,self.y))
                self.walkCount += 1

            elif player.right:
                win.blit(walkRight[self.walkCount // 3], (self.x,self.y))
                self.walkCount += 1
        
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
    
    def hit(self):
        print("Hit")


class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing  # facing variable is either 1 or -1 so this will determine weather the bullet is moving left or right

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius) # for the circle to not be filled in add another argument that is (1)


class Enemy(object):
    walkRight = [pygame.image.load('pics/R1E.png'), pygame.image.load('pics/R2E.png'), pygame.image.load('pics/R3E.png'), pygame.image.load('pics/R4E.png'), pygame.image.load('pics/R5E.png'), pygame.image.load('pics/R6E.png'), pygame.image.load('pics/R7E.png'), pygame.image.load('pics/R8E.png'), pygame.image.load('pics/R9E.png'), pygame.image.load('pics/R10E.png'), pygame.image.load('pics/R11E.png')]
    walkLeft = [pygame.image.load('pics/L1E.png'), pygame.image.load('pics/L2E.png'), pygame.image.load('pics/L3E.png'), pygame.image.load('pics/L4E.png'), pygame.image.load('pics/L5E.png'), pygame.image.load('pics/L6E.png'), pygame.image.load('pics/L7E.png'), pygame.image.load('pics/L8E.png'), pygame.image.load('pics/L9E.png'), pygame.image.load('pics/L10E.png'), pygame.image.load('pics/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)


    def draw(self, win):
        self.move()

        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        print("Hit")


def redrawGameWin():
    # makes drawing of character draw over the previous stuff on the board
    win.blit(bg, (0, 0)) # background image
    player.draw(win)
    goblin.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()

# main game loop
player = Player(300, 410, 64, 64)
goblin = Enemy(100, 415, 64, 64, 450)

shootLoop = 0
bullets = []
score = 0
font = pygame.font.SysFont('Poppins')

run = True
while run:
    clock.tick(27) # amount of FPS

    if shootLoop > 0:
        shootLoop += 1
    
    if shootLoop > 3:
        shootLoop = 0

    # checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # check for player collision with goblin
    if player.hitbox[1] + player.hitbox[3] > goblin.hitbox[1] and player.hitbox[3] - player.hitbox[1] < goblin.hitbox[3]:
        if player.hitbox[0] + player.hitbox[2] > goblin.hitbox[0] and player.hitbox[0] - player.hitbox[2] < goblin.hitbox[0] + goblin.hitbox[2]:
            player.hit()

    # check for bullet collision with goblin
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius >  goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                bullets.pop(bullets.index(bullet))
                score += 1
                print(score)

        if bullet.x < win_width and bullet.x > 0:
            bullet.x += bullet.vel
        
        else:
            bullets.pop(bullets.index(bullet))
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LSHIFT] and shootLoop == 0:
        if player.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(Projectile(round(player.x + player.width // 2), round(player.y + player.height // 2), 6, (0, 0, 0), facing))

        shootLoop = 1

    if keys[pygame.K_a] and player.x > 0:
        player.x -= player.vel
        player.left = True
        player.right = False
        player.standing = False

    elif keys[pygame.K_d] and player.x < win_width - player.width - player.vel:
        player.x += player.vel
        player.right = True
        player.left = False
        player.standing = False

    else:
        player.standing = True
        player.walkCount = 0

    # jumping
    if not (player.isJump):
        if keys[pygame.K_SPACE]:
            player.isJump = True
            player.walkCount = 0
    
    else:
        if player.jumpCount >= -7:
            neg = 1

            if player.jumpCount < 0:
                neg = -1   

            player.y -= (player.jumpCount ** 2) * 0.5 * neg
            player.jumpCount -= 1
        
        else:
            player.isJump = False
            player.jumpCount = 7
    
    redrawGameWin()

pygame.quit()