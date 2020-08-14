import pygame, random, pygame.mouse, time
from pygame.locals import *
from numpy import *

max_tps = 70.0
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (150, 150, 150)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0 ,255 ,0 )
DARK_RED=(139, 0, 0)
AQUAMARINE=(102, 205, 170)

INSTRUKCJA = pygame.image.load('instrukcja.jpg')
pygame.init()
screen = pygame.display.set_mode((1100, 640))
pygame.display.set_caption('Statki')
tlo=pygame.image.load('warships.jpg')
screen.blit(tlo, (0, 0))

def otocz_statki(tab, x, y):
    tab[x - 1][y - 1] = -1
    tab[x - 1][y] = -1
    tab[x - 1][y + 1] = -1
    tab[x][y - 1] = -1
    tab[x][y + 1] = -1
    tab[x + 1][y - 1] = -1
    tab[x + 1][y] = -1
    tab[x + 1][y + 1] = -1

def rysuj_statek(tab, n):
    kierunek = random.randint(1, 3)
    while True:
        x = random.randint(1, 11)
        y = random.randint(1, 11)
        if (tab[x][y] == 0 and x + n < 12 and y + n < 12):
            break
        else:
            continue
    if (kierunek == 1):
        for i in range(0, n):
            otocz_statki(tab, x + i, y)
        for i in range(0, n):
            tab[x + i][y] = 1
    elif (kierunek == 2):
        for i in range(0, n):
            otocz_statki(tab, x, y + i)
        for i in range(0, n):
            tab[x][y + i] = 1

def losuj_statki():
    random.seed()
    statki = zeros((10, 10), int)
    tab = zeros((12, 12), int)
    # wypełnianie brzegów -1
    for i in range(12):
        tab[0][i] = -1
        tab[11][i] = -1
        tab[i][0] = -1
        tab[i][11] = -1
    # rysowanie statków dopóki nie będzie odpowiednia ilość
    while True:
        rysuj_statek(tab, 4)
        for i in range(2):
            rysuj_statek(tab, 3)
        for i in range(3):
            rysuj_statek(tab, 2)
        for i in range(4):
            rysuj_statek(tab, 1)
        licznik = 0
        for i in range(12):
            for j in range(12):
                if (tab[i][j] == 1):
                    licznik = licznik + 1
        if (licznik == 20):
            break
        else:
            tab = zeros((12, 12), int)
    # usuwanie wartości -1 z tabelki
    for i in range(12):
        for j in range(12):
            if (tab[i][j] == -1):
                tab[i][j] = 0
    # przekształcanie na tabelke 10x10
    for i in range(10):
        for j in range(10):
            statki[i][j] = tab[i + 1][j + 1]
    return statki

