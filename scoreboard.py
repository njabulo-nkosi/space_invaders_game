from turtle import Turtle

FONT = ("Courier", 18, "normal")


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("white")
        self.current_score = 0
        self.lives = 3
        self.goto(x=-270, y=270)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(arg=f"Score: {self.current_score}  Lives: {self.lives}", align="left", font=FONT)

    def increase_score(self):
        """Increase the score and update the display."""
        self.current_score += 1
        self.update_scoreboard()

    def decrease_lives(self):
        self.lives -= 1
        self.update_scoreboard()

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=("Courier", 18, "bold"))

    def you_win(self):
        self.goto(0, 0)
        self.write("YOU WIN!", align="center", font=("Courier", 18, "bold"))

    def out_of_bounds(self):
        self.goto(0, 0)
        self.write("Out of bounds! Game Over!", align="center", font=("Courier", 18, "bold"))
