from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
MOVE_INCREMENT = 2
ENEMY_SPAWN_PROBABILITY = 5
STARTING_POSITIONS = [
    (100, 100),
    (150, 50),
    (200, 0),
    (150, -50),
    (100, -100),
    (250, 150),
    (250, -150),
    (280, 100),
    (280, -100),
    (200, 50),
]


class Enemy(Turtle):
    def __init__(self):
        super().__init__()
        self.enemies = []
        self.enemy_bullets = []
        self.direction = 'down'
        self.steps = 0
        self.maximum_steps = 20
        self.maximum_enemies = 15
        self.boss = None
        self.boss_health = 10
        self.boss_direction = 'down'
        self.horizontal_direction = 'left'

        for position in STARTING_POSITIONS:
            self.create_enemies(position)

    def create_enemies(self, position):
        """Create normal enemies."""
        if len(self.enemies) < self.maximum_enemies:
            new_enemy = Turtle(shape="turtle")
            new_enemy.penup()
            new_enemy.color('green')
            new_enemy.setheading(180)
            new_enemy.goto(position)
            self.enemies.append(new_enemy)

    def attack(self):
        """Move normal enemies and allow them to shoot."""
        move_amount = MOVE_INCREMENT if self.direction == 'down' else -MOVE_INCREMENT

        for enemy in self.enemies:
            new_y = enemy.ycor() + move_amount
            enemy.sety(new_y)

            # Randomly decide if the enemy should shoot
            if random.randint(1, 200) <= 5:
                self.shoot_bullet(enemy)

        self.steps += 1
        if self.steps >= self.maximum_steps:
            self.steps = 0
            self.direction = 'up' if self.direction == 'down' else 'down'

        # Move bullets fired by enemies
        self.move_bullets()

    def shoot_bullet(self, enemy):
        """Enemy shoots a bullet."""
        bullet = Turtle(shape='square')
        bullet.penup()
        bullet.color('orange')
        bullet.shapesize(stretch_wid=0.2, stretch_len=0.5)
        bullet.goto(enemy.xcor(), enemy.ycor())
        self.enemy_bullets.append(bullet)

    def move_bullets(self):
        """Move bullets fired by enemies."""
        for bullet in self.enemy_bullets:
            bullet.setheading(180)
            bullet.forward(10)

            if bullet.xcor() < -300:
                bullet.hideturtle()
                self.enemy_bullets.remove(bullet)

    def create_boss_enemy(self):
        """Create the boss enemy."""
        self.clear_normal_enemies()  # Remove normal enemies
        self.boss = Turtle(shape="turtle")
        self.boss.penup()
        self.boss.color(random.choice(COLORS))
        self.boss.setheading(180)
        self.boss.shapesize(stretch_wid=5, stretch_len=5)
        self.boss.goto(250, 0)  # Place the boss at the center of the screen

    def clear_normal_enemies(self):
        """Clear all normal enemies from the screen."""
        for enemy in self.enemies:
            enemy.hideturtle()
        self.enemies = []

    def move_boss(self):
        """Move the boss enemy vertically up and down."""
        if self.boss:
            move_amount = MOVE_INCREMENT if self.boss_direction == 'down' else -MOVE_INCREMENT
            new_y = self.boss.ycor() + move_amount
            self.boss.sety(new_y)

            # Change direction when the boss reaches the screen bounds
            if self.boss.ycor() <= -300:   # previously -250
                self.boss_direction = 'up'
            elif self.boss.ycor() >= 300:
                self.boss_direction = 'down'

    def boss_shoot(self):
        """Boss enemy fires bullets."""
        if self.boss:
            for _ in range(3):   # can be made to 6
                bullet = Turtle(shape="square")
                bullet.shapesize(stretch_len=1, stretch_wid=0.5)
                bullet.color("red")
                bullet.penup()
                bullet.goto(self.boss.xcor(), self.boss.ycor() - 20)
                bullet.setheading(270)  # Bullets move downward
                self.enemy_bullets.append(bullet)

    def check_boss_collision(self, player):
        """Check if the boss is hit by the player's bullets."""
        if self.boss:  # Ensure the boss exists
            for bullet in player.bullets[:]:  # Iterate over a copy to safely remove items
                if bullet.distance(self.boss) < 50:  # Adjust for boss size
                    bullet.hideturtle()
                    player.bullets.remove(bullet)
                    self.boss_health -= 1
                    print(f"Boss hit! Remaining health: {self.boss_health}")

            if self.boss_health <= 0:
                self.boss.hideturtle()
                self.boss = None
                print("Boss defeated!")
                return True  # Indicates boss was defeated

        return False

    def check_bullet_collision_with_player(self, player, scoreboard):
        """Check if enemy or boss bullets hit the player."""
        for bullet in self.enemy_bullets:
            if bullet.distance(player) < 15:  # Collision radius for bullets
                bullet.hideturtle()
                self.enemy_bullets.remove(bullet)
                if bullet.color() == ("red",):  # Boss bullet
                    scoreboard.lives = 0  # Immediate elimination
                else:
                    scoreboard.decrease_lives()
