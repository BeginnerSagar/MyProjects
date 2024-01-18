import pygame
import time
import random
import os

pygame.init()

# Set up display
width, height = 800, 600
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
brown = (165, 42, 42)

# Set up clock
clock = pygame.time.Clock()

# Set up font
font = pygame.font.SysFont(None, 30)

# Set up snake
snake_block = 10
snake_speed = 15

# Set up levels
levels = [{"speed": 15, "obstacles": 5}, {"speed": 20, "obstacles": 8}, {"speed": 25, "obstacles": 12}]
current_level = 0

# Set up snake customization
snake_color = (0, 255, 0)
head_color = (0, 200, 0)

def our_snake(snake_block, snake_list):
    for x, y in snake_list:
        pygame.draw.rect(game_display, snake_color, [x, y, snake_block, snake_block])
    if len(snake_list) > 0:
        x, y = snake_list[-1]
        pygame.draw.rect(game_display, head_color, [x, y, snake_block, snake_block])

def message(msg, color, y_displace=0):
    mesg = font.render(msg, True, color)
    game_display.blit(mesg, [width / 6, height / 3 + y_displace])

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        x, y = obstacle
        pygame.draw.rect(game_display, white, [round(x), round(y), snake_block, snake_block])

def draw_borders():
    for x in range(0, width, snake_block):
        pygame.draw.rect(game_display, brown, [x, 0, snake_block, snake_block])
        pygame.draw.rect(game_display, brown, [x, height - snake_block, snake_block, snake_block])

    for y in range(0, height, snake_block):
        pygame.draw.rect(game_display, brown, [0, y, snake_block, snake_block])
        pygame.draw.rect(game_display, brown, [width - snake_block, y, snake_block, snake_block])

def game_loop():
    global current_level

    game_over = False
    game_close = False

    # Initialize obstacle_count and snake_speed
    obstacle_count = levels[current_level]["obstacles"]
    snake_speed = levels[current_level]["speed"]

    # Initialize snake
    snake_list = []
    snake_length = 1
    x1, y1 = width / 2, height / 2
    x1_change, y1_change = 0, 0

    # Initialize food position
    foodx, foody = round(random.randrange(0, width - snake_block) / 10.0) * 10.0, round(
        random.randrange(0, height - snake_block) / 10.0
    ) * 10.0

    # Initialize obstacles
    obstacles = [
        [round(random.randrange(0, width - snake_block) / 10.0) * 10.0,
         round(random.randrange(0, height - snake_block) / 10.0) * 10.0]
        for _ in range(obstacle_count)
    ]

    while not game_over:

        while game_close:
            game_display.fill(black)
            message("You Lost! Press Q-Quit or C-Play Again", red, -50)
            message(f"Your Score: {snake_length - 1}", white, 10)
            our_snake(snake_block, snake_list)
            draw_obstacles(obstacles)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    game_close = True
                    pause()

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        game_display.fill(black)

        # Draw borders
        draw_borders()

        # Draw obstacles
        draw_obstacles(obstacles)

        # Update snake position
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        # Check for collisions with obstacles
        for obstacle in obstacles:
            if snake_head == obstacle:
                game_close = True

        # Check if the snake eats food
        if x1 == foodx and y1 == foody:
            foodx, foody = round(random.randrange(0, width - snake_block) / 10.0) * 10.0, round(
                random.randrange(0, height - snake_block) / 10.0
            ) * 10.0
            while [foodx, foody] in snake_list or (foodx == x1 and foody == y1):
                foodx, foody = round(random.randrange(0, width - snake_block) / 10.0) * 10.0, round(
                    random.randrange(0, height - snake_block) / 10.0
                ) * 10.0
            snake_length += 1

        # Check if the snake collides with itself
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Draw the snake
        our_snake(snake_block, snake_list)

        # Draw the food
        pygame.draw.rect(game_display, red, [foodx, foody, snake_block, snake_block])

        # Display current score
        score = snake_length - 1
        score_text = font.render(f"Score: {score}", True, white)
        game_display.blit(score_text, [10, 10])

        pygame.display.update()

        # Check for level completion
        if score > 0 and score % 5 == 0:
            current_level += 1
            if current_level < len(levels):
                obstacle_count = levels[current_level]["obstacles"]
                snake_speed = levels[current_level]["speed"]
                obstacles = [
                    [round(random.randrange(0, width - snake_block) / 10.0) * 10.0,
                     round(random.randrange(0, height - snake_block) / 10.0) * 10.0]
                    for _ in range(obstacle_count)
                ]

        clock.tick(snake_speed)

    pygame.quit()
    quit()

def pause():
    paused = True

    message("Paused", white, -50)
    message("Press C to continue or Q to quit", white, 50)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(5)

game_loop()
