import pygame
import sys
import random

# Constants
WIDTH = 600
HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
SNAKE_SPEED = 10


# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Set background color
BG_COLOR = BLACK

class Snake:
    def __init__(self, color):
        self.color = color
        self.body = [(GRID_SIZE // 2, GRID_SIZE // 2)]
        self.direction = (0,1)

    def update(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, self.color, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BG_COLOR, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def check_collision(self):
        head = self.body[0]
        if (
            head[0] < 0
            or head[0] >= GRID_WIDTH
            or head[1] < 0
            or head[1] >= GRID_HEIGHT
            or self.body.count(head) > 1
        ):
            return True
        return False

    def grow(self):
        tail = self.body[-1]
        new_tail = (tail[0] + self.direction[0], tail[1] + self.direction[1])  # Fixed here
        self.body.append(new_tail)

    def change_direction(self, direction):
        if direction == "UP" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif direction == "DOWN" and self.direction != (0, -1):
            self.direction = (0, 1)
        elif direction == "LEFT" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif direction == "RIGHT" and self.direction != (-1, 0):
            self.direction = (1, 0)

class Food:
    def __init__(self, color):
        self.position = self.generate_position()
        self.color = color

    def generate_position(self):
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, screen):
        pygame.draw.rect(
            screen, self.color, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    # Generate random RGB values for snake, apple, and background color
    snake_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    apple_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    snake = Snake(snake_color)
    food = Food(apple_color)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle user input for changing snake direction
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")

        snake.update()

        # Check for collision with food
        if snake.body[0] == food.position:
            snake.grow()
            food.position = food.generate_position()

        # Check for collision with walls or self
        if snake.check_collision():
            print("Game Over!")
            pygame.quit()
            sys.exit()

        # Update background
        screen.fill(bg_color)  # Update background color

        # Draw snake and food on the screen
        snake.draw(screen)
        food.draw(screen)

        pygame.display.update()
        pygame.display.flip()
        clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    main()
