import random
import sys
import pygame
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('player/player_walk_2.png').convert_alpha()
        self.player_walk_list = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.image = self.player_walk_list[self.player_index]
        self.jump = pygame.image.load('player/jump.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(80, 270))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 270:
            self.jump_sound.play()
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 270:
            self.rect.bottom = 270

    def animation_state(self):
        if self.rect.bottom < 270:
            self.image = self.jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk_list): self.player_index = 0
            self.image = self.player_walk_list[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 180
        else:
            snail_1 = pygame.image.load('snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 270

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900,1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

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

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

def player_animations():
    global player_surf, player_index
    if player_rect.bottom < 270:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk_list): player_index = 0
        player_surf = player_walk_list[int(player_index)]


pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('1st try game')
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.set_volume(0.1)
bg_music.play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()



score_font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 30)

sky_surface = pygame.image.load('Backgrounds/Sky.png').convert()
ground_surface = pygame.image.load('Backgrounds/ground.png').convert()

# score_surf = score_font.render('Score', True, (64,64,64))
# score_rect = score_surf.get_rect(center=(400, 50))

#Snail
snail_frame_1 = pygame.image.load('snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

# Fly
fly_frame_1 = pygame.image.load('fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]


obstacle_rect_list = []

player_walk_1 = pygame.image.load('player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('player/player_walk_2.png').convert_alpha()
player_walk_list = [player_walk_1, player_walk_2]
player_index = 0
player_surf = player_walk_list[player_index]
player_rect = player_surf.get_rect(midbottom=(60, 270))
player_jump = pygame.image.load('player/jump.png').convert_alpha()
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

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

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

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacles(choice(['fly','snail','snail'])))
                # if randint(0, 2):
                #     obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 270)))
                # else:
                #     obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 180)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]
                

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
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 270: player_rect.bottom = 270
        # player_animations()
        # screen.blit(player_surf, player_rect)

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #Obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collisions
        game_active = collision_sprite()
        # game_active = collisions(player_rect, obstacle_rect_list)

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