from traceback import print_tb

import pygame

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load('Main_menu.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK = (50, 50, 50)
font = pygame.font.SysFont(None, 48)

info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption('My first game on pygame')

player_1 = pygame.Rect(20, 50, 70, 200)
player_2 = pygame.Rect(width - 90, 50, 70, 200)
ball = pygame.Rect(width // 2, height // 2, 35, 35)

speed = 10
clock = pygame.time.Clock()
FPS = 60
cnt_player1 = 0
cnt_player2 = 0

ball_speed_x = 9
ball_speed_y = 9

state = "menu"

# Кнопки
play_button = pygame.Rect(300, 200, 200, 60)
exit_button = pygame.Rect(300, 300, 200, 60)

while True:
    # Проверка на выход
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Нажатие мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if play_button.collidepoint(mouse_pos):
                print("Игра началась!")
                state = 'game'

            if exit_button.collidepoint(mouse_pos):
                pygame.quit()


    if state == "menu":
        screen.fill(DARK)

        # Рисуем кнопки
        pygame.draw.rect(screen, GRAY, play_button)
        pygame.draw.rect(screen, GRAY, exit_button)

        # Текст кнопок
        play_text = font.render("Играть", True, WHITE)
        exit_text = font.render("Выход", True, WHITE)

        screen.blit(play_text, (340, 215))
        screen.blit(exit_text, (350, 315))

    if state == "game":


        ball.x += ball_speed_x
        ball.y += ball_speed_y
        if ball.top <= 0 or ball.bottom >= height:
            ball_speed_y *= -1
        if ball.colliderect(player_1):
            ball_speed_x *= -1
        if ball.colliderect(player_2):
            ball_speed_x *= -1
        if ball.right <= 0:
            cnt_player2 += 1
            ball.x = width // 2
            ball.y = height // 2
        if ball.left >= width:
            cnt_player1 += 1
            ball.x = width // 2
            ball.y = height // 2

        # Получение нажатий
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            state = 'menu'

        # Управление игроком 1
        if keys[pygame.K_w]:
            if player_1.y - speed > 0:
                player_1.y -= speed
        if keys[pygame.K_s]:
            if player_1.y + player_1.height < height:
                player_1.y += speed

        # Управление игроком 2
        if keys[pygame.K_UP]:
            if player_2.y - speed > 0:
                player_2.y -= speed
        if keys[pygame.K_DOWN]:
            if player_2.y + 200 + speed < height:
                player_2.y += speed

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (245, 19, 2), player_1)
        pygame.draw.rect(screen, (245, 152, 2), player_2)
        pygame.draw.rect(screen, (250, 243, 242), ball)
    clock.tick(FPS)
    pygame.display.flip()

