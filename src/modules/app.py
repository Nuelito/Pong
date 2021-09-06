import sys, os, random
import pygame
import xml
import math as m

from pygame import *
import xml.etree.ElementTree as ET

from src.modules.Bodies import*
from src.modules.Graphics import*

pygame.init()
pygame.font.init()

#App properties
children = []
paused = False
gameRunning = False
gameEnded = False
inSettings = False
typing = False

resolution = [900, 600]
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Pong")
pygame.display.set_icon(pygame.image.load("src/icon.ico"))

#Fps thing
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial Black", 20)

#Game objects
ball = None

#Game properties
Score1 = 0; Score2 = 0
pLabel, pLabel2 = None, None
sLabel1, sLabel2 = None, None

#Making sound
cFolder = os.path.dirname(os.path.realpath(sys.argv[0]))
winPath = os.path.join(cFolder, "src\\assets\\sfx\\Win.ogg")
pausePath = os.path.join(cFolder, "src\\assets\\music\\Pause.mp3")
menuPath = os.path.join(cFolder, "src\\assets\\music\\Menu.mp3")
dissapPath = os.path.join(cFolder, "src\\assets\\sfx\\Dissapointment.ogg")

winSound = pygame.mixer.Sound(winPath)
pauseSound = pygame.mixer.Sound(pausePath)
menuSound = pygame.mixer.Sound(menuPath)
dissapSound = pygame.mixer.Sound(dissapPath)


winSound.set_volume(.05)
menuSound.set_volume(.05)
pauseSound.set_volume(.01)
dissapSound.set_volume(.05)

dataPath = os.path.join(cFolder, 'src\\data\\settings.xml')
data = ET.parse(dataPath)

#Collecting data
ballSpd = data.find('Ball/speed').text
ballMaxSpd = data.find('Ball/maxspeed').text
maxScore = data.find('Game/maxscore').text

Timer = None
TimerOn = False
gameTime = float(data.find("Game/time").text)

mvtKey = [
    int(data.find('Players/Player1/up').text),
    int(data.find('Players/Player1/down').text),
    int(data.find('Players/Player2/up').text), 
    int(data.find('Players/Player2/down').text)
]
#Checking values
if not maxScore.isnumeric(): maxScore = 2; data.find('Game/maxscore').text = str(maxScore)
else: maxScore = int(data.find('Game/maxscore').text)

def on_right():
    global Score1
    global sLabel1
    global ballSpd
    Score1 = Score1 + 1
    sLabel1.text = str(Score1)
    
    if ball.vel.x > 0: ball.vel.x = int(ballSpd)*m.cos(m.pi/6)
    else: ball.vel.x = -int(ballSpd)*m.cos(m.pi/6)
    if ball.vel.y > 0: ball.vel.y = int(ballSpd)* m.sin(m.pi/3)
    else: ball.vel.y = -int(ballSpd)* m.sin(m.pi/3)

def on_left():
    global Score2
    global sLabel2
    global ballSpd
    Score2 += 1; sLabel2.text = str(Score2)
    
    if ball.vel.x > 0: ball.vel.x = int(ballSpd)*m.cos(m.pi/6)
    else: ball.vel.x = -int(ballSpd)*m.cos(m.pi/6)
    if ball.vel.y > 0: ball.vel.y = int(ballSpd)* m.sin(m.pi/3)
    else: ball.vel.y = -int(ballSpd)* m.sin(m.pi/3)
        
