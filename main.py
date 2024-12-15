from turtle import Screen
from player import Player
from enemy import Enemy
from scoreboard import Scoreboard
from debris import Debris
import time

# Screen Setup
screen = Screen()
screen.title("Space Invader")
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.tracer(0)

# Game Objects
player = Player()
enemy = Enemy()
scoreboard = Scoreboard()
debris = Debris()

# Event Listeners
screen.listen()
screen.onkey(player.shoot, "space")
screen.onkey(player.forwards, "Right")
screen.onkey(player.backwards, "Left")
screen.onkey(player.downwards, "Down")
screen.onkey(player.upwards, "Up")

# Game State Variables
game_on = True
boss_active = False
boss_shoot_timer = 0

# Game Loop
while game_on:
    time.sleep(0.1)
    screen.update()

    # Move player bullets
    player.move_bullets()
    enemy.attack()  # Normal enemies move and shoot

    debris.check_bullet_collision(player.bullets)
    debris.check_bullet_collision(enemy.enemy_bullets)

    # Boss-specific logic
    if boss_active:
        # Boss vertical movement
        enemy.boss.sety(enemy.boss.ycor() + (15 if enemy.direction == 'up' else -15))

        if enemy.horizontal_direction == 'left':
            enemy.boss.setx(enemy.boss.xcor() - 5)  # Move left
            if enemy.boss.xcor() <= -20:  # Limit to -20
                enemy.horizontal_direction = 'right'  # Switch to moving right
        else:
            enemy.boss.setx(enemy.boss.xcor() + 5)  # Move right
            if enemy.boss.xcor() >= 200:  # Right boundary (adjust as needed)
                enemy.horizontal_direction = 'left'  # Switch to moving left

        if enemy.steps >= enemy.maximum_steps:  # Change direction at max steps
            enemy.direction = 'up' if enemy.direction == 'down' else 'down'
            enemy.steps = 0
        else:
            enemy.steps += 1

        # Boss shooting at intervals
        boss_shoot_timer += 1
        if boss_shoot_timer % 5 == 0:  # Adjust shooting frequency
            enemy.boss_shoot()

        # Check if boss hits the player
        if enemy.check_boss_collision(player):
            scoreboard.decrease_lives()
            boss_active = False  # Boss stops when hitting the player

        # Check if player's bullets hit the boss
        for bullet in player.bullets:
            if bullet.distance(enemy.boss) < 20:
                bullet.hideturtle()
                player.bullets.remove(bullet)
                enemy.boss.hideturtle()
                boss_active = False
                game_on = False
                scoreboard.you_win()

    # Check for player-bullet collisions with enemies
    for bullet in player.bullets:
        for single_enemy in enemy.enemies:
            if bullet.distance(single_enemy) < 15:  # Adjust collision distance as needed
                bullet.hideturtle()
                single_enemy.hideturtle()
                player.bullets.remove(bullet)
                enemy.enemies.remove(single_enemy)
                scoreboard.increase_score()

    # Activate boss when score threshold is met
    if not boss_active and scoreboard.current_score > 0 and scoreboard.current_score % 5 == 0:
        enemy.create_boss_enemy()
        boss_active = True

    # Check for enemy bullets hitting player
    if enemy.check_bullet_collision_with_player(player, scoreboard):
        pass

    # Check if player is out of lives
    if scoreboard.lives == 0:
        scoreboard.game_over()
        game_on = False

    # Out-of-bounds game over condition
    if player.xcor() < -290 or player.xcor() > 290 or player.ycor() < -290 or player.ycor() > 290:
        scoreboard.out_of_bounds()
        game_on = False

# Exit game
screen.exitonclick()
