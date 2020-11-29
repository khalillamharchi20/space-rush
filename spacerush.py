import pygame
import sys
from pygame.locals import *
from sys import exit
import time
from pygame import mixer
from math import *
from pygame.locals import *
import random

pygame.init()
screen = pygame.display.set_mode((500, 700), 0, 32)
click = False
mainClock = pygame.time.Clock()
cursor_img = pygame.image.load('data/images/cursor.png').convert_alpha()
pygame.mouse.set_visible(False)
pygame.display.set_caption("SPACE RUSH")
icon = pygame.image.load("data/images/icon.png")
pygame.display.set_icon(icon)
#background = pygame.image.load()
mute=False
f = 300
infoimg = pygame.image.load('data/images/infobg.png').convert_alpha()
left_arrow = pygame.image.load('data/images/arrow.png').convert_alpha()
right_arrow = pygame.image.load('data/images/arrow_right.png').convert_alpha()
font = pygame.font.SysFont("Arial", 65)
font2 = pygame.font.SysFont("Arial", 40)
font3 = pygame.font.SysFont("Arial", 80)
sprite = pygame.transform.scale(pygame.image.load('data/images/rocket.png').convert_alpha(), (60, 60))
player = pygame.sprite.Sprite()
player.image = sprite
player.rect = player.image.get_rect()
player.mask = pygame.mask.from_surface(player.image)
mixer.music.load("data/audio/space.mp3")
mixer.music.play(-1)
collision_sound = mixer.Sound("data/audio/collision.wav")
welcome_sound = mixer.Sound("data/audio/welcome.wav")
increasing_sound = mixer.Sound("data/audio/increasing.wav")
obstacles = [pygame.image.load('data/images/obstacles/obstacles' + str(i) + '.png').convert_alpha() for i in range(1,16)]
t = 0
ran = [random.randint(1, 15) for i in range(40)]
sprites = []

for i in ran:
    sprites.append(pygame.sprite.Sprite())


def cursor():
    x,y=pygame.mouse.get_pos()
    screen.blit(cursor_img,(x-18,y+3))


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)



def highscore():
    high=pygame.image.load('data/images/highscore.png').convert_alpha()
    f = open("data/text/highscore.txt", "r")
    n = open("data/text/nom.txt", "r")
    k = f.read()
    l = n.read()

    bg = pygame.image.load('data/images/background2.jpg')
    clock = pygame.time.Clock()
    ast_image = pygame.image.load('data/images/menu-asteroid.png').convert_alpha()
    ast_image1 = pygame.image.load('data/images/menu-asteroid1.png').convert_alpha()
    ast_image2 = pygame.image.load('data/images/menu-asteroid2.png').convert_alpha()
    asts_acc = []
    for i in range(60):
        v = pygame.Vector2(random.randrange(-5, 5), random.randrange(-5, 5))
        if v == (0, 0): v = (4, -3)
        asts_acc.append(v)

    asts = [ast_image for i in range(20)] + [ast_image1 for i in range(20)] + [ast_image2 for i in range(20)]
    start = []
    for i in range(60):
        v = pygame.Vector2(random.randrange(-4000, 4000), random.randrange(-4800, 4800))
        if (v.x <= 500 and v.x >= -20) or (v.y <= -20 or v.y >= 700):
            v = pygame.Vector2(random.randrange(-4000, 0), random.randrange(700, 4800))
        start.append(v)
    ast_pos = start
    bg_x, bg_y = 0, 0
    s = 2
    while True:
        screen.blit(bg, (bg_x, bg_y))
        bg_y += s
        if bg_y > 0:
            screen.blit(bg, (0, bg_y - 700))
            screen.blit(bg, (0 + 490, bg_y - 700))
            screen.blit(bg, (0 - 490, bg_y - 700))
        if bg_y < 0:
            screen.blit(bg, (0, bg_y + 700))
            screen.blit(bg, (0 + 490, bg_y - 700))
            screen.blit(bg, (0 - 490, bg_y - 700))
        if (bg_y > 700) or (bg_y <= -700):
            bg_y = 0
        for i in range(40):
            ast_pos[i].x -= asts_acc[i][0]
            ast_pos[i].y += asts_acc[i][1]
            screen.blit(asts[i], ast_pos[i])
            if (ast_pos[i].x > 900 or ast_pos[i].y > 900):
                ast_pos[i] = pygame.Vector2(random.randrange(-1000, 0), random.randrange(-1000, 0))
        mx, my = pygame.mouse.get_pos()
        s = 6 - my / 144
        screen.blit(high, (0, 0))
        button = pygame.image.load('data/images/buttons/return.png').convert_alpha()
        buttonhover = pygame.image.load('data/images/buttons/return-hover.png').convert_alpha()
        screen.blit(button, (100, 10))
        buttonrect = button.get_rect()
        buttonrect = buttonrect.move(100, 10)

        draw_text(k, font, (255,69,0), screen, 120, 490)
        draw_text(l, font, (255,69,0), screen, 120, 340)
        if buttonrect.collidepoint((mx, my)):
            screen.blit(buttonhover, (100, 10))
            if pygame.mouse.get_pressed()[0]:
                main_menu()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        cursor()
        pygame.display.update()
        mainClock.tick(60)