def run_game():
    global gameRunning, gameEnded, inSettings
    global Player1, Player2, ball
    global pLabel, pLabel2
    global Score1, Score2
    global sLabel1, sLabel2
    global ballSpd, ballMaxSpd
    global Timer, gameTime

    gameTime = float(data.find("Game/time").text)
    
    Score1, Score2 = 0, 0

    ballSpd = data.find('Ball/speed').text
    ballMaxSpd = data.find('Ball/maxspeed').text

    Timer = Label(text="", pos=Vector2(450, 100), fontSize=25)
    
    #Creating players
    Player1 = Paddle(pos=Vector2(80,300), keys=[mvtKey[0], mvtKey[1]])
    Player2 = Paddle(pos=Vector2(app.screen.get_size()[0]-80, 300), keys=[mvtKey[2], mvtKey[3]])
    

    ball = Ball(pos=Vector2(450,300), vel=Vector2(int(ballSpd)*m.cos(m.pi/6) * random.choice([-1,1]),int(ballSpd)* m.sin(m.pi/3))); Net()

    sLabel1 = Label(pos=Vector2(230,100), text="0", fontName="Sans Serif", fontSize=150)
    sLabel2 = Label(pos=Vector2(app.screen.get_size()[0]-230,100), text="0", fontName="Sans Serif", fontSize=150)
    
    pLabel = Label("Press 'space' to resume", fontSize=17, pos= (450, 340), render=False, fontName="Arial Black")
    pLabel2 = Label("Press 'r' to restart", fontSize=14, pos= (450, 360), render=False, fontName="Arial Black")
    ball.on_right = on_right
    ball.on_left = on_left
    
    gameRunning = True
    gameEnded = False
    
    menuSound.stop()
    pauseSound.stop()
    winSound.stop()
    dissapSound.stop()
    inSettings = False

def main_menu():
    global title, subTitle, startSign, inSettings
    Label(text="Pong", fontName="Arial Black", pos=Vector2(450, 140), fontSize=130)
    Label(text="Onuelito's Edition", fontName="Arial Black", pos=Vector2(450, 240), fontSize=20)
    Label(text="Press 'space' to start", pos=Vector2(450, 450), fontSize=18, fontName="Arial Black")
    Label(text="Press 's' for settings", pos=Vector2(450, 480), fontSize=12, fontName="Arial Black")
    
    #menuSound.play() #Not good mate
    pauseSound.stop()
    inSettings = False

