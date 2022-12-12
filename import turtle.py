import turtle

object = turtle.Turtle()

object.color("red")
object.speed(0)
object.circle(8)

def up():
  object.setheading(90)
  object.forward(100)

def down():
  object.setheading(270)
  object.forward(100)

def left():
  object.setheading(180)
  object.forward(100)

def right():
  object.setheading(0)
  object.forward(100)