def change_highsocre(score):
    bg = pygame.image.load('data/images/background2.jpg')
    newhigh=pygame.image.load('data/images/newhigh.png')
    word = ""
    pygame.display.update()
    click = ""
    done = True
    pygame.key.set_repeat(1, 1000)
    while done:
        mx, my = pygame.mouse.get_pos()
        screen.blit(bg, (0, 0))
        screen.blit(newhigh, (0, 0))
        draw_text(str(score), font, (255,69,0), screen, 210, 340)
        button = pygame.image.load('data/images/buttons/check.png').convert_alpha()
        buttonhover = pygame.image.load('data/images/buttons/check-hover.png').convert_alpha()
        screen.blit(button, (330, 10))
        buttonrect = button.get_rect()
        buttonrect = buttonrect.move(330, 10)
        if buttonrect.collidepoint((mx, my)):
            screen.blit(buttonhover, (330, 10))
            if pygame.mouse.get_pressed()[0]:
                done = False
        cursor()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    word += "q"
                if event.key == pygame.K_b:
                    word += "b"
                if event.key == pygame.K_c:
                    word += "c"
                if event.key == pygame.K_d:
                    word += "d"
                if event.key == pygame.K_e:
                    word += "e"
                if event.key == pygame.K_f:
                    word += "f"
                if event.key == pygame.K_g:
                    word += "g"
                if event.key == pygame.K_h:
                    word += "h"
                if event.key == pygame.K_i:
                    word += "i"
                if event.key == pygame.K_j:
                    word += "j"
                if event.key == pygame.K_k:
                    word += "k"
                if event.key == pygame.K_l:
                    word += "l"
                if event.key == pygame.K_m:
                    word +="m"
                if event.key == pygame.K_n:
                    word += "n"
                if event.key == pygame.K_o:
                    word += "o"
                if event.key == pygame.K_p:
                    word += "p"
                if event.key == pygame.K_q:
                    word += "a"
                if event.key == pygame.K_r:
                    word += "r"
                if event.key == pygame.K_s:
                    word += "s"
                if event.key == pygame.K_t:
                    word += "t"
                if event.key == pygame.K_u:
                    word += "u"
                if event.key == pygame.K_v:
                    word += "v"
                if event.key == pygame.K_w:
                    word += "z"
                if event.key == pygame.K_x:
                    word += "x"
                if event.key == pygame.K_y:
                    word += "y"
                if event.key == pygame.K_z:
                    word += "w"
                if event.key == pygame.K_0:
                    word += "0"
                if event.key == pygame.K_1:
                    word += "1"
                if event.key == pygame.K_2:
                    word += "2"
                if event.key == pygame.K_3:
                    word += "3"
                if event.key == pygame.K_4:
                    word += "4"
                if event.key == pygame.K_5:
                    word += "5"
                if event.key == pygame.K_6:
                    word += "6"
                if event.key == pygame.K_7:
                    word += "7"
                if event.key == pygame.K_8:
                    word += "8"
                if event.key == pygame.K_9:
                    word += "9"

                if event.key == pygame.K_ESCAPE:
                    done = False
            draw_text(word, font, (255,69,0), screen, 160, 540)
            pygame.display.update()

    f = open("data/text/nom.txt", "w")
    f.write(word)


