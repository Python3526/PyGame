import pygame
import db

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Adventure')
clock = pygame.time.Clock()
text_font = pygame.font.SysFont('Arial', 25)

main_surface = pygame.image.load('pictures/bright_day1.png').convert()
basic_player = pygame.image.load('pictures/basic_player1.png').convert_alpha()
basic_player_position = basic_player.get_rect(midleft=(0, 368))

enemy_level1 = pygame.image.load('pictures/enemy_level_1.png').convert_alpha()
enemy_level1_position = enemy_level1.get_rect(midleft=(900, 380))

bullet_64 = pygame.image.load('pictures/bullet_64.png').convert_alpha()
bullet_64_position = bullet_64.get_rect(midleft=(-5, 60))

thunder_32 = pygame.image.load('pictures/thunder_32.png').convert_alpha()
thunder_32_position = thunder_32.get_rect(midleft=(400, 368))

game_over = pygame.image.load('pictures/game_over.png').convert_alpha()
game_over_position = game_over.get_rect(midleft=(350, 150))

game_runner = True

while True:
    mouse_position = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and basic_player_position.y == 332:
                db.jumb = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_r:
                game_runner = True
                basic_player_position = basic_player.get_rect(midleft=(0, 368))
                enemy_level1_position = enemy_level1.get_rect(midleft=(900, 380))
                db.total_nitro = 0
                db.total_bullet = 0

    if game_runner:
        nitro_text = text_font.render(f"={int(db.total_nitro)}", True, (255, 0, 100))
        bullet_text = text_font.render(f"={int(db.total_bullet)}", True, (255, 0, 100))

        screen.blit(main_surface, (0, -130))
        screen.blit(basic_player, basic_player_position)

        screen.blit(enemy_level1, enemy_level1_position)
        enemy_level1_position.x -= 1

        screen.blit(thunder_32, (-6, 6))

        screen.blit(bullet_64, bullet_64_position)

        screen.blit(nitro_text, (20, 10))
        screen.blit(bullet_text, (20, 50))

        screen.blit(thunder_32, thunder_32_position)

        if int(db.nitro_movement) >= 0 and not db.nitro_lore_checker:
            thunder_32_position.y -= 1
            db.nitro_movement -= 1
            if db.nitro_movement == 0:
                db.nitro_lore_checker = True
        if int(db.nitro_movement) <= 100 and db.nitro_lore_checker:
            thunder_32_position.y += 1
            db.nitro_movement += 1
            if db.nitro_movement == 100:
                db.nitro_lore_checker = False

        if db.jumb:
            if db.jumb_lore > 0:
                db.jumb_lore -= 1
                basic_player_position.y -= db.speed_jumb
            else:
                db.jumb_lore = 8
                db.jumb = False

        if not db.jumb and basic_player_position.y < 332:
            basic_player_position.y += 3
        if basic_player_position.y < 200:
            basic_player_position.y += 5
        if basic_player_position.y < 100:
            basic_player_position.y += 10

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            basic_player_position.x += db.speed_forward
        if keys[pygame.K_d] and keys[pygame.K_LSHIFT] and db.total_nitro > 0:
            basic_player_position.x += db.speed_forward * 2
            db.total_nitro -= 1

        if keys[pygame.K_a]:
            screen.blit(pygame.transform.flip(basic_player, True, False), basic_player_position)
            basic_player_position.x -= db.speed_backward
        if keys[pygame.K_a] and keys[pygame.K_LSHIFT] and db.total_nitro > 0:
            screen.blit(pygame.transform.flip(basic_player, True, False), basic_player_position)
            basic_player_position.x -= db.speed_backward * 2
            db.total_nitro -= 1

        if thunder_32_position.colliderect(basic_player_position):
            thunder_32_position.x += 100
            db.total_nitro += db.bonus_nitro

        if basic_player_position.colliderect(enemy_level1_position):
            game_runner = False

    else:
        # screen.fill((0, 0, 0))
        screen.blit(game_over, game_over_position)

    pygame.display.update()
    clock.tick(80)
