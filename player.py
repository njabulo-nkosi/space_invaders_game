import time
from turtle import Turtle

MOVE_INCREMENT = 10
SHOOT_COOLDOWN = 2   # increase (2 seconds) for longer delay between shots


class Player(Turtle):

    def __init__(self):
        super().__init__()
        self.player = Turtle()
        self.shapesize(stretch_wid=1.5, stretch_len=1.5)
        self.penup()
        self.color("white")
        self.goto(x=-280, y=0)
        self.bullets = []
        self.last_time_shot = 0
        self.lives = 3

    def shoot(self):
        current_time = time.time()
        if current_time - self.last_time_shot >= SHOOT_COOLDOWN:
            bullet = Turtle()
            bullet.shape("square")
            bullet.shapesize(stretch_len=0.75, stretch_wid=0.25)
            bullet.color("yellow")
            bullet.penup()
            bullet.speed("fastest")
            bullet.setheading(self.heading())
            bullet.goto(self.xcor(), self.ycor())
            self.bullets.append(bullet)
            self.last_time_shot = current_time

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.forward(MOVE_INCREMENT)

    def forwards(self):
        self.forward(MOVE_INCREMENT)

    def backwards(self):
        self.backward(MOVE_INCREMENT)

    def upwards(self):
        self.goto(x=self.xcor(), y=self.ycor() + MOVE_INCREMENT)

    def downwards(self):
        self.goto(x=self.xcor(), y=self.ycor() - MOVE_INCREMENT)