def ruch_gracza(tab1, tab2, tura):
    event_happened = False
    while not event_happened:
        czy_wygrana(tab1,tura)
        rysuj_plansze(tab1, tab2)
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            strzal(x, y, tab2)
            if (tab2[(x - 600) // 40][(y - 120) // 40] == -1) :
                event_happened = True
            else:
                rysuj_plansze(tab1 , tab2)
                time.sleep(1)
                screen.blit(tlo, (0, 0))
                czy_wygrana(tab2, tura)


    rysuj_plansze(tab1, tab2)
    time.sleep(0.5)

def strzal(x, y, tab2):
    if x >= 600 and x <= 1200 and y >= 120 and y <= 520:
        if tab2[(x - 600) // 40][(y - 120) // 40] == 1:
            tab2[(x - 600) // 40][(y - 120) // 40] = 2
        if tab2[(x - 600) // 40][(y - 120) // 40] == 0:
            tab2[(x - 600) // 40][(y - 120) // 40] = -1

def strzal_AI(x,y,tab):
    if tab[x][y]==1:
        tab[x][y]=2
    elif tab[x][y]==0:
        tab[x][y]=-1

def ruch_AI(tab1,tab2, tura):
    while True:
        random.seed()
        czy_wygrana(tab1, tura)
        x = random.randint(0, 10)
        y = random.randint(0, 10)
        strzal_AI(x,y,tab2)
        if tab2[x][y]==-1:
            break
        elif tab2[x][y]==2:
            time.sleep(0.5)
            screen.blit(tlo,(0,0))
            czy_wygrana(tab2,tura)

def kolor_lewa(tab, x, y):
    # 0 puste, nitrafione pole BIAŁY
    # 1 statek, nietrafiony BIAŁY
    # 3 strzelone, trafione, CZERWONY
    # -1 strzelone, nietrafione, NIEBIESKI
    # 2 podświetlenie SZARY
    if (tab[x][y] == 3):
        return RED
    elif (tab[x][y] == -1):
        return BLUE
    elif (tab[x][y]==1):
        return DARK_RED
    elif (tab[x][y] == 2):
        return GREY
    else:
        return AQUAMARINE

def kolor_prawa(tab, x, y):
    # 0 puste, nitrafione pole BIAŁY
    # 1 statek, nietrafiony BIAŁY
    # 3 strzelone, trafione, CZERWONY
    # -1 strzelone, nietrafione, NIEBIESKI
    # 2 podświetlenie SZARY
    if (tab[x][y] == 3):
        return RED
    elif (tab[x][y] == -1):
        return BLUE
    elif (tab[x][y] == 2):
        return GREY
    else:
        return AQUAMARINE

def rysuj_plansze(tab1, tab2):
    for x in range(0, 10):  # x
        for y in range(0, 10):  # y
            # argumenty: powierzchnia, kolor, x,y, w,h, grubość linii
            pygame.draw.rect(screen, kolor_lewa(tab1, x, y),
                             pygame.Rect((x * 40 + 100, y * 40 + 120), (35, 35)))
    for x in range(0, 10):  # x
        for y in range(0, 10):  # y
            # argumenty: powierzchnia, kolor, x,y, w,h, grubość linii
            pygame.draw.rect(screen, kolor_prawa(tab2, x, y),
                             pygame.Rect((x * 40 + 600, y * 40 + 120), (35, 35)))
    pygame.display.update()

def napisy(tura):
    if (tura==1):
        text= "TURA GRACZA PIERWSZEGO"
    elif (tura==2):
        text="TURA GRACZA DRUGIEGO"
    czcionka = pygame.font.SysFont("dejavusans", 20)
    text_render = czcionka.render(text, 1, (250, 250, 250))
    screen.blit(text_render, (400, 50))

def licz_statki(tab):
    statki = 0
    for x in range(0, 10):
        for y in range(0, 10):
            if tab[x][y] == 1:
                statki = statki + 1
    return statki

def czy_wygrana(tab, tura):
    statki = licz_statki(tab)
    if statki==0:
        if (tura==1):
            text = "KONIEC GRY - WYGRAŁ GRACZ PIERWSZY!"
        elif (tura==2):
            text="KONIEC GRY - WYGRAŁ GRACZ DRUGI!"
        czcionka = pygame.font.SysFont("dejavusans", 40)
        text_render = czcionka.render(text, 1,DARK_RED)
        screen.blit(text_render, (150, 250))
        pygame.display.flip()
        time.sleep(2)
        exit(1)

def instrukcja():
    pygame.init()
    screen = pygame.display.set_mode((1100,640))
    screen.blit(INSTRUKCJA, (0, 0))
    pygame.display.flip()
    while True:
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if (pressed[pygame.K_SPACE]):
                return

def menu():
    small_font = pygame.font.SysFont('monospace', 20)
    myfont = pygame.font.SysFont('monospace', 40)
    pygame.init()
    screen = pygame.display.set_mode((1100, 640))
    menu_position = 1
    screen.blit(tlo, (0,0))
    instructions = small_font.render("Sterowanie po menu strzalkami, a wybor spacja", 1, DARK_RED)
    txt = myfont.render("WARSHIPS", 1, (0,0,0))
    play = myfont.render("PvP", 1, AQUAMARINE )
    ai= myfont.render("PvAI", 1, AQUAMARINE)
    zas= myfont.render("Zasady Gry", 1, AQUAMARINE)
    ext = myfont.render("Exit", 1, AQUAMARINE)
    screen.blit(txt, (450, 25))
    pygame.display.flip()
    while True:
        screen.blit(tlo, (0,0))
        screen.blit(txt, (450, 25))
        screen.blit(instructions, (300, 550))

        nacisk = pygame.key.get_pressed()

        if (menu_position == 1):
            play2 = myfont.render("PvP", 1, RED)
            screen.blit(play2, (520, 150))
            screen.blit(ai, (500, 250))
            screen.blit(zas, (420, 350))
            screen.blit(ext, (500, 450))
        elif (menu_position == 2):
            ai2 = myfont.render("PvAI", 1, RED)
            screen.blit(play, (520, 150))
            screen.blit(ai2, (500, 250))
            screen.blit(zas, (420, 350))
            screen.blit(ext, (500, 450))
        elif (menu_position == 3):
            zas2 = myfont.render("Zasady Gry", 1, RED)
            screen.blit(play, (520, 150))
            screen.blit(ai, (500, 250))
            screen.blit(zas2, (420, 350))
            screen.blit(ext, (500, 450))
        elif (menu_position == 4):
            ext2 = myfont.render("Exit", 1, RED)
            screen.blit(play, (520, 150))
            screen.blit(ai, (500, 250))
            screen.blit(zas, (420, 350))
            screen.blit(ext2, (500, 450))
        for event in pygame.event.get():
            if nacisk[pygame.K_UP]:
                if (menu_position != 1):
                    menu_position -= 1

            if (nacisk[pygame.K_DOWN]):
                if (menu_position != 4):
                    menu_position += 1
            if nacisk[pygame.K_SPACE]:
                return menu_position
        pygame.display.flip()

def muzyka():
    pygame.mixer.music.load('szanta.mp3')
    pygame.mixer.music.play(-1)

tab1 = losuj_statki()
time.sleep(0.1)
tab2 = losuj_statki()

while True:
    menu_return = menu()
    if menu_return == 1:
        break
    elif menu_return == 2:
        break
    elif menu_return == 3:
        instrukcja()
    elif menu_return == 4:
        exit(0)

screen.blit(tlo, (0,0))
muzyka()

if menu_return == 1:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                sys.exit(0)
        napisy(1)
        ruch_gracza(tab1, tab2, 1)
        screen.blit(tlo, (0, 0))
        napisy(2)
        ruch_gracza(tab2, tab1, 2)
        screen.blit(tlo, (0, 0))

elif menu_return == 2:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    sys.exit(0)
            napisy(1)
            ruch_gracza(tab1, tab2, 1)
            screen.blit(tlo, (0, 0))
            ruch_AI(tab2,tab1,2)
