import pygame
import random
from time import sleep  

pygame.init()
pygame.mixer.init()

# Load music track
pygame.mixer.music.load("Music1.mp3")

# Display the screen
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Aloha Pig!")
font = pygame.font.Font(None, 40)
font2 = pygame.font.Font(None, 20)
number = 0
list = []
# List from 0 to 250
for x in range(1, 250):
    number += 1
    list.append(number)
# Gameover function
def Gameover(screen, font2, font):
    # Run this throughout the entire code page
    global run
    # Not moving
    moving = 0
    # Gameover text
    gameover = font.render('GAMEOVER', True, (30,153,0))
    # Stop music when game ends
    pygame.mixer.music.stop()
    # Show gameover text
    screen.blit(gameover, [73, 130, 50, 30])
    
# Pig / Player class
class Pig:
    def __init__(self, x, y, vel):
        # Prepare all Pig / Player variables
        self.x = x
        self.y = y
        self.vel = vel
    def show(self, screen):
        # Load pig image
        pig_image = pygame.image.load('PIG.png')
        screen.blit(pig_image, (self.x, self.y))
    def move(self, screen):
        keys = pygame.key.get_pressed()
        # Up key arrow pressed go up
        if keys[pygame.K_UP] and self.y > -3:
            self.y -= self.vel
        # Down key arrow pressed go down
        if keys[pygame.K_DOWN] and self.y < 278:
            self.y += self.vel
        # Right key arrow pressed go right
        if keys[pygame.K_RIGHT] and self.x < 278:
            self.x += self.vel
        # Left key arrow pressed go left
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel
            
# Pineapple class
class Pineapple:
    def __init__(self, x, y):
        # Prepare all pineapple variables
        self.x = x
        self.y = y
    def show(self, screen):
        # Load Pineapple image
        pine_image = pygame.image.load('pineapple.png')
        screen.blit(pine_image, (self.x, self.y))
    def change(self):
        global score
        # Touching pig then appear in random spot
        if self.y > pig.y - 20 and self.y < pig.y + 20 and self.x < pig.x + 10 and self.x > pig.x - 10:           
            self.x = random.choice(list)
            self.y = random.choice(list)
            # Change score by 1
            score += 1
# Fire class
class Fire:
    def __init__(self, x , y):
        # Prepare all fire variables
        self.x = x
        self.y = y
    def show(self, screen):
        # Load fire image
        fire_image = pygame.image.load('fire.png')
        screen.blit(fire_image, (self.x, self.y))
# Fireball class
class fireball:
    def __init__(self, x , y, velx, vely):
        # Prepare all fireball variables
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
    def show(self, screen):
        # Load fireball image
        fireball_image = pygame.image.load('fireball.png')
        screen.blit(fireball_image, (self.x, self.y))
            
    def move(self, screen):
        # Fireball bounces around the screen
        if self.y < 0:
            self.vely = -self.vely
        if self. y > 267:
            self.vely = -self.vely
        if self.x < 0:
            self.velx = -self.velx
        if self.x > 267:
            self.velx = -self.velx

        self.x += self.velx
        self.y += self.vely
# Background class            
class Background:
    def __init__(self, x, y):
        # Prepare all background variables
        self.x = x
        self.y = y
    def show(self, screen):
        # Load background image
        bg = pygame.image.load('grass.png')
        screen.blit(bg, (self.x, self.y))
# Score function
def show_score(screen, score, font):
    scoretext = font.render('Score: ' + str(score),True, (30,155,0))
    screen.blit(scoretext, [97, 0, 50, 30])
# Create lists called fires and feus
fires = []
feus = []
# Creating each object    
pig = Pig(270, 270, 2)
pine = Pineapple(120, 145)
bg = Background(0, 0)
# Add different fires - when the score reaches fire limit
fires.append(Fire(60, 199))
fires.append(Fire(237, 90))
fires.append(Fire(35, 59))
feus.append(fireball(123, 123, 1, 2))

# Run the game
run = True
# Start score variable when starting the game run
score = 1
# Possible to move
moving = 1

# Start saved music track
pygame.mixer.music.play(-1)

while run:
    if moving == 1:
        # Move pig
        pig.move(screen)

    for feu in feus:
        if moving == 1:
            # Move fireballs
            feu.move(screen)
    # X Button pressed? End game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # Score is a multiple of 14? Add new fireball
    if score % 14 == 0 and pine.y > pig.y - 20 and pine.y < pig.y + 20 and pine.x < pig.x + 10 and pine.x > pig.x - 10:
        feus.append(fireball(0, 0, 1, 2))
    # Score is a multiple of 10? All fireballs get faster
    if score % 10 == 0 and pine.y > pig.y - 20 and pine.y < pig.y + 20 and pine.x < pig.x + 10 and pine.x > pig.x - 10:
        for feu in feus:
            feu.velx += 0.4
    # if pineapple appears touching the fire? Pineapple changes it's place
    for fire in fires:
        if pine.y > fire.y - 20 and pine.y < fire.y + 20 and pine.x < fire.x + 10 and pine.x > fire.x - 10:
                pine.x = random.choice(list)
                pine.y = random.choice(list)
                
    pine.change()

    # Show background
    bg.show(screen)

    # Show Score
    show_score(screen, score, font)
    
    # Show pig
    pig.show(screen)
    # Show Pineapple
    pine.show(screen)

    for feu in feus:
        # Show fireballs
        feu.show(screen)
        # If fireball touching pig then Gameover
        if feu.y > pig.y - 10 and feu.y < pig.y + 10 and feu.x < pig.x + 20 and feu.x > pig.x - 20:
            y = -300
            Gameover(screen, font2, font)
            moving = 0
            
    # Show Fires    
    for fire in fires:
        fire.show(screen)
        # If Fire touching pig then Gameover
        if fire.y > pig.y - 10 and fire.y < pig.y + 10 and fire.x < pig.x + 20 and fire.x > pig.x - 20:
            y = -300
            Gameover(screen, font2, font)
            pygame.mixer.music.stop()
            moving = 0

    # update all displays for moving effect`
    pygame.display.update()
# Quit pygame
pygame.mixer.stop()
pygame.quit()
