


import turtle
import functools
import random
import time



#turtle objects
obstacle_turtle = turtle.Turtle()
character_turtle = turtle.Turtle()
treasure_turtle= turtle.Turtle()
monster_turtle = turtle.Turtle()


window = turtle.Screen()
window.title("Maze Runner by Dominic_Domingo")
window.bgcolor("black")
window.setup(width=0.3, height=0.5)
width = window.window_width()
height = window.window_height()
window.tracer(0)
turtle.hideturtle()
turtle.penup()
turtle.color("white")
turtle.goto(0, -width//1.7)


# Settings
DEFAULT_TEXT_FILE = "maze_1.txt"
MAZE_TEXT_FILE = "maze_1.txt"
BLOCK_STR = OB = 'X'  # OB --> Out of Bounds
PLAYER_STR = 'C'
TREASURE_STR = 'T'
MONSTER_STR = 'M'
EMPTY_STR = '.'
ALIVE = 0
DEAD = 1
WIN = 2
PLAYER_STATE = ALIVE
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3
KEY_LEFT = "a"
KEY_UP = "w"
KEY_RIGHT = "d"
KEY_DOWN = "s"
MONSTER_SPEED_IN_SEC = 1  # in seconds
row_pos = 0
col_pos = 0

# Text feedback for winning the game, or losing the game
game_end_list = []
game_win_list = []


# Classes
# --------------------------------------------------------
# A Cell object stores a Turtle object and its coordinates
class Cell:
    def __init__(self, x, y, turtle_obj):
        self.x = x
        self.y = y
        self.turtle_obj = turtle_obj


# A Player is a Cell. It also has a 'state' property,
# where the state keeps track of whether the Player is either
# ALIVE, DEAD, or WIN (the last of which is the brief state
# where the Player has found the treasure and the game is about
# to be over)
class Player(Cell):
    def __init__(self, x, y, turtle_player, state):
        super().__init__(x, y, turtle_player)
        self.state = state


# A Monster is a Cell. It also has the 'direction' property,
# which keeps track of the direction that the monster is
# currently going, either LEFT, UP, DOWN, or RIGHT
class Monster(Cell):
    def __init__(self, x, y, turtle_player, direction=UP):
        super().__init__(x, y, turtle_player)
        self.direction = direction
      
# treasure class
class Treasure(Cell):
    def __init__(self, x, y, turtle_player, direction=UP):
        super().__init__(x, y, turtle_player)
        self.direction = direction
# obstacle class
      
class Obstacle(Cell):
    def __init__(self, x, y, turtle_player, direction=UP):
        super().__init__(x, y, turtle_player)
        self.direction = direction
# Functions
# --------------------------------------------------
# Creates an empty n x n grid of the given data type
def make_grid(size, data_type):
    return [[data_type] * size for _ in range(size)]


# Creates a grid of strings that represent the images
# in the game. These strings are PLAYER_STR, MONSTER_STR,
# TREASURE_STR, BLOCK_STR, and EMPTY_STR, the last of which
# represents empty spaces in the grid
def create_maze(file=DEFAULT_TEXT_FILE):
    cell_maze = [[]]

    file_object = open(file, "r")
    row = 0
    for line in file_object:
        cell_list = line.split(" ")
        for cell in cell_list:
            cell_maze[row].append(cell.strip())
        row += 1
        new_list = []
        cell_maze.append(new_list)

    del cell_maze[len(cell_maze) - 1]
    file_object.close()

    return cell_maze


# This method prints the grid of strings, and can be used as a
# quick reminder what the grid currently looks like in text form
def print_maze_debug(maze):
    for row in maze:
        for col in row:
            print(col, end=' ')
        print("", end="\n")


# Set up grid objects
grid = create_maze(MAZE_TEXT_FILE)
# print_maze_debug(grid)  # For debugging
cell_width = width / len(grid[0])  # Set width based on screen size
cell_height = height / len(grid)  # Set height based on screen size

def create_obstacle(x,y):
  obstacle_turtle.hideturtle()
  obstacle_turtle.penup()
  obstacle_turtle.goto(x,y)
  obstacle_turtle.color("white")
  obstacle_turtle.fillcolor("white")
  obstacle_turtle.pendown()
  obstacle_turtle.begin_fill()
  for i in range(4):
    obstacle_turtle.forward(10)
    obstacle_turtle.right(90)
  obstacle_turtle.end_fill()

def create_monster(x,y):
  
  monster_turtle.hideturtle()
  monster_turtle.penup()
  monster_turtle.goto(x,y)
  monster_turtle.color("red")
  monster_turtle.fillcolor("red")
  monster_turtle.pendown()
  monster_turtle.begin_fill()
  monster_turtle.circle(8)
  monster_turtle.end_fill()

def create_treasure(x,y):
  treasure_turtle.hideturtle()
  treasure_turtle.penup()
  treasure_turtle.goto(x,y)
  treasure_turtle.pendown()
  treasure_turtle.color("yellow")
  treasure_turtle.fillcolor("yellow")
  treasure_turtle.begin_fill()
  for i in range (3):
    treasure_turtle.forward(20)
    treasure_turtle.left(120)
  treasure_turtle.end_fill()

def create_player(x,y):
  character_turtle.hideturtle()
  character_turtle.penup()
  character_turtle.goto(x,y)
  x_pos = x
  y_pos = y
  character_turtle.pendown()
  character_turtle.color("blue")
  character_turtle.fillcolor("blue")
  character_turtle.begin_fill()
  character_turtle.circle(10)
  character_turtle.end_fill()
  return x_pos, y_pos



#map creation:
x = -110
y= 110

"""
for row in grid:
  row = grid[i]
  for col in row:
    if col == BLOCK_STR:
      create_obstacle(x,y)
      obstacle = Obstacle(x, y,obstacle_turtle)
    elif col == MONSTER_STR:
      create_monster(x+5,y-10)
      monster = Monster(x,y,monster_turtle)
    elif col == TREASURE_STR:
      create_treasure(x-5,y-10)
      treasure = Treasure(x,y,treasure_turtle)
    elif col == PLAYER_STR:
      create_player(x+5,y-15)
      player = Player(x,y,character_turtle, ALIVE)
    x+=20
  y-=20
  x=-110
  i+=1
"""



#creating player object


obstacle_object = Cell(x,y,obstacle_turtle)

x_boundary_negative = float(-110)
x_boundary_positive = float(130)
y_boundary_negative = float(-110)
y_boundary_positive = float(110)
boundaries = [x_boundary_negative,x_boundary_positive,y_boundary_negative,y_boundary_positive]

#controls
def move_up():
  global player_pos
  character_turtle.penup()
  player_up_position = [player_pos[0],player_pos[1]+20]
  if ((player_up_position[1])) < boundaries[3]:
    character_turtle.clear()
    create_player(player_pos[0],player_pos[1]+20)
  player_pos = character_turtle.pos()
  print (player_up_position[1])
  
def move_down():
  global player_pos
  character_turtle.penup()
  player_down_position = [player_pos[0],player_pos[1]-20]
  if ((player_down_position[1])) > boundaries[2]:
    character_turtle.clear()
    create_player(player_pos[0],player_pos[1]-20)
  player_pos = character_turtle.pos()
  

def move_left():
  global player_pos
  character_turtle.penup()
  player_left_position = [player_pos[0]-20,player_pos[1]]
  if ((player_left_position[0])) > boundaries[0]:
    character_turtle.clear()
    create_player(player_pos[0]-20,player_pos[1])
  player_pos = character_turtle.pos()

def move_right():
  global player_pos
  character_turtle.penup()
  player_right_position = [player_pos[0]+20,player_pos[1]]
  if ((player_right_position[0]+20)) < boundaries[1]:
    character_turtle.clear()
    create_player(player_pos[0]+20,player_pos[1])
  player_pos = character_turtle.pos()

def move_monsters():
  pass

  
  
#game loop


x = -110
y= 110
player_position = []
obstacle_position_list = []
monster_count = 0
for row in grid:
  for col in row:
    if col == BLOCK_STR:
      create_obstacle(x,y)
      obstacle = Obstacle(x, y,obstacle_turtle)
      obstacle_pos = obstacle_turtle.pos()
      obstacle_position_list.append((obstacle_pos))
    elif col == MONSTER_STR:
      create_monster(x+5,y-10)
      monster = Monster(x,y,monster_turtle)
      monster_count+=1
    elif col == TREASURE_STR:
      create_treasure(x-5,y-10)
      treasure = Treasure(x,y,treasure_turtle)
    elif col == PLAYER_STR:
      create_player(x+5,y-15)
      player = Player(x,y,character_turtle, ALIVE)
      player_pos = character_turtle.pos()
    x+=20
  y-=20
  x=-110

f = 0
print (obstacle_position_list)
while PLAYER_STATE == 0:
  window.update()
  window.listen()
  window.onkeypress(move_up, "w")
  window.onkeypress(move_down, "s")
  window.onkeypress(move_left, "a")
  window.onkeypress(move_right, "d")


start_time = time.time()
while True:
    window.update()

    # Move the monsters
    if time.time() - start_time > MONSTER_SPEED_IN_SEC:
        move_monsters()
        start_time = time.time()

turtle.done()