def info():
    global click
    bg = pygame.image.load('data/images/background2.jpg')
    clock = pygame.time.Clock()
    ast_image = pygame.image.load('data/images/menu-asteroid.png').convert_alpha()
    ast_image1 = pygame.image.load('data/images/menu-asteroid1.png').convert_alpha()
    ast_image2 = pygame.image.load('data/images/menu-asteroid2.png').convert_alpha()
    asts_acc = []
    for i in range(60):
        v = pygame.Vector2(random.randrange(-5, 5), random.randrange(-5, 5))
        if v == (0, 0): v = (4, -3)
        asts_acc.append(v)

    asts = [ast_image for i in range(20)] + [ast_image1 for i in range(20)] + [ast_image2 for i in range(20)]
    start = []
    for i in range(60):
        v = pygame.Vector2(random.randrange(-4000, 4000), random.randrange(-4800, 4800))
        if (v.x <= 500 and v.x >= -20) or (v.y <= -20 or v.y >= 700):
            v = pygame.Vector2(random.randrange(-4000, 0), random.randrange(700, 4800))
        start.append(v)
    ast_pos = start
    bg_x, bg_y = 0, 0
    s = 2
    while True:
        screen.blit(bg, (bg_x, bg_y))
        bg_y += s
        if bg_y > 0:
            screen.blit(bg, (0, bg_y - 700))
            screen.blit(bg, (0 + 490, bg_y - 700))
            screen.blit(bg, (0 - 490, bg_y - 700))
        if bg_y < 0:
            screen.blit(bg, (0, bg_y + 700))
            screen.blit(bg, (0 + 490, bg_y - 700))
            screen.blit(bg, (0 - 490, bg_y - 700))
        if (bg_y > 700) or (bg_y <= -700):
            bg_y = 0
        for i in range(40):
            ast_pos[i].x -= asts_acc[i][0]
            ast_pos[i].y += asts_acc[i][1]
            screen.blit(asts[i], ast_pos[i])
            if (ast_pos[i].x > 900 or ast_pos[i].y > 900):
                ast_pos[i] = pygame.Vector2(random.randrange(-1000, 0), random.randrange(-1000, 0))
        mx, my = pygame.mouse.get_pos()
        s = 6 - my / 144
        click=False
        screen.blit(infoimg, (0, 0))
        button= pygame.image.load('data/images/buttons/return.png').convert_alpha()
        buttonhover = pygame.image.load('data/images/buttons/return-hover.png').convert_alpha()
        screen.blit(button, (10, 10))
        buttonrect = button.get_rect()
        buttonrect = buttonrect.move(10, 10)

        if buttonrect.collidepoint((mx, my)):
            screen.blit(buttonhover, (10, 10))
            if pygame.mouse.get_pressed()[0]:
                main_menu()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        cursor()
        pygame.display.update()
        mainClock.tick(60)


