import sys
import pygame
from random import randint


def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surf = score_font.render(f'{current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center=(400,50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 270: screen.blit(snail_surface, obstacle_rect)
            else: screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True


pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('1st try game')
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0

score_font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 30)

sky_surface = pygame.image.load('Backgrounds/Sky.png').convert()
ground_surface = pygame.image.load('Backgrounds/ground.png').convert()

# score_surf = score_font.render('Score', True, (64,64,64))
# score_rect = score_surf.get_rect(center=(400, 50))

#Obstacles
snail_surface = pygame.image.load('snail/snail1.png').convert_alpha()
fly_surface = pygame.image.load('fly/Fly1.png').convert_alpha()


obstacle_rect_list = []

player_surf = pygame.image.load('player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(60, 270))
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load('player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1.5)
player_stand_rect = player_stand.get_rect(center=(400, 200))

title_surf = title_font.render('Pixel runner', True, (111, 196, 169))
title_rect = title_surf.get_rect(center=(400,80))

# title_score_surf = title_font.render('Score', True, (64,64,64))
# title_score_rect = title_score_surf.get_rect(center=(400,100))

title_start_surf = title_font.render('"Press SPACE to start the game"', True, (111, 196, 169))
title_start_rect = title_start_surf.get_rect(center=(400, 300))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            if player_rect.bottom >= 270:
                if event.type == pygame.MOUSEBUTTONUP:
                    if player_rect.collidepoint(event.pos):
                        player_gravity -= 20
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900,1100), 270)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 180)))

    if game_active:
        screen.blit(sky_surface, (0,-100))
        screen.blit(ground_surface, (0, 270))
        score = display_score()
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, width=5)
        # screen.blit(score_surf, score_rect)
        # pygame.draw.line(screen, 'Red', (0,0), (800, 400), width=2)

        # snail_rect.x -= 4
        # if snail_rect.left < -100: snail_rect.right = 800
        # screen.blit(snail_surface, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 270: player_rect.bottom = 270
        screen.blit(player_surf, player_rect)

        #Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collisions
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surf, title_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = title_font.render(f'Your Score: {score}', True, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400,300))

        if score == 0: screen.blit(title_start_surf, title_start_rect)
        else: screen.blit(score_message, score_message_rect)


    pygame.display.update()
    clock.tick(60)