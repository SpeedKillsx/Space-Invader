import math
import pygame
import random
from pygame import mixer
from pygame.event import wait
#Initialize the game
pygame.init()
#Change the title of the screen
pygame.display.set_caption("Space Invader")
# Create the screen
screen = pygame.display.set_mode((800,600))
#Change the logo
icon = pygame.image.load('SpaceInvaders.png')
pygame.display.set_icon(icon)
#Add icon on the screen
playerImg = pygame.image.load('NaveSpaceInvaders.png')
# Position of the rocket in the screen
PlayerX = 340
PlayerY = 480
# Change the X position because the rocket will move horizontaly 
palyerX_change = 0
# The oppenent(enemy like alien's rocket)
# We use list to make a lot of enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6 # You can change it if you want but it will make the game slower because of icons 
# Print the enemies and make them walk on screen
for i in range(0,6):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,340))
    enemyY.append(random.randint(50,100))
    enemyX_change.append(5)
    enemyY_change.append(30)


# Rocket 
def Player(x, y):
    screen.blit(playerImg,(x,y))

# Enemy
def Enemy(x, y,i):
    screen.blit(enemyImg[i],(x,y))

# Background image
background = pygame.image.load("background.png")
# Position of laser
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"
# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10
# Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Laser
def Bullet(x, y):
    global bullet_state
    
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16,y + 20))
        
# Calculate the collision between the Laser and the Enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
   distance = math.sqrt((math.pow((enemyX - bulletX),2)) + (math.pow((enemyY - bulletY),2)))
   if distance < 25:
       return True
   return False
def Score(x, y):
    
    Myscore = font.render("Your score: " + str(score), True, (255, 255, 255))
    screen.blit(Myscore, (x, y))
# Pour arreter le jeu
def Perdu():
    laugh = mixer.Sound('laugh.wav') # Make an Horor sound when it's GAME OVER
    laugh.play()
    Message = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(Message, (400,400))
    
running = True
while running:
    # Color of the background
    screen.fill((0,0,0))
    # Add the background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check if a key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # if we want to go left we minus the X position
                palyerX_change = -5
            if event.key == pygame.K_RIGHT:
                # # if we want to go right we add the X position
                palyerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    laser_sound = mixer.Sound('laser.wav')
                    laser_sound.play()
                    bulletX = PlayerX
                    Bullet(bulletX, bulletY)


        
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or pygame.K_RIGHT :
                palyerX_change = 0
            
        
    # For not going out of screen (Rocket)
    
    if PlayerX <=0:
        PlayerX = 0
    if PlayerX>= 738:
        PlayerX = 738
    # For not going out of screen (Enemy)
    for i in range(num_enemies):
        # Here the player loose
        if enemyY[i] > 470:
            for j in range(num_enemies):
                enemyY[i] = 2000
            # Call the function Perdu
            Perdu()            
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >=738:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            # reinitialization
            bulletY = 480
            bullet_state = "ready"
            # Add one to score
            score +=1
            enemyX[i] = random.randint(0,700)
            enemyY[i] = random.randint(15,200)
        # Change the Enemy icon    
        if score > 10:
            enemyImg[i] = pygame.image.load('ufo.png')
        if score> 20:
            enemyImg[i] = pygame.image.load('alien.png')
        # Print the new enemy icon
        Enemy(enemyX[i], enemyY[i],i)
    # Replace the lazer in same position of the player
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    # if we pressed space we discrease the Y position of laser
    if bullet_state is "fire":
        Bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    PlayerX += palyerX_change
    Player(PlayerX, PlayerY)    
    # Print the score in the screen
    Score(10,10)
    pygame.display.update()
 