def settings():
    global inSettings, data, TimerOn

    p1Name, p2Name = data.find('Players/Player1/name'),  data.find('Players/Player2/name')
    ballSpeed, ballMaxSpeed = data.find("Ball/speed"), data.find("Ball/maxspeed")

    #Headers
    Label("Settings", pos=Vector2(450, 100))
    Label("Ball settings", pos=Vector2(200, 210), fontSize=18)
    Label("Game settings", pos=Vector2(450, 200), fontSize=20)
    Label("Paddle settings", pos=Vector2(700, 210), fontSize=18)

    #Players
    Name1 = Entry(text = str(p1Name.text), pos=Vector2(700, 260), fontSize=20, size=Vector2(150, 22))
    Name2 = Entry(text = str(p2Name.text), pos=Vector2(700, 310), fontSize=20, size=Vector2(150, 22))

    Label("(Player1, name)", pos=Vector2(700, 280), fontSize=12)
    Label("(Player2, name)", pos=Vector2(700, 330), fontSize=12)

    #Ball
    ballSpeed = Entry(text = data.find('Ball/speed').text, pos=Vector2(200, 260), fontSize=20, size=Vector2(150, 22))
    ballMaxSpeed = Entry(text = data.find('Ball/maxspeed').text, pos=Vector2(200, 310), fontSize=20, size=Vector2(150, 22))

    NoteBallS = Label("(Ball, speed)", pos=Vector2(200, 280), fontSize=12)
    NoteBallMS = Label("(Ball, max speed)", pos=Vector2(200, 330), fontSize=12)

    #Game
    maxS = Entry(text=data.find('Game/maxscore').text, pos=Vector2(450, 250), fontSize=20, size=Vector2(150, 22))
    timer = Entry(text=data.find('Game/time').text, pos=Vector2(450, 310), fontSize=20, size=Vector2(150, 22))
    timerTF = CheckBox(pos=Vector2(450, 400), checked=TimerOn)

    NoteScore = Label("(Game, max score)", pos=Vector2(450, 275), fontSize=12)
    NoteTime = Label("(Game, time limit)", pos=Vector2(450, 335), fontSize=12)
    Label("(Timer?)", pos=Vector2(450, 425), fontSize=12)

    Label("Press 'escape' for main menu", pos=Vector2(450, 550), fontSize=12)

    #Inputs
    p1Up = InputSaver(input = int(data.find('Players/Player1/up').text),pos=Vector2(630, 400), fontSize=20)
    p1Down = InputSaver(input = int(data.find('Players/Player1/down').text), pos=Vector2(770, 400), fontSize=20)

    Label(text="(Player1, up)", pos=Vector2(630, 420), fontSize=12)
    Label(text="(Player1, down)", pos=Vector2(770, 420), fontSize=12)

    p2Up = InputSaver(input = int(data.find('Players/Player2/up').text),pos=Vector2(630, 450), fontSize=20)
    p2Down = InputSaver(input = int(data.find('Players/Player2/down').text),pos=Vector2(770, 450), fontSize=20)

    Label(text="(Player2, up)", pos=Vector2(630, 470), fontSize=12)
    Label(text="(Player2, down)", pos=Vector2(770, 470), fontSize=12)

    #Creating event function
    def deactivate1():
        data.find('Players/Player1/name').text = Name1.text

    def deactivate2():
        data.find('Players/Player2/name').text = Name2.text

    #Ball speed stuff
    def ball_activate():
        fix_txt = ""
        for txt in ballSpeed.text:
            if txt.isnumeric(): fix_txt += str(txt)
        if fix_txt == "": fix_txt ="8"
        ballSpeed.text = str(int(fix_txt))
        if int(ballSpeed.text) >= 100: ballSpeed.text="99"
        data.find('Ball/speed').text = ballSpeed.text

        #Changing note
        NoteBallS.text = "(Ball, speed)"
        if int(ballSpeed.text) == 0: NoteBallS.text = "(Really?)"
        #if int(ballSpeed.text) >= 20: NoteBallS.text = "(Starting fast)"
        #if int(ballSpeed.text) >= 50: NoteBallS.text = "(Good luck with that)"
        if int(ballSpeed.text) == 99: NoteBallS.text = "(GAS, GAS, GAS!)"


    def ballmax_activate():
        fix_txt = ""
        for txt in ballMaxSpeed.text:
            if txt.isnumeric(): fix_txt += str(txt)

        if fix_txt == "": fix_txt ="20"
        ballMaxSpeed.text = str(int(fix_txt))
        if int(ballMaxSpeed.text) >= 100: ballMaxSpeed.text="99"
        data.find('Ball/maxspeed').text = ballMaxSpeed.text

        #Changing note
        NoteBallMS.text = "(Ball, max speed)"

        if int(ballMaxSpeed.text) < int(ballSpeed.text): NoteBallMS.text = "(Ok but why thought?)"
        if int(ballMaxSpeed.text) == 0: NoteBallMS.text = "(Bruh)"
        if int(ballMaxSpeed.text) == int(ballSpeed.text): NoteBallMS.text = "(Why even bother)"


    #Game score setup
    def score_activate():
        global maxScore
        fix_txt = ""
        for txt in maxS.text:
            if txt.isnumeric(): fix_txt += str(txt)

        
        if fix_txt == "": fix_txt ="2"
        maxS.text = str(int(fix_txt))
        if int(maxS.text) >= 100: maxS.text="99"
        maxScore = int(maxS.text)
        data.find('Game/maxscore').text = maxS.text

        #Changing note
        NoteScore.text = "(Game, max score)"

        if int(maxS.text) == 0: NoteScore.text = "(Is that event a game?)"

    def on_input_change():
        mvtKey[0] = int(p1Up.input)
        mvtKey[1] = int(p1Down.input)

        mvtKey[2] = int(p2Up.input)
        mvtKey[3] = int(p2Down.input)

        data.find('Players/Player1/up').text = str(mvtKey[0])
        data.find('Players/Player1/down').text = str(mvtKey[1])
        data.find('Players/Player2/up').text = str(mvtKey[2])
        data.find('Players/Player2/down').text = str(mvtKey[3])

    def on_checkbox():
        global TimerOn
        TimerOn = timerTF.checked

    def on_gameTime():
        fix_txt = ""
        for txt in timer.text:
            if txt.isnumeric(): fix_txt += str(txt)

        
        if fix_txt == "": fix_txt ="0"
        timer.text = str(int(fix_txt))
        if int(maxS.text) >= 100: timer.text="999"
        data.find('Game/time').text = timer.text

        #Changing note
        NoteTime.text = "(Game, time limit)"
        if int(timer.text) == 0: NoteTime.text = "(Finished before it started)"

    timerTF.on_activate = on_checkbox
    timerTF.on_deactivate = on_checkbox
    timer.on_unactivate = on_gameTime

    p1Up.on_deactivate = on_input_change
    p1Down.on_deactivate = on_input_change
    p2Up.on_deactivate = on_input_change
    p2Down.on_deactivate = on_input_change

    ballSpeed.on_unactivate = ball_activate
    ballMaxSpeed.on_unactivate = ballmax_activate

    maxS.on_unactivate = score_activate
    

    Name1.on_unactivate = deactivate1
    Name2.on_unactivate = deactivate2
    
    menuSound.stop()
    inSettings = True

