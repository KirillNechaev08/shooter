
from pygame import *
from random import randint
import time as tm

win_width = 700 
win_height = 500 
game = True
score_lost=0
score_kill=0
finish=False
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed,width=65,height=65):
        super().__init__()
  
        self.image = transform.scale(image.load(player_image), (width,height))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_a] :
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
        if self.rect.x >=700:
            self.rect.x =0
        if self.rect.x <-65:
            self.rect.x =695
    def fire(self):
        bullet= Bullet("bullet.png", self.rect.x+32, self.rect.y+32, 7, width=15, height=15)
        bullets.add(bullet)
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()  


class Enemy(GameSprite):
    def update(self):
        global score_lost
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            score_lost +=1
            self.rect.y = -65
            self.rect.x = randint(1, win_width-65)
            self.speed = randint(1, 2)

hero = Player("rocket.png", 100, 400, 5)
enemy1 = Enemy("ufo.png", randint (1, win_width-65),-65 , randint(1, 2))
enemy2 = Enemy("ufo.png", randint (1, win_width-65),-65 , randint(1, 2))
enemy3 = Enemy("ufo.png", randint (1, win_width-65),-65 , randint(1, 2))
enemy4 = Enemy("ufo.png", randint (1, win_width-65),-65 , randint(1, 2))
enemy5 = Enemy("ufo.png", randint (1, win_width-65),-65 , randint(1, 2))
enemies=sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)
enemies.add(enemy3)
enemies.add(enemy4)
enemies.add(enemy5)

bullets=sprite.Group()

window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
ogon=mixer.Sound("fire.ogg")

font.init()
font1 = font.Font(None, 50)
win = font1.render("ты выиграл", True, (0,255,0))
lose = font1.render("ты проиграл", True, (255,0,0))
FPS = 60
clock=time.Clock()

background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))


num_fire=0
rel_time=False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key==K_SPACE and rel_time ==False:
                hero.fire()
                num_fire+=1
                ogon.play()
    if not finish:
        score = font1.render("Счёт: "+ str(score_kill), True, (255,255,255))
        lost = font1.render("Пропущено: "+ str(score_lost), True, (255,255,255))
        
        window.blit(background, (0,0))
        window.blit(score, (20,20))
        window.blit(lost, (20,70))
        hero.move()
        hero.reset()
        bullets.draw(window)
        bullets.update()
        enemies.draw(window)
        enemies.update()


        sprite_list = sprite.groupcollide(enemies, bullets, True, True)
        for c in sprite_list:
            score_kill +=1
            enemy6 = Enemy("ufo.png", randint (1, win_width-65),-65 , randint(1, 2))
            enemies.add(enemy6)


        if score_kill >= 10:
            window.blit(win, (win_width/2-50, win_height/2-50))
            finish=True


        if score_lost >= 5 or sprite.spritecollide(hero, enemies, False):
            window.blit(lose, (win_width/2-50, win_height/2-50)) 
            finish=True
        
        if num_fire >= 5 and rel_time == False:
            rel_time=True
            start = tm.time()

        if rel_time == True:
            end =tm.time()
            if end - start>=1:
                rel_time = False
                num_fire=0
            else:
                rel= font1.render("перезарядка", True,(255,0,0))
                window.blit(rel,(340,450))






    display.update()
    clock.tick(FPS)