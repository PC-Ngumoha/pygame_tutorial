"""
main.py: pygame tutorial
"""
import pygame
import os

pygame.font.init()  # Initialize pygame fonts
pygame.mixer.init()  # Initialize pygame sound

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BULLET_WIDTH, BULLET_HEIGHT = 10, 5

# Creating custom pygame events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('Comic Sans MS', 40)
WINNER_FONT = pygame.font.SysFont('Comic Sans MS', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'Gun+Silencer.mp3'))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,
                           (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90  # 90 degrees
)

SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(
        RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270  # 270 degrees
)

# Change screen title
pygame.display.set_caption("First Game")


def draw_window(yellow, red, red_bullets, yellow_bullets, red_health, yellow_health):
    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    # Draw border
    pygame.draw.rect(WIN, BLACK, BORDER)

    # Render health score
    red_health_text = HEALTH_FONT.render(
        f"Health: {str(red_health)}", 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        f"Health: {str(yellow_health)}", 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # Render sprites
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Render bullets if any
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def handle_yellow_mvmt(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # Left 'a' key
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # Right 'd' key
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # Up 'w' key
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 20:  # Down 's' key
        yellow.y += VEL


def handle_red_mvmt(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 20:
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(winner_text, (WIDTH//2 - winner_text.get_width() /
             2, HEIGHT//2 - winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    yellow = pygame.Rect(100, 250, SPACESHIP_WIDTH,
                         SPACESHIP_HEIGHT)  # On the left
    red = pygame.Rect(700, 250, SPACESHIP_WIDTH,
                      SPACESHIP_HEIGHT)  # On the right

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    game_running = True
    while game_running:
        clock.tick(FPS)  # Ensures frame-rate of 60fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()  # So the game ends when we quit

            # Trigger bullet firing
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # Responding to spaceship getting hit
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        # Checking for winner.
        if red_health <= 0:
            winner_text = "YELLOW WINS !!!"

        if yellow_health <= 0:
            winner_text = "RED WINS !!!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        # print(red_bullets, yellow_bullets)
        # Listening for key press events
        keys_pressed = pygame.key.get_pressed()

        # For the Yellow Spaceship
        handle_yellow_mvmt(keys_pressed, yellow)

        # For the Red Spaceship
        handle_red_mvmt(keys_pressed, red)

        # For bullets movements
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()


if __name__ == '__main__':
    main()
