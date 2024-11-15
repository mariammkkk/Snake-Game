from tkinter import *
import random

# CONSTANTS
GAME_WIDTH = 700            # Width of the game window
GAME_HEIGHT = 700           # Height of the game window
SPEED = 25                  # Speed of the game (milliseconds per frame)
SPACE_SIZE = 50             # Size of each grid space (in pixels)
BODY_PARTS = 3              # Initial number of body parts for the snake
SNAKE_COLOR = "#00FF00"     
FOOD_COLOR = "#FF0000"      
BACKGROUND_COLOR = "#000000" 

# SNAKE CLASS
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS   # Initial size of the snake
        self.coordinates = []         # Coordinates of the snake's body parts
        self.squares = []             # Square objects representing the snake on the canvas

        # Initialize the snake's starting position
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])  # Start at the top-left corner

        # Create the snake's body on the canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# FOOD CLASS
class Food:
    def __init__(self):
        # Generate random coordinates
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE # Multiply by SPACE_SIZE to convert to pixels
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]  # Store the food's coordinates

        # Display food on canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food")

# Update the game for the next turn
def next_turn(snake, food):
    # Retrieve the current position of the snake's head
    x, y = snake.coordinates[0]

    # Determine the new position based on the direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Add the new head position to the snake's body
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check if the snake eats the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1  # Increment the score
        label.config(text="Score:{}".format(score))  # Update the score display
        canvas.delete("food")  # Remove the current food
        food = Food()  # Generate a new food object
    else:
        # Remove the snake's tail if no food is eaten
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions and end the game if any are detected
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

# CHANGE DIRECTION
def change_direction(new_direction):
    global direction

    # Ensure the snake cannot reverse direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

# CHECK COLLISIONS
def check_collisions(snake):
    x, y = snake.coordinates[0]  # Get the position of the snake's head

    # Check if the head collides with the walls
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    # Check if the head collides with any part of the snake's body
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

# END GAME
def game_over():
    # Clear the canvas and display a "Game Over" message
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

# Initialize main game window
window = Tk()
window.title("Snake game")  
window.resizable(False, False)

# Initialize game variables
score = 0
direction = 'down'

# Display score
label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

# Create canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Center the game window
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind arrow keys to control snake's direction
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Create the snake and food objects
snake = Snake()
food = Food()

# Start the game loop
next_turn(snake, food)

# Run the game window
window.mainloop()
