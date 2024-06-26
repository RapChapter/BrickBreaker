import pygame
import random
import math

# Initialisierung von Pygame
pygame.init()

# Farben definieren
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Fenstergröße definieren (HD-Standard)
width = 1920
height = 1080

# Spielfenster erstellen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Brick Breaker")

# Spielvariablen
paddle_width = 150
paddle_height = 10
ball_radius = 10
brick_width = 80
brick_height = 30
paddle_speed = 20
ball_speed = 10
initial_ball_angle = 0

# Spielerpositionen
paddle_pos = [width // 2 - paddle_width // 2, height - 50]
ball_pos = [width // 2, height - 70]

# Bricks
bricks = []
brick_lives = []

# Punktestand
score = 0

# Schriftart für den Punktestand
font = pygame.font.SysFont(None, 55)

# Level-Layouts definieren
levels = {
    'easy': [
        # Level 1
        [
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111"
        ],
        # Level 2
        [
            "000000000000",
            "011111111110",
            "011111111110",
            "011111111110",
            "011111111110",
            "011111111110",
            "011111111110",
            "011111111110",
            "011111111110",
            "011111111110",
            "011111111110",
            "011111111110",
            "011111111110",
            "000000000000",
            "000000000000"
        ],
        # Weitere Levels können hier hinzugefügt werden
    ],
    'medium': [
        # Level 1
        [
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111"
        ],
        # Weitere Levels können hier hinzugefügt werden
    ],
    'hard': [
        # Level 1
        [
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111",
            "111111111111"
        ],
        # Weitere Levels können hier hinzugefügt werden
    ]
}

current_level_index = 0
balls = [{'pos': ball_pos.copy(), 'speed': [ball_speed, -ball_speed]}]

# Funktion zum Zeichnen der Paddles, des Balls und der Bricks
def draw_objects():
    screen.fill(black)
    pygame.draw.rect(screen, blue, (*paddle_pos, paddle_width, paddle_height))
    for ball in balls:
        pygame.draw.circle(screen, red, ball['pos'], ball_radius)
    for brick, lives in zip(bricks, brick_lives):
        color = (255 - (lives * 25), 255, 255 - (lives * 25))
        pygame.draw.rect(screen, color, brick)
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

# Funktion zum Erstellen der Bricks
def create_bricks(level_layout):
    bricks.clear()
    brick_lives.clear()
    for row_idx, row in enumerate(level_layout):
        for col_idx, cell in enumerate(row):
            if cell == '1':
                bricks.append(pygame.Rect(col_idx * brick_width, row_idx * brick_height, brick_width, brick_height))
                brick_lives.append(random.randint(1, 3))

# Funktion zum Zeigen des Statusbildschirms (gewonnen/verloren)
def game_status_screen(status):
    screen.fill(black)
    if status == 'won':
        message = "You Won!"
    elif status == 'lost':
        message = "You Lost!"
    else:
        message = "Paused"
    text = font.render(message, True, white)
    restart_text = font.render("Press 'R' to Restart", True, white)
    menu_text = font.render("Press 'M' for Main Menu", True, white)
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 3))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2))
    screen.blit(menu_text, (width // 2 - menu_text.get_width() // 2, height // 2 + 50))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'restart'
                elif event.key == pygame.K_m:
                    return 'menu'

# Hauptspielschleife
def game_loop(difficulty):
    global score, paddle_pos, ball_pos, balls
    global current_level_index

    create_bricks(levels[difficulty][current_level_index])
    balls = [{'pos': ball_pos.copy(), 'speed': [ball_speed, -ball_speed]}]
    running = True
    clock = pygame.time.Clock()
    game_started = False
    show_aiming_line = True
    aiming_angle = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_started:
                    game_started = True
                    show_aiming_line = False
                    balls[0]['speed'] = [ball_speed * math.cos(aiming_angle), -ball_speed * math.sin(aiming_angle)]
                if event.key == pygame.K_ESCAPE:
                    result = game_status_screen('paused')
                    if result == 'restart':
                        create_bricks(levels[difficulty][current_level_index])
                        balls = [{'pos': ball_pos.copy(), 'speed': [ball_speed, -ball_speed]}]
                        game_started = False
                        show_aiming_line = True
                    elif result == 'menu':
                        return

        keys = pygame.key.get_pressed()

        # Paddle Steuerung
        if keys[pygame.K_LEFT] and paddle_pos[0] > 0:
            paddle_pos[0] -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_pos[0] < width - paddle_width:
            paddle_pos[0] += paddle_speed

        if game_started:
            for ball in balls[:]:
                ball['pos'][0] += ball['speed'][0]
                ball['pos'][1] += ball['speed'][1]

                # Ballkollision mit den Wänden
                if ball['pos'][0] <= ball_radius or ball['pos'][0] >= width - ball_radius:
                    ball['speed'][0] = -ball['speed'][0]
                if ball['pos'][1] <= ball_radius:
                    ball['speed'][1] = -ball['speed'][1]
                if ball['pos'][1] >= height:
                    balls.remove(ball)
                    if not balls:
                        result = game_status_screen('lost')
                        if result == 'restart':
                            create_bricks(levels[difficulty][current_level_index])
                            balls = [{'pos': ball_pos.copy(), 'speed': [ball_speed, -ball_speed]}]
                            game_started = False
                            show_aiming_line = True
                        elif result == 'menu':
                            return

                # Ballkollision mit dem Paddle
                paddle_rect = pygame.Rect(paddle_pos[0], paddle_pos[1], paddle_width, paddle_height)
                if paddle_rect.collidepoint(ball['pos'][0], ball['pos'][1] + ball_radius):
                    ball['speed'][1] = -ball['speed'][1]

                # Ballkollision mit den Bricks
                for brick in bricks[:]:
                    if brick.collidepoint(ball['pos'][0], ball['pos'][1]):
                        bricks.remove(brick)
                        score += 10
                        ball['speed'][1] = -ball['speed'][1]
                        break

        else:
            # Aiming line controls
            if keys[pygame.K_LEFT]:
                aiming_angle += 0.1  # Drehen nach links (Gegen den Uhrzeigersinn)
            if keys[pygame.K_RIGHT]:
                aiming_angle -= 0.1  # Drehen nach rechts (Im Uhrzeigersinn)

        draw_objects()

        # Drawing the aiming line
        if show_aiming_line:
            aim_x = int(ball_pos[0] + 100 * math.cos(aiming_angle))
            aim_y = int(ball_pos[1] - 100 * math.sin(aiming_angle))
            pygame.draw.line(screen, white, ball_pos, (aim_x, aim_y), 2)
            pygame.display.flip()

        clock.tick(60)

# Startbildschirm
def start_screen():
    global menu_selection
    menu_font = pygame.font.SysFont(None, 100)
    while True:
        screen.fill(black)
        title = menu_font.render("Brick Breaker", True, white)
        screen.blit(title, (width // 2 - title.get_width() // 2, height // 4))

        easy_text = font.render("Easy", True, green if menu_selection == 'easy' else white)
        medium_text = font.render("Medium", True, green if menu_selection == 'medium' else white)
        hard_text = font.render("Hard", True, green if menu_selection == 'hard' else white)
        exit_text = font.render("Exit", True, green if menu_selection == 'exit' else white)

        screen.blit(easy_text, (width // 2 - easy_text.get_width() // 2, height // 2))
        screen.blit(medium_text, (width // 2 - medium_text.get_width() // 2, height // 2 + 50))
        screen.blit(hard_text, (width // 2 - hard_text.get_width() // 2, height // 2 + 100))
        screen.blit(exit_text, (width // 2 - exit_text.get_width() // 2, height // 2 + 150))

        # Draw the arrow
        arrow = menu_font.render(">", True, green)
        if menu_selection == 'easy':
            screen.blit(arrow, (width // 2 - easy_text.get_width() // 2 - 50, height // 2))
        elif menu_selection == 'medium':
            screen.blit(arrow, (width // 2 - medium_text.get_width() // 2 - 50, height // 2 + 50))
        elif menu_selection == 'hard':
            screen.blit(arrow, (width // 2 - hard_text.get_width() // 2 - 50, height // 2 + 100))
        elif menu_selection == 'exit':
            screen.blit(arrow, (width // 2 - exit_text.get_width() // 2 - 50, height // 2 + 150))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if menu_selection == 'easy':
                        menu_selection = 'medium'
                    elif menu_selection == 'medium':
                        menu_selection = 'hard'
                    elif menu_selection == 'hard':
                        menu_selection = 'exit'
                    else:
                        menu_selection = 'easy'
                elif event.key == pygame.K_UP:
                    if menu_selection == 'exit':
                        menu_selection = 'hard'
                    elif menu_selection == 'hard':
                        menu_selection = 'medium'
                    elif menu_selection == 'medium':
                        menu_selection = 'easy'
                    else:
                        menu_selection = 'exit'
                elif event.key == pygame.K_RETURN:
                    if menu_selection == 'easy':
                        game_loop('easy')
                    elif menu_selection == 'medium':
                        game_loop('medium')
                    elif menu_selection == 'hard':
                        game_loop('hard')
                    elif menu_selection == 'exit':
                        pygame.quit()
                        exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_text.get_rect(topleft=(width // 2 - easy_text.get_width() // 2, height // 2)).collidepoint(event.pos):
                    game_loop('easy')
                elif medium_text.get_rect(topleft=(width // 2 - medium_text.get_width() // 2, height // 2 + 50)).collidepoint(event.pos):
                    game_loop('medium')
                elif hard_text.get_rect(topleft=(width // 2 - hard_text.get_width() // 2, height // 2 + 100)).collidepoint(event.pos):
                    game_loop('hard')
                elif exit_text.get_rect(topleft=(width // 2 - exit_text.get_width() // 2, height // 2 + 150)).collidepoint(event.pos):
                    pygame.quit()
                    exit()

menu_selection = 'easy'
start_screen()
