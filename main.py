"""
main.py: pygame tutorial
"""
import pygame
import os

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
FPS = 60
VEL = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,
                           (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90  # 90 degrees
)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(
        RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270  # 270 degrees
)

# Change screen title
pygame.display.set_caption("First Game")


def draw_window(yellow, red):
    WIN.fill(WHITE)
    # Render sprites
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    pygame.display.update()


def handle_yellow_mvmt(keys_pressed, yellow):
    if keys_pressed[pygame.K_a]:  # Left 'a' key
        yellow.x -= VEL
    if keys_pressed[pygame.K_d]:  # Right 'd' key
        yellow.x += VEL
    if keys_pressed[pygame.K_w]:  # Up 'w' key
        yellow.y -= VEL
    if keys_pressed[pygame.K_s]:  # Down 's' key
        yellow.y += VEL


def handle_red_mvmt(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT]:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT]:
        red.x += VEL
    if keys_pressed[pygame.K_UP]:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN]:
        red.y += VEL


def main():
    yellow = pygame.Rect(100, 250, SPACESHIP_WIDTH,
                         SPACESHIP_HEIGHT)  # On the left
    red = pygame.Rect(700, 250, SPACESHIP_WIDTH,
                      SPACESHIP_HEIGHT)  # On the right

    clock = pygame.time.Clock()
    game_running = True
    while game_running:
        clock.tick(FPS)  # Ensures frame-rate of 60fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        # Listening for key press events
        keys_pressed = pygame.key.get_pressed()

        # For the Yellow Spaceship
        handle_yellow_mvmt(keys_pressed, yellow)

        # For the Red Spaceship
        handle_red_mvmt(keys_pressed, red)

        draw_window(yellow, red)

    pygame.quit()


if __name__ == '__main__':
    main()
