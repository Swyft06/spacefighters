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

SPACESHIP_WIDTH,SPACESHIP_HEIGHT = 55,40

blueship = pygame.image.load('blueship.png')
redship = pygame.image.load('redship.png')
background = pygame.image.load('space.jpg')
bg = pygame.transform.scale(background,(WIDTH,HEIGHT))
WIN.blit(bg,(0,0))

blueship = pygame.transform.scale(blueship,(50,50))
redship = pygame.transform.scale(redship,(50,50))



powerups_list = pygame.sprite.Group()

health_powerup = pygame.image.load('powerup1.png')
health_powerup = pygame.transform.scale(health_powerup, (30, 30))

damage_powerup = pygame.image.load('powerup2.png')
damage_powerup = pygame.transform.scale(damage_powerup, (30, 30))

health_rect = health_powerup.get_rect(topleft=(100, 200))
damage_rect = damage_powerup.get_rect(topleft=(500, 300))

images = [health_powerup,damage_powerup]


def draw_window(red, blue, red_bullets, blue_bullets, red_health, blue_health,powerups):
    WIN.blit(bg,(0,0))
    pygame.draw.rect(WIN,WHITE,BORDER)
    blue_health_text = HEALTH_FONT.render("Health: " + str(blue_health), 1, WHITE)
    WIN.blit(blue_health_text,(10,10))
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health),1,WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(blueship, (blue.x, blue.y))
    WIN.blit(redship, (red.x, red.y))

    for bullet in blue_bullets:
        pygame.draw.rect(WIN,BLUE,bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    for p in powerups:
        WIN.blit(p["image"],(p["rect"].x,p["rect"].y))
    pygame.display.update()

def handle_bullets(blue_bullets,red_bullets,blue,red):
    for bullet in blue_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            blue_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
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
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x+= VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    blue = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red_bullets = []
    blue_bullets = []
    red_health = 10
    blue_health = 10
    red_damage = 1
    blue_damage = 1

    powerups = []
    for _ in range(5):
        img = random.choice([health_powerup, damage_powerup])
        rect = img.get_rect()
        rect.x = random.randrange(WIDTH - rect.width)
        rect.y = random.randrange(HEIGHT - rect.height)
        powerups.append({"image": img, "rect": rect, "type": "health" if img == health_powerup else "damage"})


    clock = pygame.time.Clock()
    run= True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x + blue.width, blue.y + blue.height // 2, 10, 5)
                    blue_bullets.append(bullet)
                if event.key == pygame.K_m and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1+ blue_damage
            if event.type == BLUE_HIT:
                blue_health -= 1+ red_damage
        for p in powerups[:]:
            if blue.colliderect(p["rect"]):
                if p["type"] == "health":
                    blue_health += 1
                else:
                    blue_damage += 1
                powerups.remove(p)
            elif red.colliderect(p["rect"]):
                if p["type"] == "health":
                    red_health += 1
                else:
                    red_damage += 1
                powerups.remove(p)

        winner_text = ""
        if red_health <= 0:
            winner_text = "Blue Wins!"
        if blue_health <= 0:
            winner_text = "Red Wins!"
        if winner_text !="":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        blue_handle_movement(keys_pressed,blue)
        red_handle_movement(keys_pressed,red)

        handle_bullets(blue_bullets,red_bullets,blue,red)

        draw_window(red,blue,red_bullets,blue_bullets,red_health,blue_health,powerups)
    pygame.quit()

if __name__ == "__main__":
    main()







