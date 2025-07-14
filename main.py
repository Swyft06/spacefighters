import pygame
import random 
pygame.font.init()


WIDTH = 800
HEIGHT = 700

WIN = pygame.display.set_mode([WIDTH,HEIGHT])

BORDER = pygame.Rect(WIDTH // 2-5,0,10,HEIGHT)

HEALTH_FONT = pygame.font.SysFont("Times New Roman",40)
WINNER_FONT = pygame.font.SysFont("Times New Roman",100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5

WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)

BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT +  2

blueship = pygame.image.load('blueship.png')
redship = pygame.image.load('redship.png')
background = pygame.image.load('space.jpg')
bg = pygame.transform.scale(background,(WIDTH,HEIGHT))
WIN.blit(bg(0,0))

blueship = pygame.transform.scale(blueship(50,50))
redship = pygame.transform.scale(redship(50,50))


class PowerUps(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('powerup1.png','powerup2.png')
        self.image = pygame.transform.scale(self.image(30,30))
        self.rect = self.image.get_rect()

powerups_list = pygame.sprite.Group()

images = ["powerup1.png","powerup2.png"]

for i in range(10):
    powerup = random.choice(images) 
    powerup.rect.x = random.randrange(WIDTH)
    powerup.rect.y = random.randrange(HEIGHT)

def draw_window(blue_bullets,red_bullets,blue_health,red_health):
    pygame.draw.rect(WIN,BORDER)
    blue_health_text = HEALTH_FONT.render("Health: " + str(blue_health),1, WHITE)
    WIN.blit(blue_health_text,(10,10))
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health),1,WHITE)
    WIN.blit(red_health_text,(600,10))

    for bullet in blue_bullets:
        pygame.draw.rect(WIN,BLUE,bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    pygame.display.update()

def handle_bullets(blue_bullets,red_bullets,blue,red):
    for bullet in blue_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def blue_handle_movement(keys_pressed,blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0:
        blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x + VEL + blue.width < BORDER.x:
        blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y - VEL >0:
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT - 10:
        blue.y += VEL

def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL





