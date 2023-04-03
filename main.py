import pygame, sys
import random
import time

pygame.init()
pygame.mixer.init()
pygame.font.init()
#print(pygame.font.get_fonts())

pygame.mixer.music.load("img/Music/l39201toile-d39afrique-18_456256703.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)



money = 0
width = 1000
height = 700
FPS = 30
KO = 0
window = pygame.display.set_mode((width, height))
screen = pygame.Surface((width, height))


RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

class Menu:
    def __init__(self, items=[400, 350, u'Item', (250, 250, 30), (250, 30, 250)]):
        self.item = items



    def render(self, poverhnost, font, num_punkt):
        for i in self.item:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

    def menu(self):
        done = True
        font_menu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        item = 0
        while done:
            screen.blit(first, first_rect)
            mp = pygame.mouse.get_pos()
            for i in self.item:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    item = i[5]
            self.render(screen, font_menu, item)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if item > 0:
                            item -= 1
                    if e.key == pygame.K_DOWN:
                        if item < len(self.item) - 1:
                            item += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if item == 0:
                        main_player.hp = main_player.max_hp
                        done = False
                    elif item == 1:
                        exit()
            window.blit(first, first_rect)
            window.blit(screen, (0, 30))
            pygame.display.flip()

class Player(pygame.sprite.Sprite):
    def __init__(self,img):
        super(Player, self).__init__()
        self.image = pygame.transform.scale(img,(200,250))
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.centery = height // 2
        self.speed = 10
        self.hp = 100
        self.max_hp = 100
        # self.rect.top -- верхня точка
        # self.rect.botton -- нижня точка
        # self.rect.left -- крайня ліва точка
        # self.rect.right -- крайня права точка

    def update(self):
        if KO == 30:
            img = player_img_KOS
            self.image = pygame.transform.scale(img,(180,180))
            self.hp = 200
            self.max_hp = 200
            if KO == 100:
                img = player_img_leader
                self.image = pygame.transform.scale(img, (100, 100))
                self.speed = 15
                self.hp = 1000
                self.max_hp = 1000

        #self.rect.colliderect() # -- перевіряє чи 1 об'єкт перетнувся із 1 об'єктом
        #self.rect.collidepoint() # перевіряє чи точка знаходить в середині об'єкту
        keytstate = pygame.key.get_pressed()
        if keytstate[pygame.K_a]:
            self.rect.x -= self.speed
        if keytstate[pygame.K_d]:
            self.rect.x += self.speed
        if keytstate[pygame.K_w]:
            self.rect.y -= self.speed
        if keytstate[pygame.K_s]:
            self.rect.y += self.speed
        if keytstate[pygame.K_m]:
            game = Menu(choose)
            game.menu()

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height

    def shoot(self,bullet_img):
        piy = pygame.mixer.Sound("img/Sounds/Shot 1.0.mp3")
        piy.set_volume(0.2)
        b = Bullet(x = self.rect.centerx, y = self.rect.top, img = bullet_img)
        piy.play()
        all_sprites.add(b)
        bullets.add(b)


class EnemyPlane(pygame.sprite.Sprite):
    def __init__(self,img):
        super(EnemyPlane, self).__init__()
        self.image = pygame.transform.scale(img, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0+self.rect.w// 2,600-self.rect.w // 2)
        self.rect.centery = random.randint(-100,-50)
        #self.speed_mnoj = 1.0
        self.speedx = random.randint(-3,3)
        self.speedy = random.randint(2,4)

    def update(self):
        if KO >= 30:
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(4, 8)
            if KO >= 100:
                self.speedx = random.randint(-3, 3)
                self.speedy = random.randint(10, 30)
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > height or self.rect.left > width or self.rect.right < 0 :
            #self.speed_mnoj += 0.2
            out = pygame.mixer.Sound("img/Sounds/bideen.mp3")
            #out.play()
            self.rect.centerx = random.randint(0 + self.rect.w // 2, 600 - self.rect.w // 2)
            self.rect.centery = random.randint(-100, -50)
            self.speedx = random.randint(-5, 5)#* self.speed_mnoj
            self.speedy = random.randint(3, 8)#* self.speed_mnoj


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        super(Bullet, self).__init__()
        self.image = img
        self.image = pygame.transform.scale(img, (50, 50))
        self.speed_y = 10
        self.speed_x = random.randint(-3,3)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        if KO == 100:
            self.speed_y = 15


        self.rect.y -= self.speed_y
        self.rect.x -= self.speed_x
        if self.rect.bottom < 0:
            self.kill()

player_img1 = pygame.image.load("img/abrams2.png")
player_img_KOS = pygame.image.load("img/lopard2.png")
enemy_img1 = pygame.image.load("img/samolet-removebg-preview.png")
player_img_leader= pygame.image.load("img/Enemies/ShipDestroyerHull.png")
laser_img = pygame.image.load("img/raketa2.png")
first = pygame.image.load("img/backgrounds/Zastavka2.0.png")
first = pygame.transform.scale(first, (width,height))
first_rect = first.get_rect()
background = pygame.image.load("img/desert_2.png")
background = pygame.transform.scale(background, (width,height))
background_rect = background.get_rect()
enemy_imgs = [enemy_img1]

main_player = Player(player_img1)
screan = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
enemies =  pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(main_player)


choose = [(400, 300, u'PLAY GAME', (0, 0, 0), (0, 200, 30), 0),
          (450, 340, u'EXIT', (0, 0, 0), (0, 200, 30), 1)]
game = Menu(choose)
game.menu()



class Button():
    def __init__(self, x, y, width, height, onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': GREEN,
            'hover': RED,
            'pressed': BLUE,
        }

def draw_hp(surface, value, max_val, x, y): # value - це те що ми малюємо -- hp
    strip_lenght = 100
    strip_height = 10

    if value <= 30:
        color = RED
    elif value <= 50:
        color = (255, 165, 0)
    elif value > 70:
        color = GREEN
    else:
        color = (255, 255, 0)

    screen.fill((50, 50, 50))
    fill_hp = (value / max_val) * strip_lenght
    back_rect = pygame.Rect(x, y, strip_lenght, strip_height) # задній прямокутний
    front_rect = pygame.Rect(x, y, fill_hp, strip_height) # передній прямокутник
    pygame.draw.rect(surface, color, back_rect, 2)
    pygame.draw.rect(surface, color, front_rect)


def draw_text(surface, size, x, y, text):
    font = pygame.font.Font("img/Fonts/arial.ttf",size)
    text_surface = font.render(text,True,RED)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_surface,text_rect)


for i in range(10):
    m = EnemyPlane(random.choice(enemy_imgs))
    all_sprites.add(m)
    enemies.add(m)


run = True
while run:
    all_sprites.update()
    events = pygame.event.get() # events - список подій
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #main_player.rect.collidepoint()
                main_player.shoot(laser_img)


    hits = pygame.sprite.spritecollide(main_player,enemies,True)
    if hits: # якшо відбулась колізія
        for sprt in hits:
            hitds = pygame.mixer.Sound("img/Sounds/бум.mp3")
            money -= 5
            hitds.set_volume(0.4)
            hitds.play()
            print(sprt.speedx, sprt.speedy)
            main_player.hp -= abs(sprt.speedx) + abs(sprt.speedy)
            m = EnemyPlane(random.choice(enemy_imgs))
            all_sprites.add(m)
            enemies.add(m)







    hits = pygame.sprite.groupcollide(bullets,enemies,True,True)
    if hits:
        for hit in hits:
            money += 10
            KO += 1
            piy = pygame.mixer.Sound("img/Sounds/roblox-death-sound-effect.mp3")
            piy.set_volume(0.4)
            m = EnemyPlane(random.choice(enemy_imgs))
            all_sprites.add(m)
            enemies.add(m)
            piy.play()
    #pygame.sprite.collide_rect()
    screan.fill(BLACK)
    screan.blit(background, background_rect)
    #background_rect.x += 1
    all_sprites.draw(screan)
    draw_hp(screan, main_player.hp, main_player.max_hp, main_player.rect.left + 45, main_player.rect.bottom - 40)
    draw_text(screan, 25, 100,20,"hp:"+str(main_player.hp))
    draw_text(screan, 25, 250,20, "Money:" + str(money))
    draw_text(screan, 25, 400, 20, "KO's:" + str(KO))
    draw_text(screan, 30, 400, 650, "Press `m` to menu")
    if main_player.hp <= 0:
        all_sprites.draw(screan)
        draw_text(screan, 60, 400, 400, "GAME OVER")
        draw_text(screan, 20, 400, 450, "*game will close at 2 secs")
        draw_text(screan, 25, 300, 480, "SCORE:")
        draw_text(screan, 18, 400, 480, "Money:" + str(money))
        draw_text(screan, 18, 500, 480, "KO's:" + str(KO))
        if main_player.hp <= -20:
            time.sleep(1)
            game = Menu(choose)
            game.menu()


        pygame.display.update()

    pygame.display.update()

    clock.tick(FPS)



pygame.quit()
exit()



