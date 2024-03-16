'''my_first_game.py'''

import os
import pygame
pygame.mixer.init()
pygame.font.init()


# Display set up
WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First Game")
BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)
FPS = 60
HEALTH_FONT = pygame.font.SysFont('times new roman',40)
WINNER_FONT = pygame.font.SysFont('times new roman',100)

# Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Bullets
BULLETS_VEL = 7
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
MAX_AMMO = 3

# Sounds
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'blaster.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hit.mp3'))
LOSER_EXPLOSION = pygame.mixer.Sound(os.path.join('Assets','boom.mp3'))

# Image inserts
SHIP_HEIGHT , SHIP_WIDTH = 50, 50
VEL = 2
SPACESHIP_IMAGE_A = pygame.image.load(
    os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SP = pygame.transform.rotate(pygame.transform.scale
                (SPACESHIP_IMAGE_A, (SHIP_WIDTH,SHIP_HEIGHT)),90)
SPACESHIP_IMAGE_B = pygame.image.load(
    os.path.join('Assets','spaceship_red.png'))
RED_SP = pygame.transform.rotate(pygame.transform.scale
            (SPACESHIP_IMAGE_B, (SHIP_WIDTH,SHIP_HEIGHT)),270)

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')) ,(WIDTH, HEIGHT))

# Draw to screen function
def draw_window(red, yellow, yellow_bullets, red_bullets, red_health, yellow_health):
    '''image inserts and positions, health and win texts, border '''
    WIN.blit(BACKGROUND,(0,0))
    pygame.draw.rect(WIN,BLACK, BORDER)
    red_health_text = HEALTH_FONT.render(
        "Health:" + str(red_health),1,WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health:" + str(yellow_health),1,WHITE)
    WIN.blit(red_health_text, (WIDTH-red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text, (10,10))
    WIN.blit(YELLOW_SP, (yellow.x,yellow.y))
    WIN.blit(RED_SP, (red.x,red.y))

    for bullets in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullets)
    for bullets in red_bullets:
        pygame.draw.rect(WIN,RED,bullets)
    pygame.display.update()

#Yellow spaceship movement function
def movement_yellow(keys_pressed, yellow):
    '''WSDA: Up, Down, Right, Left. '''
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # left
        yellow.x -=VEL
    if keys_pressed[pygame.K_d]and yellow.x + VEL + yellow.width < BORDER.x: # right
        yellow.x +=VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0 : # up
        yellow.y -=VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: # down
        yellow.y +=VEL

#Red spaceship movement function
def movement_red(keys_pressed, red):
    '''Arrow keys'''
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # left
        red.x -=VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH : # right
        red.x +=VEL
    if keys_pressed[pygame.K_UP] and red.y + VEL > 0: # up
        red.y -=VEL
    if keys_pressed[pygame.K_DOWN]and red.y + VEL + red.height < HEIGHT: # down
        red.y +=VEL

# Bullet collision and out of bound events
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    '''Removes out of bound bullets and collision bullets '''
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    '''Winner text styling'''
    draw_text = WINNER_FONT.render (text, 1,WHITE )
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2,
                         HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

# Main game function
def main():
    '''variable, clock, while loop with events and winner, called functions'''
    yellow = pygame.Rect(100,300, SHIP_WIDTH,SHIP_HEIGHT)
    red = pygame.Rect(700,300, SHIP_WIDTH,SHIP_HEIGHT)
    yellow_bullets = []
    yellow_health = 10
    red_bullets=[]
    red_health= 10

    clock = pygame.time.Clock()
    run = True
    run =True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event. type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets)< MAX_AMMO:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2-2,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets)   < MAX_AMMO :
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2-2,10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
            LOSER_EXPLOSION.play()
        if yellow_health <= 0 :
            winner_text = "Red Wins!"
            LOSER_EXPLOSION.play()
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        movement_yellow(keys_pressed,yellow)
        movement_red(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        draw_window(red,yellow,yellow_bullets,red_bullets,red_health,yellow_health)
main()


if __name__ == "__main__":
    main()
