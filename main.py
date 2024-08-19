import sys
import pygame

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surf = score_font.render(f'{current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center=(400,50))
    screen.blit(score_surf, score_rect)


pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('1st try game')
clock = pygame.time.Clock()
game_active = True
start_time = 0

score_font = pygame.font.Font(None, 40)

sky_surface = pygame.image.load('Backgrounds/Sky.png').convert()
ground_surface = pygame.image.load('Backgrounds/ground.png').convert()

# score_surf = score_font.render('Score', True, (64,64,64))
# score_rect = score_surf.get_rect(center=(400, 50))

snail_surface = pygame.image.load('snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomright=(600, 270))

player_surf = pygame.image.load('player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(60, 270))
player_gravity = 0


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
                snail_rect.right = 800

    if game_active:
        screen.blit(sky_surface, (0,-100))
        screen.blit(ground_surface, (0, 270))
        display_score()
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, width=5)
        # screen.blit(score_surf, score_rect)
        # pygame.draw.line(screen, 'Red', (0,0), (800, 400), width=2)

        snail_rect.x -= 4
        if snail_rect.left < -100: snail_rect.right = 800
        screen.blit(snail_surface, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 270: player_rect.bottom = 270
        screen.blit(player_surf, player_rect)

        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill('red')


    pygame.display.update()
    clock.tick(60)