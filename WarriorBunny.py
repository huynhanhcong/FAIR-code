import pygame
from pygame.locals import *
import math
import random
import sys

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Load background images
background_start = pygame.image.load("Background_start.png")
background = pygame.image.load("Background_ingame.png")

# Load the start button image
start_button_img = pygame.image.load("start.png")
start_button_rect = start_button_img.get_rect(center=(width // 2, height // 2.45))

keys = [False, False, False, False]
playerpos = [100, 100]
acc = [0, 0]
arrows = []
badtimer = 100
badtimer1 = 0
badguys = []
healthvalue = 100
pygame.mixer.init()

player = pygame.image.load("dude.png")
arrow = pygame.image.load("bullet.png")
badguyimg = pygame.image.load("enemy_1.png")
badguyA_img = pygame.image.load("enemy_2.png")
healthbar = pygame.image.load("healthbar.png")
health = pygame.image.load("health.png")
youlose = pygame.image.load("youlose.png")
youwin = pygame.image.load("youwin.png")
enemy_attack_img = pygame.image.load("-10.png")
replay_button_img = pygame.image.load("replay.png")
replay_button_rect = replay_button_img.get_rect(center=(width // 2, height // 2))
castle = pygame.image.load("castle.png")
hit = pygame.mixer.Sound("explode.wav")
enemy = pygame.mixer.Sound("enemy.wav")
shoot = pygame.mixer.Sound("shoot.mp3")
hit.set_volume(0.1)
enemy.set_volume(0.1)
shoot.set_volume(0.15)
pygame.mixer.music.load('moonlight.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.15)
def reset_game():
    global playerpos, acc, arrows, badtimer, badtimer1, badguys, healthvalue, enemy_attack_position, last_attack_time, start_time, running
    playerpos = [100, 100]
    acc = [0, 0]
    arrows = []
    badtimer = 100
    badtimer1 = 0
    badguys = []
    healthvalue = 100
    enemy_attack_position = None
    last_attack_time = 0
    start_time = pygame.time.get_ticks()
    running = False  # Set running to False initially
enemy_attack_position = None
last_attack_time = 0
start_time = pygame.time.get_ticks()
running = False
exitcode = -1
enemy_speed = 7
enemy_attack_duration = 1000
while True:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
        elif event.type == pygame.KEYUP:
            if event.key == K_w:
                keys[0] = False
            elif event.key == K_a:
                keys[1] = False
            elif event.key == K_s:
                keys[2] = False
            elif event.key == K_d:
                keys[3] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not running:
                if start_button_rect.collidepoint(event.pos):
                    reset_game()
                    running = True  # Set running to True when the button is clicked
                continue
            shoot.play()
            position = pygame.mouse.get_pos()
            acc[1] += 1
            arrows.append([math.atan2(position[1] - (playerpos[1] + 32), position[0] - (playerpos[0] + 26)),
                           playerpos[0] + 32, playerpos[1] + 32])
    screen.blit(background_start, (0, 0))  # Display the start background image
    if not running:
        screen.blit(start_button_img, start_button_rect.topleft)
        pygame.display.flip()
        if start_button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:  # Check if the left mouse button is pressed
                reset_game()
                running = True  # Set running to True when the button is clicked
        clock.tick(30)
        continue  # Skip the rest of the game loop if not running
    badtimer -= 1
    if badtimer == 0:
        badguys.append([640, random.randint(50, 430), random.choice(["default", "typeA"])])
        badtimer = 100 - (badtimer1 * 2)
        if badtimer1 >= 35:
            badtimer1 = 35
        else:
            badtimer1 += 5
        if enemy_speed < 25:
            enemy_speed += 0.1
    screen.blit(background, (0, 0))
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1] - (playerpos[1] + 32), position[0] - (playerpos[0] + 26))
    playerrot = pygame.transform.rotate(player, 360 - angle * 57.29)
    playerpos1 = (playerpos[0] - playerrot.get_rect().width / 2, playerpos[1] - playerrot.get_rect().height / 2)
    screen.blit(playerrot, playerpos1)
    for bullet in arrows:
        velx = math.cos(bullet[0]) * 10
        vely = math.sin(bullet[0]) * 10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            arrows.remove(bullet)
    for projectile in arrows:
        arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
        screen.blit(arrow1, (projectile[1], projectile[2]))
    for badguy in badguys:
        badguy[0] -= enemy_speed
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 64:
            hit.play()
            healthvalue -= 10
            badguys.remove(badguy)
            enemy_attack_position = (badguy[0], badguy[1])
            last_attack_time = current_time
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                enemy.play()
                acc[0] += 1
                arrows.remove(bullet)
                badguys.remove(badguy)
    for badguy in badguys:
        if badguy[2] == "default":
            screen.blit(badguyimg, (badguy[0], badguy[1]))
        elif badguy[2] == "typeA":
            screen.blit(badguyA_img, (badguy[0], badguy[1]))
    if enemy_attack_position is not None and current_time - last_attack_time <= enemy_attack_duration:
        screen.blit(enemy_attack_img, enemy_attack_position)
    font = pygame.font.Font(None, 24)
    elapsed_time = (current_time - start_time) if running else 0
    minutes = (90000 - elapsed_time) // 60000
    seconds = ((90000 - elapsed_time) // 1000) % 60
    survivedtext = font.render(f"{minutes:02d}:{seconds:02d}", True, (0, 0, 0))
    textRect = survivedtext.get_rect()
    textRect.topright = [635, 5]
    screen.blit(survivedtext, textRect)
    screen.blit(healthbar, (5, 5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1 + 8, 8))
    if pygame.time.get_ticks() >= 90000 or healthvalue <= 0:
        exitcode = 1  # Player wins
    if healthvalue <= 40:
        exitcode = 0  # Player loses
    if acc[1] != 0:
        accuracy = acc[0] * 1.0 / acc[1] * 100
    else:
        accuracy = 0
    while exitcode != -1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button_rect.collidepoint(event.pos):
                    reset_game()
                    exitcode = -1
        if exitcode == 0:
            screen.blit(youlose, (0, 0))
            replay_button_rect.center = (width // 2, height // 2)
            screen.blit(replay_button_img, replay_button_rect.topleft)
        elif exitcode == 1:
            screen.blit(youwin, (0, 0))
        pygame.display.flip()
        clock.tick(30)
    else:
        replay_button_rect.center = (-100, -100)  # Move the replay button off-screen
        pygame.display.flip()
        clock.tick(30)