def main_menu():
    global click
    global mute
    bg = pygame.image.load('data/images/background2.jpg')
    clock = pygame.time.Clock()
    ast_image = pygame.image.load('data/images/menu-asteroid.png').convert_alpha()
    ast_image1 = pygame.image.load('data/images/menu-asteroid1.png').convert_alpha()
    ast_image2 = pygame.image.load('data/images/menu-asteroid2.png').convert_alpha()
    logo=pygame.image.load('data/images/logo.png').convert_alpha()
    asts_acc=[]
    for i in range(60):
        v=pygame.Vector2(random.randrange(-5,5),random.randrange(-5,5))
        if v==(0,0):v=(4,-3)
        asts_acc.append(v)

    asts=[ast_image for i in range(20)]+[ast_image1 for i in range(20)]+[ast_image2 for i in range(20)]
    start=[]
    for i in range(60):
        v=pygame.Vector2(random.randrange(-4000,4000),random.randrange(-4800,4800))
        if (v.x<=500 and v.x>=-20) or (v.y<=-20 or v.y>=700):
            v=pygame.Vector2(random.randrange(-4000,0),random.randrange(700,4800))
        start.append(v)
    ast_pos = start
    bg_x,bg_y=0,0
    s=2
    while True:
        screen.blit(bg, (bg_x, bg_y))
        bg_y+=s
        if bg_y > 0:
            screen.blit(bg, (0, bg_y  - 700))
            screen.blit(bg, (0 + 490, bg_y  - 700))
            screen.blit(bg, (0- 490, bg_y  - 700))
        if bg_y  < 0:
            screen.blit(bg, (0, bg_y  + 700))
            screen.blit(bg, (0+ 490, bg_y  - 700))
            screen.blit(bg, (0- 490,bg_y  - 700))
        if (bg_y  > 700) or (bg_y  <= -700):
            bg_y  = 0
        for i in range(40):
            ast_pos[i].x-=asts_acc[i][0]
            ast_pos[i].y+=asts_acc[i][1]
            screen.blit(asts[i], ast_pos[i])
            if (ast_pos[i].x>900 or ast_pos[i].y>900):
                ast_pos[i]=pygame.Vector2(random.randrange(-1000,0),random.randrange(-1000,0))
        mx, my = pygame.mouse.get_pos()
        s=6-my/144
        button_1=pygame.image.load('data/images/buttons/play-button.png').convert_alpha()
        button_1hover=pygame.image.load('data/images/buttons/play-button-hover.png').convert_alpha()
        screen.blit(button_1,(145,400))
        button_1rect=button_1.get_rect()
        button_1rect=button_1rect.move(145,400)
        button_2 = pygame.image.load('data/images/buttons/leaderboard.png').convert_alpha()
        button_2hover = pygame.image.load('data/images/buttons/leaderboard-hover.png').convert_alpha()
        screen.blit(button_2, (10, 10))
        button_2rect = button_2.get_rect()
        button_2rect = button_2rect.move(10, 10)
        button_4 = pygame.image.load('data/images/buttons/info.png').convert_alpha()
        button_4hover = pygame.image.load('data/images/buttons/info-hover.png').convert_alpha()
        screen.blit(button_4, (210, 10))
        button_4rect = button_4.get_rect()
        button_4rect = button_4rect.move(210, 10)
        muted = pygame.image.load('data/images/buttons/music-off.png').convert_alpha()
        unmuted = pygame.image.load('data/images/buttons/music-on.png').convert_alpha()
        if mute:
            button_3 = muted
            pygame.mixer.music.set_volume(0)
        else :
            button_3 = unmuted
            pygame.mixer.music.set_volume(1)
        screen.blit(button_3, (413, 10))
        button_3rect = button_3.get_rect()
        button_3rect = button_3rect.move(413, 10)

        if button_1rect.collidepoint((mx, my)):
            screen.blit(button_1hover, (145, 400))
            if click:
                game()
        if button_2rect.collidepoint((mx, my)):
            screen.blit(button_2hover, (10, 10))
            if click:
                highscore()
        if button_3rect.collidepoint((mx, my)):
            if click:
                mute=not mute
                screen.blit(button_3, (413, 10))
        if button_4rect.collidepoint((mx, my)):
            screen.blit(button_4hover, (210, 10))
            if click:
                info()
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        screen.blit(logo, (0, 00))
        cursor()
        pygame.display.update()
        mainClock.tick(60)
    click = False



def update_player(Vect):
    player.rect.topleft = Vect
    screen.blit(player.image, player.rect)


def update_obstacle(obstacle, x, y):
    obstacle.rect.topleft = x, y
    screen.blit(obstacle.image, obstacle.rect)



