import sys
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('1st try game')
clock = pygame.time.Clock()
text_font = pygame.font.Font(None, 50)

sky_surface = pygame.image.load('Backgrounds/Sky.png').convert()
ground_surface = pygame.image.load('Backgrounds/ground.png').convert()
text_surface = text_font.render('Game', False, 'Black')
snail_surface = pygame.image.load('snail/snail1.png').convert_alpha()
# snail_x_pos = 700
snail_rect = snail_surface.get_rect(bottomright=(600, 270))

player_surf = pygame.image.load('player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(50, 270))
print(type(player_rect))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(sky_surface, (0,-100))
    screen.blit(ground_surface, (0, 270))
    screen.blit(text_surface, (300, 50))
    snail_rect.x -= 4
    if snail_rect.left < -100: snail_rect.right = 800
    screen.blit(snail_surface, snail_rect)
    screen.blit(player_surf, player_rect)
    pygame.display.update()
    clock.tick(60)