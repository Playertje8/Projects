import pygame
import os
import math
pygame.font.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First game!")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
FPS = 60
VEL = 5
BULLET_VEL = 10
BOM_VEL = 5
DROP_VEL = 4
MAX_BULLETS = 4
MAX_DROP = 3
MAX_BOM = 2
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
YELLOW_HIT_BOM = pygame.USEREVENT + 3
RED_HIT_BOM = pygame.USEREVENT + 4
YELLOW_HIT_DROP = pygame.USEREVENT + 5
RED_HIT_DROP = pygame.USEREVENT + 6
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)
RED_MINE = pygame.Rect(WIDTH/1.5 - 5, 0, 50, 25)
YELLOW_MINE = pygame.Rect(WIDTH/4 - 5, 0, 50, 25)

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 60)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "Spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "Spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


class Enemies:
    def __init__(self, color, name,) -> None:
        self.color = color
        self.name = name

    




def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_bom, yellow_bom, red_drop, yellow_drop):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    pygame.draw.rect(WIN, WHITE, RED_MINE)
    pygame.draw.rect(WIN, GREY, YELLOW_MINE)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))


    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bom in red_bom:
        pygame.draw.rect(WIN, RED, bom)

    for bom in yellow_bom:
        pygame.draw.rect(WIN, YELLOW, bom)

    for drop in red_drop:
        pygame.draw.rect(WIN, GREEN, drop)

    for drop in yellow_drop:
        pygame.draw.rect(WIN, PURPLE, drop)
         
    pygame.display.update()

def red_mine_movement(red_mine):
    # Calculate the horizontal movement based on the current time
    time_since_start = pygame.time.get_ticks() / 1000  # Convert milliseconds to seconds
    horizontal_offset = 197 * math.sin(time_since_start)

    # Update the red mine's position
    red_mine.x = WIDTH - red_mine.width - 197 - horizontal_offset
    red_mine.y = 0

    
def yellow_mine_movement(yellow_mine):
    # Calculate the horizontal movement based on the current time
    time_since_start = pygame.time.get_ticks() / 1000  # Convert milliseconds to seconds
    horizontal_offset = 199 * math.sin(time_since_start)

    # Update the yellow mine's position
    yellow_mine.x = 197 + horizontal_offset
    yellow_mine.y = 0


def yellow_handle_movement(keys_pressed, yellow):
    
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
            yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x : # RIGHT
            yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
            yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT -10: # DOWN
            yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
            red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
            red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
            red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT -10: # DOWN
            red.y += VEL




def handle_drops(yellow_drop, red_drop, yellow_mine, red_mine, yellow, red):
    for drop in yellow_drop:
        drop.y += DROP_VEL
        if yellow.colliderect(drop):
            pygame.event.post(pygame.event.Event(RED_HIT_DROP))
            yellow_drop.remove(drop)
        elif drop.x > WIDTH:
             yellow_drop.remove(drop)
    
    for drop in red_drop:
        drop.y += DROP_VEL
        if red.colliderect(drop):
            pygame.event.post(pygame.event.Event(YELLOW_HIT_DROP))
            red_drop.remove(drop)
        elif drop.x > WIDTH:
            red_drop.remove(drop)
    



def handle_bullets(yellow_bullets, red_bullets, yellow, red, yellow_bom, red_bom):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
             yellow_bullets.remove(bullet)
              
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
             red_bullets.remove(bullet)


    for bom in red_bom:
        bom.x -= BOM_VEL
        if yellow.colliderect(bom):
            pygame.event.post(pygame.event.Event(YELLOW_HIT_BOM))
            red_bom.remove(bom)
        elif bom.x < 0:
            red_bom.remove(bom)
    
    for bom in yellow_bom:
        bom.x += BOM_VEL
        if red.colliderect(bom):
            pygame.event.post(pygame.event.Event(RED_HIT_BOM))
            yellow_bom.remove(bom)
        elif bom.x > WIDTH:
             yellow_bom.remove(bom)

        

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /2, HEIGHT/2 - draw_text.get_height()/2))
    
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_mine = pygame.Rect(WIDTH/2 - 5, 0, 50, 25)
    yellow_mine = pygame.Rect(WIDTH/4 - 5, 0, 50, 25)

    
    yellow_drop = []
    red_drop = []
    red_bom = []
    yellow_bom = []
    red_bullets = []
    yellow_bullets = []
    red_health = 30
    yellow_health = 30

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x - 60 + red.width, red.y + red.height/2 - 2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m and len(red_bom) < MAX_BOM:
                    bom = pygame.Rect(red.x - 60 + red.width, red.y + red.height/2 - 2, 10, 10)
                    red_bom.append(bom)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and len(yellow_bom) < MAX_BOM:
                    bom = pygame.Rect(yellow.x - 60 + yellow.width, yellow.y + yellow.height/2 - 2, 10, 10)
                    yellow_bom.append(bom)
            
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and len(yellow_drop) < MAX_DROP:
                    drop = pygame.Rect(yellow.x + yellow.width, yellow_mine.y + yellow.height/2 - 2, 10, 5)
                    yellow_drop.append(drop)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and len(red_drop) < MAX_DROP:
                    drop = pygame.Rect(red_mine.x + 60+ red_mine.width, red_mine.y + red_mine.height/2 - 2, 10, 5)
                    red_drop.append(drop)



            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1

            if event.type == RED_HIT_BOM:
                 red_health -= 5

            if event.type == YELLOW_HIT_BOM:
                 yellow_health -= 5

            if event.type == YELLOW_HIT_DROP:
                 yellow_health -= 3

            if event.type == RED_HIT_DROP:
                red_health -= 3

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"
           

        if yellow_health <= 0:
              winner_text = "Red wins!"
              
        
        if winner_text != "":
            draw_winner(winner_text)
            break

            
        keys_pressed = pygame.key.get_pressed()


        handle_drops(yellow_drop, red_drop, yellow_mine, red_mine, yellow, red)
        yellow_mine_movement(YELLOW_MINE)
        red_mine_movement(RED_MINE)
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red, yellow_bom, red_bom)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_bom, yellow_bom, red_drop, yellow_drop)

    main()

if __name__ == "__main__":
    main()


