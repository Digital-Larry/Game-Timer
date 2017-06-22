#Import and initialize
import pygame, random
from pygame.locals import *
global wins, comp, main, deaths, KeepGoing, box_x, box_y
pygame.init()
KeepGoing = True
deaths = 0
wins = 0
main = 1
comp = 0
def check_key():
    
    global box_y, main
    
    keystate = pygame.key.get_pressed()
    if box_y > 0:
        
        if keystate[pygame.locals.K_UP]:
            box_y -= 5
            
    if box_y < 430:
        
        if keystate[pygame.locals.K_DOWN]:
            box_y += 5
            
    if keystate[pygame.locals.K_ESCAPE]:
        main = 1
        
def main_seq():
    global main, KeepGoing, winning, deaths, wins
    
    pygame.init()
    
    deaths = 0
    wins = 0
    color = (200, 200, 150)
    display = True
    
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption("Hello, world!")
    
    intro = "Welcome to pong, please click here to start."
    myFont = pygame.font.SysFont("Comic Sans MS", 15)
    label = myFont.render(intro, 1, (255,25,0))
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    
    while display:
        
        keystate = pygame.key.get_pressed()
        
        if keystate[pygame.locals.K_ESCAPE]:
            display = False
            KeepGoing = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    KeepGoing = False
                    display = False
                    winning = False
                    
            mouse = pygame.mouse.get_pos()
            
            if mouse[0] >= 220 and mouse[0] <= 545 and mouse[1] >= 200 and mouse[1] <= 250:
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    color = (250, 250, 250)
                else:
                    color = (225, 225, 225)
                    
                if event.type == MOUSEBUTTONUP:
                    display = False
                    main = False
                    main = 0
                    
            else:
                color = (200, 200, 200)
                
        bar = pygame.Surface((325, 50))
        bar = bar.convert()
        bar.fill(color)
        
        screen.blit(background, (0,0))
        screen.blit(bar, (180, 200))
        screen.blit(label, (200, 220))
        pygame.display.flip()
        
def winning_game():
    global winning, comp, main, deaths, box_y, KeepGoing
    #Display configuration
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption("Hello, world!")
    
    #Entities (just background for now)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    
    box = pygame.Surface((10, 50))
    box = box.convert()
    box.fill((200,200,150))
    
    paddle = pygame.Surface((10, 50))
    paddle = paddle.convert()
    paddle.fill((200,200,150))
    
    pong_blit = pygame.image.load("pong.bmp")
    pong_blit = pong_blit.convert()
    
    box_x = 625
    box_y = 300
    
    pong_x = random.randrange(60, 300)
    pong_y = random.randrange(60, 400)
    
    paddle_x = 20
    paddle_y = 0
    
    x = 5
    y = 5
    
    bounce = True
    
    text = "Computer: "+ str(deaths) + " User: " + str(wins)
    myFont = pygame.font.SysFont("Comic Sans MS", 12)
    label = myFont.render(text, 1, (255,255,0))
    
    #Assign values to key variables
    clock = pygame.time.Clock()
    winning = True
    dir = 0
    counter = 11
    pong_dir = pong_y
    
    while winning:
        
        clock.tick(30)
        
        box_x_right = box_x + 10
        box_y_bottom = box_y + 50
        pong_x_right = pong_x + 25
        pong_y_bottom = pong_y + 25
        
        check_key()
        
        if main == 1:
            winning = False
        if box_x <= pong_x_right and box_x + 10 >= pong_x_right and box_y <= pong_y_bottom and box_y + 50 >= pong_y_bottom:
            x = -x
            
            if x < 0:
                x -= 0.15
                y -= 0.1
            else:
                x += 0.15
                y += 0.1
                
        if box_x <= pong_x and box_x + 10 >= pong_x and box_y <= pong_y and box_y + 50 >= pong_y:
            x = -x
            
            if x < 0:
                x -= 1
                y -= 0.75
            else:
                x += 1
                y += 0.75
                
        if paddle_x <= pong_x_right and paddle_x + 10 >= pong_x_right and paddle_y <= pong_y_bottom and paddle_y + 50 >= pong_y_bottom:
            x = -x
            faster = ( 1.00 * random.randrange(1, 80))/ 100
            faster_1 = ( 1.10 * random.randrange(1, 120))/ 100
            
            if x < 0:
                x -= faster
                y -= faster_1
            else:
                x += faster
                y += faster_1
                
        if paddle_x <= pong_x and paddle_x + 10 >= pong_x and paddle_y <= pong_y and paddle_y + 50 >= pong_y:
            x = -x
            
            if x < 0:
                x -= 1
                y -= 0.75
            else:
                x += 1
                y += 0.75
        
        dir = 0
        
        if pong_y >= 455:
            y = -y
            
        if pong_y <= 0:
            y = -y
            
        speed = [6, -6]
        
        if pong_x > 350 and pong_y <= random.randrange(1, 480):
            rand = random.randrange(1, 5)
            
            if rand == 3:
                counter = -5
                
        if pong_x < 300:
            counter = 11
            
        if counter > 10:
            
            if paddle_y > pong_y:
                
                if paddle_y > 0 :
                    dir = speed[1]
                elif paddle_y < 0:
                    dir = 0
                    
            if paddle_y < pong_y:
                
                if paddle_y < 430:
                    dir = speed[0]
                elif paddle_y > 430:
                    dir = 0
                    
            elif pong_dir > pong_y and pong_x < 350 and pong_x > 100 and pong_y > 100 and pong_y < 500:
                dir = speed[1]
                
            elif pong_dir < pong_y and pong_x < 350 and pong_x > 100 and pong_y > 100 and pong_y < 500:
                dir = speed[0]
        counter += 1   
        paddle_y += dir
        
        if pong_x >= 615:
            winning = False
            main = 0
            comp = 0
        elif pong_x <= 0 :
            winning = False
            main = 0
            comp = 1
        
        pong_x += x
        pong_y += y
        pong_dir = pong_y
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                KeepGoing = False
                winning = False
        
            
        screen.blit(background, (0,0))
        screen.blit(label, (400,20))
        screen.blit(box, (box_x, box_y))
        screen.blit(paddle, (paddle_x, paddle_y))
        screen.blit(pong_blit, (pong_x, pong_y))
        pygame.display.flip()
def game():
    global deaths, wins, comp, main, KeepGoing
    
    main = 1
    
    while KeepGoing:
        if main == 0:
            
            if comp == 0:
                deaths += 1
            elif comp == 1:
                wins += 1
                
        elif main == 1:
            main_seq()
        winning_game()
if __name__ == "__main__":
    
    game()
