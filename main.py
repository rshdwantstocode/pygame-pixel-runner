import sys
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('1st try game')
clock = pygame.time.Clock()

score_font = pygame.font.Font(None, 40)

sky_surface = pygame.image.load('Backgrounds/Sky.png').convert()
ground_surface = pygame.image.load('Backgrounds/ground.png').convert()

score_surf = score_font.render('Score', True, (64,64,64))

snail_surface = pygame.image.load('snail/snail1.png').convert_alpha()
# snail_x_pos = 700
snail_rect = snail_surface.get_rect(bottomright=(600, 270))

score_rect = score_surf.get_rect(center=(400, 50))

player_surf = pygame.image.load('player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(60, 270))
player_gravity = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if player_rect.collidepoint(event.pos):
                player_gravity -= 20
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_gravity = -20
        # if event.type == pygame.KEYUP:
        #     print('key up')

    screen.blit(sky_surface, (0,-100))
    screen.blit(ground_surface, (0, 270))

    pygame.draw.rect(screen, '#c0e8ec', score_rect)
    pygame.draw.rect(screen, '#c0e8ec', score_rect, width=5)
    screen.blit(score_surf, score_rect)
    # pygame.draw.line(screen, 'Red', (0,0), (800, 400), width=2)

    snail_rect.x -= 4
    if snail_rect.left < -100: snail_rect.right = 800
    screen.blit(snail_surface, snail_rect)

    # Player
    player_gravity += 1
    player_rect.y += player_gravity
    screen.blit(player_surf, player_rect)


    # key = pygame.key.get_pressed()
    # if key[pygame.K_SPACE]:
    #     print('jump')

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())

    pygame.display.update()
    clock.tick(60)