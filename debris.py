import random
from turtle import Turtle

COLORS = ["white", "purple", "blue"]


class Debris:
    def __init__(self):
        """Initialize the debris objects."""
        self.debris_list = []
        self.create_debris()

    def create_debris(self):
        """Create a limited number of randomly spaced debris on the screen."""
        for _ in range(15):  # Create fewer debris pieces for cleaner gameplay
            debris = Turtle()
            debris.shape("square")
            debris.shapesize(stretch_wid=1, stretch_len=0.5)  # Small debris
            debris.color(random.choice(COLORS))
            debris.penup()
            x = random.randint(-200, 50)  # Confined to central region
            y = random.randint(-200, 200)
            debris.goto(x, y)
            self.debris_list.append(debris)

    def check_bullet_collision(self, bullets):
        """Check if any bullet collides with the debris."""
        debris_to_remove = []
        bullets_to_remove = []

        for debris in self.debris_list:  # Iterate directly over debris_list
            for bullet in bullets:
                if bullet.distance(debris) < 15:  # Adjust collision threshold
                    # Hide debris and bullet
                    debris.hideturtle()
                    bullet.hideturtle()

                    # Add to removal lists
                    debris_to_remove.append(debris)
                    bullets_to_remove.append(bullet)

        # Remove debris and bullets outside the loops
        for debris in debris_to_remove:
            if debris in self.debris_list:
                self.debris_list.remove(debris)
        for bullet in bullets_to_remove:
            if bullet in bullets:
                bullets.remove(bullet)

    # def check_bullet_collision(self, bullets):
    #     """Check if any bullet collides with the debris."""
    #     for debris in self.debris_list[:]:  # Safely iterate through the list
    #         for bullet in bullets[:]:
    #             if bullet.distance(debris) < 15:  # Adjust collision threshold
    #                 # Remove debris
    #                 debris.hideturtle()
    #                 self.debris_list.remove(debris)
    #                 # Remove bullet
    #                 bullet.hideturtle()
    #                 bullets.remove(bullet)
