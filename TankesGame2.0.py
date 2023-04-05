import pygame, sys
import random
import time

pygame.init()
pygame.mixer.init()
pygame.font.init()
#print(pygame.font.get_fonts())

pygame.mixer.music.load("img/Music/l39201toile-d39afrique-18_456256703.mp3")
pygame.mixer.music.set_volume(0.2)
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
        self.image = pygame.transform.scale(img,(55,55))

        self.image_up = self.image
        self.image_down = pygame.transform.flip(self.image,False,True)
        self.image_right = pygame.transform.rotate(self.image_up,-90)
        self.image_left = pygame.transform.rotate(self.image_up, 90)

        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.centery = height // 4
        self.speed = 10
        self.hp = 100
        self.max_hp = 100
        self.direction = "STOP"
        self.gun_direction = "UP"



    def move(self,key= "STOP"):
        if key == pygame.K_a:
            self.direction = "LEFT"
            self.image = self.image_left
            self.gun_direction = "LEFT"

        elif key == pygame.K_d:
            self.direction = "RIGHT"
            self.image = self.image_right
            self.gun_direction = "RIGHT"

        elif key == pygame.K_w:
            self.direction = "UP"
            self.image = self.image_up
            self.gun_direction = "UP"

        elif key == pygame.K_s:
            self.direction = "DOWN"
            self.image = self.image_down
            self.gun_direction = "DOWN"

        elif key ==  "STOP":
            self.direction = "STOP"


    def update(self):
        # if KO >= 30: #
        #     img = player_img_KOS
        #     self.image = pygame.transform.scale(img,(65,60))
        #     self.hp = 200
        #     self.max_hp = 200
        keytstate = pygame.key.get_pressed()
        if keytstate[pygame.K_m]:
            game = Menu(choose)
            game.menu()

        old_x = self.rect.x
        old_y = self.rect.y

        if self.direction == "RIGHT":
            self.rect.x += self.speed
        elif self.direction == "LEFT":
            self.rect.x -= self.speed
        elif self.direction == "UP":
            self.rect.y -= self.speed
        elif self.direction == "DOWN":
            self.rect.y += self.speed



        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height

        if pygame.sprite.spritecollide(self,blocks,False):
            self.rect.x = old_x
            self.rect.y = old_y

        if pygame.sprite.spritecollide(self,blocks2,False):
            self.rect.x = old_x
            self.rect.y = old_y



    def shoot(self,bullet_img):
        piy = pygame.mixer.Sound("img/Sounds/Shot 1.0.mp3")
        piy.set_volume(0.2)
        if self.gun_direction == "UP":
            b = Bullet(x = self.rect.centerx, y = self.rect.top, img = bullet_img)
        elif self.gun_direction == "DOWN":
            b = Bullet(x=self.rect.centerx, y=self.rect.bottom, img=bullet_img)
        elif self.gun_direction == "RIGHT":
            b = Bullet(x=self.rect.right, y=self.rect.centery, direction="RIGHT", img=bullet_img)
        elif self.gun_direction == "LEFT":
            b = Bullet(x=self.rect.left, y=self.rect.centery, direction= "UP", img=bullet_img)


        piy.play()
        all_sprites.add(b)
        bullets.add(b)