def game():
    pygame.key.set_repeat(1, 10)
    i = 1
    pause=False
    global ran
    score=0
    running = True
    pygame.init()
    ##screen = pygame.display.set_mode((500, 700), 0, 32)
    background = pygame.image.load('data/images/background23.jpg').convert_alpha()  # type: object
    scorebutton=pygame.image.load('data/images/score.png').convert_alpha()
    clock = pygame.time.Clock()
    welcome_sound.play()
    obstacle_pos=pygame.Vector2(0,-1800)
    player_pos = pygame.Vector2(248, 530)
    background_pos=pygame.Vector2(0, 0)
    movement_direction=-1
    player_speed = 100
    player_rotation = 0.
    player_rotation_speed = 300.  # Degrees per second
    rotation_direction = 0.  # prend les valeurs +1 ou -1
    while running:
        rotation_direction = 0.
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_p:
                    pause=True
                if event.key == K_SPACE:
                    if (i % 2 == 0):
                        rotation_direction = -1.0
                    else:
                        rotation_direction = +1.0
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    rotation_direction = 0
                    i += 1

        screen.blit(background, background_pos)
        if background_pos.x > 0:
            screen.blit(background, (background_pos.x - 490, background_pos.y))
            screen.blit(background, (background_pos.x - 490, background_pos.y - 700))
            screen.blit(background, (background_pos.x - 490, background_pos.y + 700))
        if background_pos.x < 0:
            screen.blit(background, (background_pos.x + 490, background_pos.y))
            screen.blit(background, (background_pos.x + 490, background_pos.y - 700))
            screen.blit(background, (background_pos.x + 490, background_pos.y + 700))
        if background_pos.y > 0:
            screen.blit(background, (background_pos.x, background_pos.y - 700))
            screen.blit(background, (background_pos.x + 490, background_pos.y - 700))
            screen.blit(background, (background_pos.x - 490, background_pos.y - 700))
        if background_pos.y < 0:
            screen.blit(background, (background_pos.x, background_pos.y + 700))
            screen.blit(background, (background_pos.x + 490, background_pos.y - 700))
            screen.blit(background, (background_pos.x - 490, background_pos.y - 700))
        if (background_pos.x > 490) or (background_pos.x <= -490):
            background_pos.x = 0
        if (background_pos.y > 700) or (background_pos.y <= -700):
            background_pos.y = 0
        r = 0
        global f
        for j in ran:
            global t
            t += f
            sprites[r].image = obstacles[j - 1]
            sprites[r].rect = sprites[r].image.get_rect()
            sprites[r].mask = pygame.mask.from_surface(sprites[r].image)
            update_obstacle(sprites[r], obstacle_pos.x, obstacle_pos.y - t)
            r += 1
        t = 0
        if obstacle_pos.y<-300:
            player_speed+=0.5
        if (obstacle_pos.y > 12800):
            increasing_sound.play()
            obstacle_pos.y = -300
            player_rotation_speed += 30
            player_speed += 100
        if (i % 2 == 1):
            screen.blit(left_arrow, (200, 600))
        else:
            screen.blit(right_arrow, (200, 600))
        screen.blit(scorebutton, (10,10))
        draw_text(str(int(score)), font2, (255, 255, 255), screen, 160, 16)
        player.image = pygame.transform.rotate(sprite, player_rotation)
        w, h = player.image.get_size()
        sprite_draw_pos = pygame.Vector2(player_pos.x - w / 2, player_pos.y - h / 2)
        update_player(sprite_draw_pos)
        # on introduit la notion du temps pour faire de la cinematique
        # avantage : on controle avec precision la vitesse de l'objet. Elle devient independante de l'ordinateur.
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.0
        # angle = direction (+1 ou -1) * vitesse * temps (equation horaire)
        player_rotation += rotation_direction * player_rotation_speed * time_passed_seconds
        heading_x = sin(player_rotation * pi / 180.0)
        heading_y = cos(player_rotation * pi / 180.0)
        if heading_y>=0:
            score += 0.08
        else :
            score -= 0.5
        heading = pygame.Vector2(heading_x, heading_y)
        heading *= movement_direction
        background_pos -= heading * player_speed * time_passed_seconds
        obstacle_pos-=heading * player_speed * time_passed_seconds
        for j in sprites:
            if pygame.sprite.collide_mask(player, j) or (background_pos.x <= -220 or background_pos.x >= 220) or (obstacle_pos.y <= -2000):
                background_pos.x = 0
                obstacle_pos.y  = -1800
                running = False
                collision_sound.play()
                f = 300
                player_rotation_speed = 300
                ran = [random.randint(1, 15) for i in range(40)]
                if score<0:
                    score=0
                score=int(score)
                draw_text('Score : ' + str(score), font3, (255, 255, 255), screen, 70, 300)
                pygame.display.update()
                time.sleep(1)
                fic = open("data/text/highscore.txt", "r+")
                k = fic.read()
                if k != "":
                    s = int(k)
                    length = len(k)
                    if score > s:
                        fic.write(str(score))
                        fic.close()
                        change_highsocre(score)
                    else:
                        file = open("data/text/highscore.txt", "w")
                        file.write(k)
                        file.close()
                        break
                    n = open("data/text/highscore.txt", "r+")
                    name = n.read()
                    liste = []
                    chaine = ''
                    for exe in range(0, len(name)):
                        if exe >= length:
                            liste.append(name[exe])
                    for exe1 in liste:
                        chaine = chaine + exe1
                    n.close()
                    cha = open("data/text/highscore.txt", "w")
                    cha.write(chaine)
                else:
                    fili = open("data/text/highscore.txt", "w")
                    fili.write(str(score))
                    fili.close()
                    change_highsocre(score)
        pygame.display.update()
        mainClock.tick(60)


main_menu()