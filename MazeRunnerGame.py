#Maze Runner Project
# @Author -> Dominic Domingo

import turtle
import functools
import random
import time

#turtle objects
obstacle_turtle = turtle.Turtle()
character_turtle = turtle.Turtle()
treasure_turtle= turtle.Turtle()
text_turtle = turtle.Turtle()
text_turtle.hideturtle()

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
MONSTER_SPEED_IN_SEC = 0.5  # in seconds
row_pos = 0
col_pos = 0

# Text feedback for winning the game, or losing the game
game_end_list = []
game_win_list = []


# Classes
# --------------------------------------------------------
# Monster class to store coordinates, direction, and turtle object
class Monster:
    def __init__(self, x, y, turtle_obj,direction):
        self.x = x
        self.y = y
        self.turtle_obj = turtle_obj
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
    obstacle_turtle.forward(cell_width)
    obstacle_turtle.right(90)
    obstacle_turtle.forward(cell_height)
    obstacle_turtle.right(90)
  obstacle_turtle.end_fill()

def create_monster(x,y,monster):
  
  monster.turtle_obj.hideturtle()
  monster.turtle_obj.penup()
  monster.turtle_obj.goto(x,y)
  monster.turtle_obj.color("red")
  monster.turtle_obj.fillcolor("red")
  monster.turtle_obj.pendown()
  monster.turtle_obj.begin_fill()
  monster.turtle_obj.circle(cell_height/2)
  monster.turtle_obj.end_fill()

def create_treasure(x,y):
  treasure_turtle.hideturtle()
  treasure_turtle.penup()
  treasure_turtle.goto(x,y)
  treasure_turtle.pendown()
  treasure_turtle.color("yellow")
  treasure_turtle.fillcolor("yellow")
  treasure_turtle.begin_fill()
  for i in range (3):
    treasure_turtle.forward(cell_width)
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
  character_turtle.circle(cell_height/2)
  character_turtle.end_fill()
  return x_pos, y_pos



#map creation:
x = -110
y= 110

x = cell_width*(len(grid[0])/2)
y= cell_height*(len(grid)/2)


x_boundary_negative = float(0-x)
x_boundary_positive = float(0+x)
y_boundary_negative = float(0-y)
y_boundary_positive = float(0+y)
boundaries = [x_boundary_negative,x_boundary_positive,y_boundary_negative,y_boundary_positive]

#controls
def move_up():
  global player_pos
  character_turtle.penup()
  player_up_position = [player_pos[0],player_pos[1]+cell_height]
  player_up_position = round(player_up_position[0]),round(player_up_position[1])
  if ((player_up_position[1])) <= boundaries[3]:
    if (player_up_position) not in obstacle_position_list:
      character_turtle.clear()
      create_player(player_pos[0],player_pos[1]+cell_height)
  player_pos = character_turtle.pos()

  
def move_down():
  global player_pos
  character_turtle.penup()
  player_down_position = [player_pos[0],player_pos[1]-cell_height]
  player_down_position = round(player_down_position[0]),round(player_down_position[1])
  if ((player_down_position[1])) >= boundaries[2]:
    if (player_down_position) not in obstacle_position_list:
      character_turtle.clear()
      create_player(player_pos[0],player_pos[1]-cell_height)
  player_pos = character_turtle.pos()
  

def move_left():
  global player_pos
  character_turtle.penup()
  player_left_position = [player_pos[0]-cell_width,player_pos[1]]
  player_left_position = round(player_left_position[0]),round(player_left_position[1])
  if ((player_left_position[0])) >= boundaries[0]:
    if (player_left_position) not in obstacle_position_list:
      character_turtle.clear()
      create_player(player_pos[0]-cell_width,player_pos[1])
  player_pos = character_turtle.pos()

def move_right():
  global player_pos
  character_turtle.penup()
  player_right_position = [player_pos[0]+cell_width,player_pos[1]]
  player_right_position = round(player_right_position[0]),round(player_right_position[1])
  if ((player_right_position[0]+cell_width)) <= boundaries[1]+cell_width:
    if (player_right_position) not in obstacle_position_list:
      character_turtle.clear()
      create_player(player_pos[0]+cell_width,player_pos[1])
  player_pos = character_turtle.pos()

def win_text():
  text_turtle.goto(0, 0)
  text_turtle.color("white")
  random_win_text_list = ["You won!", "GG, you won!", "Too easy :)", "Well played!", "Congrats, you reached the treasure!", "Good Game!"]
  victory_text = random.choice(random_win_text_list)
  text_turtle.write(victory_text, align="center", font = ("Roboto",25, "bold"))

def loss_text():
  text_turtle.goto(0, 0)
  text_turtle.color("white")
  random_loss_text_list = ["You lost!", "Unlucky, GG go next", "Try timing your movements!", "You know you're supposed to avoid the monsters, right?", "Try again!"]
  loss_text = random.choice(random_loss_text_list)
  text_turtle.write(loss_text, align="center", font = ("Roboto",25, "bold"))


