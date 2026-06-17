import pygame

pygame.init()

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK = (50, 50, 50)
L_COlOR = (70, 70, 70)
font = pygame.font.SysFont(None, 48)

state = "menu"
game_mode = "players"  # Новая переменная: "bot" или "players"

running = True

info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption('My first game on pygame')

screen.fill((0, 0, 0))
pygame.display.flip()

pygame.mixer.init()
pygame.mixer.music.load('Main_menu.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

player_1 = pygame.Rect(20, 50, 70, 200)
player_2 = pygame.Rect(width - 90, 50, 70, 200)
ball = pygame.Rect(width // 2, height // 2, 35, 35)

background = pygame.image.load('Background_tennis_table.png')
p_1_image = pygame.image.load('Player_one-Photoroom.png').convert_alpha()
p_2_image = pygame.image.load('Player_two-Photoroom.png').convert_alpha()

background = pygame.transform.scale(background, (width, height))
p_1_image = pygame.transform.scale(p_1_image, (70, 200))
p_2_image = pygame.transform.scale(p_2_image, (70, 200))

speed = 10
bot_speed = 10  # Скорость бота (чуть меньше мяча, чтобы его можно было победить)
clock = pygame.time.Clock()
FPS = 60
cnt_player1 = 0
cnt_player2 = 0

ball_speed_x = 9
ball_speed_y = 9

# Кнопки
play_button = pygame.Rect(width // 2 - 100, height // 2 - 50, 200, 60)
exit_button = pygame.Rect(width // 2 - 100, height // 2 + 50, 200, 60)
bot_button = pygame.Rect(width // 2 - 100, height // 2 - 50, 200, 60)
players_button = pygame.Rect(width // 2 - 100, height // 2 + 50, 200, 60)

while running:
    # Проверка на выход
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Нажатие мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if state == 'menu':
                if play_button.collidepoint(mouse_pos):
                    state = 'gamemode'
                if exit_button.collidepoint(mouse_pos):
                    running = False  # Корректный выход из цикла

            elif state == 'gamemode':
                if bot_button.collidepoint(mouse_pos):
                    game_mode = "bot"  # Включаем режим с ботом
                    state = 'game'
                if players_button.collidepoint(mouse_pos):
                    game_mode = "players"  # Включаем режим на двоих
                    state = 'game'

    keys = pygame.key.get_pressed()

    if state == "menu":
        screen.fill((0, 0, 0))

        # Рисуем кнопки
        pygame.draw.rect(screen, GRAY, play_button)
        pygame.draw.rect(screen, GRAY, exit_button)

        # Текст кнопок
        play_text = font.render("Играть", True, WHITE)
        exit_text = font.render("Выход", True, WHITE)

        play_rect = play_text.get_rect(center=play_button.center)
        exit_rect = exit_text.get_rect(center=exit_button.center)

        screen.blit(play_text, play_rect)
        screen.blit(exit_text, exit_rect)

    if state == "gamemode":
        screen.fill((0, 0, 0))

        # ИСПРАВЛЕНО: Рисуем правильные кнопки для выбора режима
        pygame.draw.rect(screen, GRAY, bot_button)
        pygame.draw.rect(screen, GRAY, players_button)

        bot_text = font.render("С Ботом", True, WHITE)
        players_text = font.render("2 Игрока", True, WHITE)

        bot_rect = bot_text.get_rect(center=bot_button.center)
        players_rect = players_text.get_rect(center=players_button.center)

        screen.blit(bot_text, bot_rect)
        screen.blit(players_text, players_rect)

    if state == "game":

        # Движение мяча
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

        if keys[pygame.K_ESCAPE]:
            state = 'menu'

        # Управление игроком 1 (Всегда клавиши W и S)
        if keys[pygame.K_w]:
            if player_1.y > 0:
                player_1.y -= speed
        if keys[pygame.K_s]:
            if player_1.y + player_1.height < height:
                player_1.y += speed

        # Управление игроком 2 / Бот
        if game_mode == "players":
            # Если режим "2 игрока" — управляет человек стрелочками
            if keys[pygame.K_UP]:
                if player_2.y > 0:
                    player_2.y -= speed
            if keys[pygame.K_DOWN]:
                if player_2.y + player_2.height < height:
                    player_2.y += speed

        elif game_mode == "bot":
            # ИСПРАВЛЕНО: Алгоритм ИИ для Игрока 2
            if player_2.centery < ball.centery - 15:
                player_2.y += bot_speed
            elif player_2.centery > ball.centery + 15:
                player_2.y -= bot_speed

            # Ограничение ИИ, чтобы не вылетал за экран
            if player_2.top < 0:
                player_2.top = 0
            if player_2.bottom > height:
                player_2.bottom = height

        # Отрисовка графики
        screen.blit(background, (0, 0))
        screen.blit(p_1_image, (player_1.x, player_1.y))
        screen.blit(p_2_image, (player_2.x, player_2.y))
        pygame.draw.rect(screen, (250, 243, 242), ball)

        # Выравнивание счетчиков по центру экрана
        text_1 = font.render(str(cnt_player1), True, WHITE)
        screen.blit(text_1, (width // 2 - 100, 50))

        text_2 = font.render(str(cnt_player2), True, WHITE)
        screen.blit(text_2, (width // 2 + 70, 50))

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
