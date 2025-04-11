from turtle import *
from _tkinter import TclError
import random
import time
import os


# Fenster einrichten
window = Screen()
window.setup(900, 700)
window.bgpic('./assets/bckgrnd.png')
window.title("Space Shooter")
window.tracer(0)

# Schiffklasse
class Ship(Turtle):
    def __init__(self):
        super().__init__()
        self.img = './assets/spaceship.gif'
        register_shape(self.img)
        self.shape(self.img)
        self.penup()
        self.setposition(0, -300)

    def moveLeft(self):
        x = self.xcor()
        if x > -400:
            self.setx(x - 20)

    def moveRight(self):
        x = self.xcor()
        if x < 400:
            self.setx(x + 20)

# Projektilklasse
class Bullet(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("red")
        self.penup()
        self.hideturtle()
        self.speed(0)
        self.active = False
        self.shapesize(stretch_wid=0.6, stretch_len=0.1)

    def fire(self, x, y):
        if not self.active:
            self.setposition(x, y + 10)
            self.showturtle()
            self.active = True

    def move(self):
        if self.active:
            self.sety(self.ycor() + 20)
            if self.ycor() > 350:
                self.hideturtle()
                self.active = False

# Gegnerklasse
class Enemy(Turtle):
    def __init__(self):
        super().__init__()
        self.img = './assets/enemy.gif'
        register_shape(self.img)
        self.shape(self.img)
        self.penup()
        self.speed(0)
        self.setposition(random.randint(-400, 400), 350)
        self.dy = 1.0

    def move(self):
        self.sety(self.ycor() - self.dy)
        if self.ycor() < -350:
            self.reset_position()

    def reset_position(self):
        self.setposition(random.randint(-400, 400), 350)
        self.dy = 1.0

# Explosion anzeigen
def show_explosion(x, y):
    explosion = Turtle()
    explosion_img = './assets/explosion.gif'
    register_shape(explosion_img)
    explosion.shape(explosion_img)
    explosion.penup()
    explosion.setposition(x, y)
    explosion.showturtle()
    window.update()
    time.sleep(0.5)
    explosion.hideturtle()
    explosion.clear()

# Spielobjekte
rocket = Ship()
bullet = Bullet()
enemy = Enemy()

# Steuerung
window.listen()
window.onkeypress(rocket.moveLeft, "Left")
window.onkeypress(rocket.moveRight, "Right")
window.onkeypress(lambda: bullet.fire(rocket.xcor(), rocket.ycor()), "space")

# Game Loop
def game_loop():
    while True:
        try:
            window.update()
            time.sleep(0.015)

            bullet.move()
            enemy.move()

            # Treffer Gegner
            if bullet.active and bullet.distance(enemy) < 40:
                show_explosion(enemy.xcor(), enemy.ycor())
                bullet.hideturtle()
                bullet.active = False
                enemy.reset_position()

            # Gegner trifft Schiff
            if rocket.distance(enemy) < 40:
                show_explosion(rocket.xcor(), rocket.ycor())
                print("Game Over!")
                break

        except TclError:
            # Wenn Fenster geschlossen wird, bricht ab
            print("Fenster wurde geschlossen.")
            break

# Spiel starten
game_loop()

# Fenster offen halten
window.mainloop()