class Boss(pygame.sprite.Sprite):
    def __init__(self, img):
        super(Boss, self).__init__()
        self.image = pygame.transform.scale(img, (150, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0 + self.rect.w // 2, 600 - self.rect.w // 2)
        self.rect.centery = random.randint(-100, -50)
        self.speedx = random.randint(3, 4)
        self.speedy = random.randint(2, 4)

class Enemy_plane(pygame.sprite.Sprite):
    def __init__(self,img):
        super(Enemy_plane, self).__init__()
        self.image = pygame.transform.scale(img, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0+self.rect.w// 2,600-self.rect.w // 2)
        self.rect.centery = random.randint(-100,-50)
        #self.speed_mnoj = 1.0
        self.speedx = random.randint(-3,3)
        self.speedy = random.randint(2,4)

    def update(self):
        if KO >= 30:
            self.speedx = random.randint(-5, 5)
            self.speedy = random.randint(4, 8)
            if KO >= 100:
                self.speedx = random.randint(-5, 5)
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
    def __init__(self,x,y,img, direction = "UP"):
        super(Bullet, self).__init__()
        self.image = img
        self.image = pygame.transform.scale(self.image, (30, 40))
        self.image_up = self.image
        self.image_down = pygame.transform.flip(self.image, False, True)
        self.image_right = pygame.transform.rotate(self.image_up, -90)
        self.image_left = pygame.transform.rotate(self.image_up, 90)


        self.speed_y = 50
        self.speed_x = 50
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.direction = main_player.gun_direction


    def update(self):
        if self.direction == "UP":
            self.rect.y -= 15
            self.image = self.image_up

        elif self.direction == "DOWN":
            self.rect.y += 15
            self.image = self.image_down

        elif self.direction == "LEFT":
            self.rect.x -= 15
            self.image = self.image_left

        elif self.direction == "RIGHT":
            self.rect.x += 15
            self.image = self.image_right

        if self.rect.bottom < 0:
            self.kill()

        if pygame.sprite.spritecollide(self, blocks, False):
            self.kill()

        if pygame.sprite.spritecollide(self, blocks2, True):
            self.kill()

        if pygame.sprite.spritecollide(self, healBlo, True):
            main_player.hp += 50
            self.kill()

class Block(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super(Block, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
    def update(self):
        pass



player_img1 = pygame.image.load("img/Enemies/tank.png")
player_img_KOS = pygame.image.load("img/Enemies/enemyGreen5.png")
enemy_img1 = pygame.image.load("img/samolet-removebg-preview.png")
player_img_leader= pygame.image.load("img/Enemies/ShipBattleshipHull.png")
laser_img = pygame.image.load("img/raketa2.png")
first = pygame.image.load("img/backgrounds/Zastavka2.0.png")
first = pygame.transform.scale(first, (width,height))
first_rect = first.get_rect()
boss_img = pygame.image.load("img/Enemies/Tank_Boss.png")
background = pygame.image.load("img/desert_2.png")
background = pygame.transform.scale(background, (width,height))
background_rect = background.get_rect()
enemy_imgs = [enemy_img1]

block_img  = pygame.image.load("img/Textures/StonesBrick Textures/Brickwall5_Texture.png")
block_img = pygame.transform.scale(block_img,(36,36))
HealImg = pygame.image.load("img/Textures/StonesBrick Textures/Bluerock_Texture.jpg")
HealImg = pygame.transform.scale(HealImg,(36,36))
block_img2  = pygame.image.load("img/Textures/StonesBrick Textures/Stonewall_Texture.png")
block_img2 = pygame.transform.scale(block_img2,(36,36))

main_player = Player(player_img1)
screan = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
enemies =  pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
blocks2 = pygame.sprite.Group()
healBlo = pygame.sprite.Group()
all_sprites.add(main_player)
end = pygame.font.SysFont('Times new roman', 80)
again = pygame.font.SysFont('Times new roman', 40)


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
     m = Enemy_plane(random.choice(enemy_imgs))
     all_sprites.add(m)
     enemies.add(m)

line_counter = 0
symbol_counter = 0
with open("MapForTanks.txt","r") as map:
    for line in map:
        symbol_counter = 0
        for symbol in line:
            if symbol == "#":
                bl = Block(block_img,symbol_counter*36,line_counter*36)
                blocks.add(bl)
                all_sprites.add(bl)
            symbol_counter += 1
        line_counter += 1

line_counter2 = 0
symbol_counter2 = 0
with open("MapForTanks.txt","r") as map:
    for line in map:
        symbol_counter2 = 0
        for symbol in line:
            if symbol == "$":
                blo = Block(block_img2,symbol_counter2*36,line_counter2*36)
                blocks2.add(blo)
                all_sprites.add(blo)
            symbol_counter2 += 1
        line_counter2 += 1

line_counter3 = 0
symbol_counter3 = 0
with open("MapForTanks.txt","r") as map:
    for line in map:
        symbol_counter3 = 0
        for symbol in line:
            if symbol == "@":
                heal = Block(HealImg,symbol_counter3*36,line_counter3*36)
                healBlo.add(heal)
                all_sprites.add(heal)
            symbol_counter3 += 1
        line_counter3 += 1

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


            else:
                main_player.move(event.key)
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_a,pygame.K_d,pygame.K_w,pygame.K_s]:
                main_player.move()



    hits = pygame.sprite.spritecollide(main_player,enemies,True)
    if hits: # якшо відбулась колізія
        for sprt in hits:
            hitds = pygame.mixer.Sound("img/Sounds/бум.mp3")
            money -= 5
            hitds.set_volume(0.4)
            hitds.play()
            print(sprt.speedx, sprt.speedy)
            main_player.hp -= abs(sprt.speedx) + abs(sprt.speedy)
            m = Enemy_plane(random.choice(enemy_imgs))
            all_sprites.add(m)
            enemies.add(m)



    hits = pygame.sprite.groupcollide(bullets,enemies,True,True)
    if hits:
        for hit in hits:
            if KO >= 30:
                img = player_img_KOS
                main_player.image = pygame.transform.scale(img, (180, 180))
                main_player.hp = 200
                main_player.max_hp = 200
                if KO >= 100:
                    img = player_img_leader
                    main_player.image = pygame.transform.scale(img, (100, 100))
                    main_player.speed = 15
                    main_player.hp = 1000
                    main_player.max_hp = 1000
            money += 10
            KO += 1
            piy = pygame.mixer.Sound("img/Sounds/roblox-death-sound-effect.mp3")
            piy.set_volume(0.4)
            m = Enemy_plane(random.choice(enemy_imgs))
            all_sprites.add(m)
            enemies.add(m)
            piy.play()
    #pygame.sprite.collide_rect()
    screan.fill(BLACK)
    screan.blit(background, background_rect)
    #background_rect.x += 1
    all_sprites.draw(screan)
    draw_hp(screan, main_player.hp, main_player.max_hp, 130, 20)
    draw_text(screan, 25, 70,20,"hp:"+str(main_player.hp))
    draw_text(screan, 25, 800, 20, "KO's:" + str(KO))
    draw_text(screan, 30, 600, 20, "Press `m` to menu")
    if main_player.hp <= 0:
        all_sprites.draw(screan)
        draw_text(screan, 60, 400, 400, "GAME OVER")
        draw_text(screan, 20, 400, 450, "*game will close at 2 secs")
        draw_text(screan, 25, 300, 480, "SCORE:")
        draw_text(screan, 18, 500, 480, "KO's:" + str(KO))
        if main_player.hp <= -20:
            time.sleep(1)
            game = Menu(choose)
            game.menu()
    pygame.display.update()

    clock.tick(FPS)



pygame.quit()
exit()
