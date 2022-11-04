from tkinter import *
import random
from playsound import playsound

GAME_HEIGHT =600
GAME_WIDTH = 600
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#64ff0a"
BACKGROUND_COLOR = "black"
FOOD_COLOR = "#ff2d03"


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])
        
        for x,y in self.coordinates:
            square = canvas.create_rectangle(x,y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self):

        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x,y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

        pass

def next_turn(snake, food):
    
    x , y = snake.coordinates[0]
    if direction == "up":
        if y == 0:
            y = ((GAME_HEIGHT/SPACE_SIZE) - 1) * SPACE_SIZE
        else:
            y-=SPACE_SIZE
    if direction == "down":
        if y == ((GAME_HEIGHT/SPACE_SIZE) - 1) * SPACE_SIZE:
            y = 0
        else:
            y+=SPACE_SIZE
    if direction == "left":
        if x == 0:
            x = ((GAME_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE
        else:
            x-=SPACE_SIZE
    if direction == "right":
        if x == ((GAME_HEIGHT/SPACE_SIZE) - 1) * SPACE_SIZE:
            x = 0
        else:
            x+=SPACE_SIZE

    snake.coordinates.insert(0,(x,y))

    square = canvas.create_rectangle(x,y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")

    snake.squares.insert(0, square)

    if x== food.coordinates[0] and y== food.coordinates[1]:
        global score
        score+=1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)
    pass

def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

    pass

def check_collisions(snake):
    x , y = snake.coordinates[0]
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            global score
            # label.config(text="GAME OVER! FinalScore:{}".format(score))
            print("Game over\n Final Score = {}".format(score))
            return True
    return False

def game_over():
    global score
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 70),
    text="GAME OVER \n SCORE={}".format(score), tag = "gameover", fill = "red")
    # playsound("over.mp3")
    pass


window=Tk()
window.title("Snek")
window.resizable(False, False)


score = 0
direction = "down"

label= Label(window, text="Score: {}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height = GAME_HEIGHT, width = GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width)/2 - (window_width)/2)
y = int((screen_height)/2 - (window_height)/2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")


window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)
# playsound("game.mp3")

window.mainloop()