def updateSettings():
    global data
    data.write(os.path.join(cFolder, 'src\\data\\settings.xml'))
    

def test():
    pass


keyList = []
mouseList = []

#test()
updateSettings()
main_menu()
def run():
    global paused, children, gameRunning, gameEnded, keyList, mouseList, data
    global gameTime, Timer
    while True:
        screen.fill([0,0,0])
        keyList= []
        mouseList = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseList.append(event)

            if event.type == pygame.KEYDOWN:
                keyList.append(event)
                
                # Pause and start button
                if event.key == pygame.K_SPACE and not typing and not inSettings:
                    if gameRunning:
                        if not gameEnded:
                            paused = not paused
                            pLabel.render = paused
                            pLabel2.render = paused
                            
                            if paused == True: pauseSound.play()
                            else: pauseSound.stop()
                        else:
                            paused = False
                            children = []
                            pauseSound.stop()
                            run_game()
                    else:
                        children = []
                        pauseSound.stop()
                        run_game()
                
                # Main Menu button
                if event.key == pygame.K_ESCAPE and not typing:
                    children = []
                    gameRunning = False
                    paused = False
                    updateSettings()
                    main_menu()
                
                # Restart button
                if event.key == pygame.K_r and paused:
                    children = []
                    gameRunning = False
                    paused = False
                    run_game()
                    
                if event.key == pygame.K_s and not gameRunning and not inSettings:
                    children = []
                    settings()
        
        
                
            
        for child in children:
            child.update()
            
        # Game ending phase
        if Score1 >= maxScore or Score2 >= maxScore or (gameTime == 0 and TimerOn == True):
            if gameRunning == True and not gameEnded:
                paused = True
                gameEnded = True
                #Data checking

                if Score1 == Score2:
                    Label(text="Nobody wins", fontName="Arial Black", pos=Vector2(450, 230), fontSize=25)
                else:
                    if Score1 > Score2: Label(text=data.find('Players/Player1/name').text + " wins", fontName="Arial Black", pos=Vector2(450, 230), fontSize=25)
                    if Score2 > Score1: Label(text=data.find('Players/Player2/name').text + " wins", fontName="Arial Black", pos=Vector2(450, 230), fontSize=25)

                pLabel.text = "Press 'space' to restart"
                pLabel.render = paused
                pLabel2.render = paused
                ball.render = False

                if Score1 != Score2:
                    winSound.play()
                else:
                    dissapSound.play()
            
        # Setting paddle limits
        if gameRunning and not paused:
            if Player1.pos.y + Player1.size.y/2 > resolution[1]: Player1.pos.y = resolution[1]-Player1.size.y/2
            if Player1.pos.y - Player1.size.y/2 <0: Player1.pos.y = Player1.size.y/2
            
            if Player2.pos.y + Player2.size.y/2 > resolution[1]: Player2.pos.y = resolution[1]-Player2.size.y/2
            if Player2.pos.y - Player2.size.y/2 <0: Player2.pos.y = Player2.size.y/2
            
            
        #fps_txt = font.render(str(int(clock.get_fps())), True, [255,0,0])
        #screen.blit(fps_txt, (0,0))

        if gameRunning and not paused and TimerOn:
            Timer.text = str(int(round(gameTime, 0)))
            gameTime = max(0, gameTime-1/60)
        
        clock.tick(60)
        pygame.display.update()
        
