#Create your own shooter

from pygame import *
from random import randint
from time import time as t 

class GameSprite(sprite.Sprite):
    # class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # We call the class constructor (Sprite):
        sprite.Sprite.__init__(self)

        # each sprite must store an image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # each sprite must store the rect property it is inscribed in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

   # method that draws the character in the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x >= 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x <= win_width - self.rect.width:
            self.rect.x += self.speed

    def fire(self):
        x = self.rect.centerx
        y = self.rect.top
        bullet = Bullet("laser.png", x, y, 20, 50, 7)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed

        if self.rect.y > win_height:
           self.rect.x = randint(0, win_width - self.rect.width)
           self.rect.y = -1 * self.rect.height
           if self in monsters:
               lost += 1


class Boss(Enemy):
    def update(self):
        def spawn(self):
            Enemy1 = ("ufo.png", 180, 20, 2)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
           self.kill()

win_width = 800
win_height = 500

astroids = sprite.Group()
for i in range(3):
    astroids.add(Enemy("asteroid.png", randint(0, win_width - 65), randint(-50, 0), 65, 65, 5))

monsters = sprite.Group()
asteroids = sprite.Group()

window = display.set_mode((win_width, win_height))
display.set_caption("StarWars")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load("space.ogg")
#mixer.music.play()

font.init()
style = font.SysFont("Arial", 36)


bullets = sprite.Group()

ship = Player("rocket.png", 350, 430, 80, 90, 7)
boss = Boss("boss.png", 330, 50, 190, 200, 2)
for i in range(5):
   monsters.add(Enemy("ufo.png", randint(0, win_width - 65), randint(-50, 0), 65, 65, 1))
for i in range(3):
   asteroids.add(Enemy("asteroid.png", randint(0, win_width - 65), randint(-50, 0), 65, 65, 0.3))

bullet_count = 5
finish = False
lost = 0
score = 0
game = True
clock = time.Clock()
FPS = 60
powerups = []
while game:
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                if bullet_count > 0:
                    ship.fire()
                    bullet_count -= 1
                else:
                    is_rel = True
                    start_time = t()

        if e.type == KEYDOWN and e.key == K_SPACE:
            if bullet_count > 0:
                ship.fire()
                bullet_count -= 1
            else:
                is_rel = True
                start_time = t()


        if not finish:
            # refresh background
            window.blit(background, (0, 0))

            #Statistics
            font = style.render("Missed: " + str(lost), True, (255, 255, 255))
            font2 = style.render("Score: " + str(score), True, (255, 255, 255))
            # producing sprite movements
            ship.update()
            monsters.update()
            astroids.update()
            bullets.update()
    
            #Check Collision

            window.blit(background, (0, 0))
            text_lose = style.render("Missed: " + str(lost), True, (255, 255, 255))
            text_score = style.render("Score: " + str(score), True, (255, 255, 255))
            ship.update()
            ship.reset()
            bullets.update()
            boss.update()
            boss.reset()
            asteroids.update()
            monsters.update()
            monsters_lost = sprite.groupcollide(monsters, bullets, True, True)
            for m in monsters_lost:
                score += 1
                monsters.add(Enemy("ufo.png", randint(0, win_width - 65), randint(-50, 0), 65, 65, 1))

            #Check Win
            if score >= 10:
                pass

            #Check Lose
            if len(sprite.spritecollide(ship, monsters, False)) > 0 or lost >= 3:
                pass

            #Powerup
            if randint(1, 120) == 1:
                powerups.append(GameSprite("bolt.png", randint(0, win_width - 65), randint(-50, 0), 20, 20, 7))

            for powerup in powerups:
                powerup.rect.y += powerup.speed
                powerup.reset()
                if ship.rect.colliderect(powerup.rect):
                    powerups.remove(powerup)
                    for i in range(18):
                        bullet = Bullet("laser.png", i * 50, win_height, 20, 50, 5)
                        bullets.add(bullet)

                if is_rel and t() - start_time >= 3:
                    is_rel = False
                    bullet_count = 5


            #Enemy1.update()
            #Enemy1.reset()
            #Enemy2.update()
            #Enemy2.reset()
            #Enemy3.update()
            #Enemy3.reset()
            asteroids.draw(window)
            bullets.draw(window)
            monsters.draw(window)
            window.blit(text_score, (10, 20))
            window.blit(text_lose, (10, 54))
            display.update()
            clock.tick(FPS)
            time.delay(50)