def move_monsters(monster):
 
  def monster_up():
    monster.turtle_obj.clear()
    create_monster(monster.x, monster.y+cell_height, monster)
    monster.x = (monster.turtle_obj.pos()[0])
    monster.y = (monster.turtle_obj.pos()[1])

  def monster_down():
    monster.turtle_obj.clear()
    create_monster(monster.x, monster.y-cell_height, monster)
    monster.x = (monster.turtle_obj.pos()[0])
    monster.y = (monster.turtle_obj.pos()[1])

  def monster_left():
    monster.turtle_obj.clear()
    create_monster(monster.x-cell_width, monster.y, monster)
    monster.x = (monster.turtle_obj.pos()[0])
    monster.y = (monster.turtle_obj.pos()[1])

  def monster_right():
    monster.turtle_obj.clear()
    create_monster(monster.x+cell_width, monster.y, monster)
    monster.x = (monster.turtle_obj.pos()[0])
    monster.y = (monster.turtle_obj.pos()[1])

#Monster movement logic, checking if it is within boundaries or next to an obstacle
  random_direction = []
  monster_pos = monster.turtle_obj.pos()
  monster.x = monster_pos[0]
  monster.y = monster_pos[1]
  monster_up_position = (monster.x, monster.y+cell_height)
  monster_up_position = round(monster_up_position[0]),round(monster_up_position[1])
  monster_right_position = (monster.x+cell_width, monster.y)
  monster_right_position = round(monster_right_position[0]), round(monster_right_position[1])
  monster_left_position = (monster.x-cell_width, monster.y)
  monster_left_position = round(monster_left_position[0]), round(monster_left_position[1])
  monster_down_position = (monster.x, monster.y-cell_height)
  monster_down_position = round(monster_down_position[0]),round(monster_down_position[1])
  if monster_left_position[0] >= x_boundary_negative:
    if monster_left_position not in obstacle_position_list:
      random_direction.append(0)
  if monster_up_position[1] <= y_boundary_positive-cell_height:
    if monster_up_position not in obstacle_position_list:
      random_direction.append(1)
  if monster_right_position[0] <= x_boundary_positive:
    if monster_right_position not in obstacle_position_list:
      random_direction.append(2)
  if monster_down_position[1] >= y_boundary_negative:
    if monster_down_position not in obstacle_position_list:
      random_direction.append(3)
#choosing random direction for monster to move
  Monster.direction = random.choice(random_direction)
  if Monster.direction == 0:
    monster_left()
  elif Monster.direction == 1:
    monster_up()
  elif Monster.direction == 2:
    monster_right()
  elif Monster.direction == 3:
    monster_down()
    


#Setting starting position of grid to fit dimensions of screen

x1 = 0
y1 = 0
x = -cell_width*(len(grid[0])/2)
original_x = x
y= cell_height*(len(grid)/2)

#Use lists to track positions of each object
list_of_monsters = []
player_position = []
obstacle_position_list = []
monster_position_list = []

#Setting up map by using grid from create_maze function
#Iterate through each element of the grid, checking if there is a string indicating the position of an object
#Create object upon finding string

for row in grid:
  for col in row:
    if col == BLOCK_STR:
      create_obstacle(x,y)
      obstacle_pos = (x,y)
      obstacle_pos = obstacle_pos[0]+cell_width/2,obstacle_pos[1]-cell_height
      obstacle_pos = round(obstacle_pos[0]),round(obstacle_pos[1])
      obstacle_position_list.append((obstacle_pos))
    elif col == MONSTER_STR:
      monster_turtle = turtle.Turtle()
      monster = Monster(round(x+cell_width/2),round(y-cell_height),monster_turtle,direction=UP)
      create_monster(x+cell_width/2,y-cell_height,monster)
      list_of_monsters.append(monster)
    elif col == TREASURE_STR:
      create_treasure(x,y-cell_height)
      treasure_pos = (x+cell_width/2, y-cell_height)
      treasure_pos = round(treasure_pos[0]), round(treasure_pos[1])
    elif col == PLAYER_STR:
      create_player(x+cell_width/2,y-cell_height)
      player_pos = character_turtle.pos()
    x += cell_width
    x1 += 1
  y-= cell_height
  y1-=1
  x= original_x


#Game Loop
# While player is alive,listen for keypresses and perform movement functions on keypress
alive = True
start_time = time.time()
window.listen()
while alive is True:
  window.update()
  window.onkeypress(move_up, "w")
  window.onkeypress(move_down, "s")
  window.onkeypress(move_left, "a")
  window.onkeypress(move_right, "d")
  character_pos = character_turtle.pos() 
  character_pos = round(character_pos[0]),round(character_pos[1])
  if character_pos in monster_position_list:
        window.clear()
        window.bgcolor("black")
        loss_text()
        break
  if character_pos == treasure_pos:
        window.clear()
        window.bgcolor("black")
        win_text()
        break
  
  i = 0
  if time.time() - start_time > MONSTER_SPEED_IN_SEC:
    monster_position_list = []
    for ele in list_of_monsters:
      move_monsters(list_of_monsters[i])
      monsters_pos = list_of_monsters[i].turtle_obj.pos() 
      monsters_pos = monsters_pos [0], monsters_pos[1]
      monsters_pos = round(monsters_pos[0]),round(monsters_pos[1])
      monster_position_list.append(monsters_pos)
      i+=1
      start_time = time.time()
while PLAYER_STATE is DEAD:
  print("dead")
            
turtle.done()