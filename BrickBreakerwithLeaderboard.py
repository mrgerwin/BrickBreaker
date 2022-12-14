import pygame
import random
import sqlite3
import ast
#Hi it's Max
def drawHighScoreScreen():
    global DisplayedInfo
    TitleText = GameFont.render("HIGH SCORES", True, white)
    Line1 = GameFont.render(HighList[0][0] + "    " + str(HighList[1][0]), True, white)
    Line2 = GameFont.render(HighList[0][1] + "    " + str(HighList[1][1]), True, white)
    Line3 = GameFont.render(HighList[0][2] + "    " + str(HighList[1][2]), True, white)
    
    ListOfBlocks = [["Light Purple blocks are average", "Red blocks speed up the ball", "Grey blocks add a second ball"], [lightPurple, red, grey]]
    BlockInstructions = GameFont.render(ListOfBlocks[0][DisplayedInfo], True, ListOfBlocks[1][DisplayedInfo])
    
    Directions = GameFont.render("Press SPACE to Continue", True, white)
    StartDirections = GameFont.render("Press ENTER to Start", True, white)
    
    window.blit(TitleText, (screen_size[0]//2-150, 100))
    window.blit(Line1, (screen_size[0]//2-150, 130))
    window.blit(Line2, (screen_size[0]//2-150, 160))
    window.blit(Line3, (screen_size[0]//2-150, 190))
    window.blit(BlockInstructions, (screen_size[0]//2-250, 250))
    window.blit(Directions, (screen_size[0]//2-200, 450))
    window.blit(StartDirections, (screen_size[0]//2-200, 490))

def makeConn():
    conn=sqlite3.connect("breaker.db")
    return conn

def makeTable(conn):
    #Cat
    conn.execute("CREATE TABLE IF NOT EXISTS SCORES(ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, SCORE INT NOT NULL, BLOCKS TEXT NOT NULL);")
    conn.commit()

def makeBlockSave():
    temp = ""
    for block in blocks:
        if temp != "":
            temp += ","
        temp += repr(block.position)
    return temp

def deSerialBlocks(BlocksList):
    global blocks
    blocks = []
    temp = ast.literal_eval(BlocksList[0])
    for location in temp:
        color = random.choice(color_list)
        size = 100
        position = location
        points = random.randint(1,5)
        hits = random.randint(1,3)
        a_block = Block(color, size, position, points, hits)
        blocks.append(a_block)        

def storeData(conn):
    cur = conn.cursor()
    cur.execute("SELECT MAX(ID)FROM SCORES;")
    d = cur.fetchall()
    lastID = d[0][0]
    if lastID == None:
        lastID = 0
    nextID = int(lastID) + 1
    SerialBlocks = makeBlockSave()
    conn.execute("INSERT INTO SCORES(ID, NAME, SCORE, BLOCKS)VALUES(?,?,?,?);",(nextID, player, score, SerialBlocks))
    conn.commit()

def retrieveData(conn):
    global score
    cur = conn.cursor()
    cur.execute("SELECT SCORE FROM SCORES WHERE NAME=?", (player,))
    scores = cur.fetchall()
    cur = conn.cursor()
    cur.execute("SELECT BLOCKS FROM SCORES WHERE NAME=?", (player,))
    
    blocksList = cur.fetchall()
    
    if len(blocksList) != 0:
        deSerialBlocks(blocksList[0])
    
    MaxScore = 0 
    print(scores)
    if len(scores) != 0:
        for score in scores:
            if MaxScore < score[0]:
                MaxScore = score[0]
    score = MaxScore
    #MrGerwin
def findHighScores(conn):
    #Returns a list of names and scores for the top 3 scores from DB.
    
    cur=conn.cursor()
    cur.execute("SELECT * FROM SCORES;")
    data = cur.fetchall()
    slot = []
    name = []
    score = []
    high1 = 0
    high2 = 0
    high3 = 0
    name1 = ""
    name2 = ""
    name3 = ""
    if len(data) != 0:
        for row in data:
            slot.append(row[0])
            name.append(row[1])
            score.append(row[2])
    
    for i in range(len(score)):
        if high1 < score[i]:
            high1 = score[i]
            name1 = name[i]
    
    for j in range(len(score)):
        if score[j] != high1:
            if high2< score[j]:
                high2 = score[j]
                name2 = name[j]
                
    for k in range(len(score)):
        if score[k] != high1 and score[k] != high2:
            if high3<=score[k]:
                high3 = score[k]
                name3 = name[k]
                
    names = [name1, name2, name3]
    scores = [high1, high2, high3]
    
    return [names, scores]

def drawScore():
    global score, white, DiePlaying
    ScoreText = GameFont.render("Score:"+ str(score), True, white)
    NameText = GameFont.render(str(player), True, white)
    LevelText = GameFont.render("lvl "+str(lvl), True, white)
    LivesText = GameFont.render("Lives:"+str(lives), True, white)
    GameOverText = GameFont.render("GAME OVER", True, white)
    
    window.blit(ScoreText, (screen_size[0]//2, 30))
    window.blit(NameText, (20, 30))
    window.blit(LevelText, (440, 30))
    window.blit(LivesText, (150, 30))
    
    if lives <= 0:
        window.blit(GameOverText, (screen_size[0]//2 - 70, screen_size[1]//2+50))
        if DiePlaying==0:
            die = pygame.mixer.Sound("Death.mp3")
            pygame.mixer.Sound.play(die)
            DiePlaying=1


def Collide(pad, padSpeed, ball):
    
    if ball.rect.colliderect(pad):
        ball.speed[1] = -ball.speed[1]
        ball.speed[0] += padSpeed

def drawBall():
    global white, location, screen_size, speed, score, ball, lives
    #If the ball hits the right edge of screen bounce.
    location[1] += speed[1]
    location[0] += speed[0]
    
    ball = pygame.draw.circle(window, white, location, radius, thickness)
    
    #If ball hits right side, bounce it
    if ball.right >= screen_size[0]:
        speed[0] = -speed[0]
    #If the ball hits the left side then bounce
    if ball.left <= 0:
        speed[0] = -speed[0]
    # If the ball hits the bottom of the screen
    if ball.bottom >= screen_size[1]:
        #speed[1] = -speed[1]
        print("bottom screen triggered")
        lives -= 1
        reset()
    # If the ball hits the top of the screen
    if ball.top <= 0:
        speed[1] = -speed[1]
        #print("top screen triggered")
        
    
    
def drawPaddleA():
    global blue, padA, aSpeed
    if padA.left <= 0 and aSpeed < 0:
        aSpeed = 0
    if padA.right >= screen_size[0] and aSpeed > 0:
        aSpeed = 0
    padA = padA.move(aSpeed, 0)
    padA = pygame.draw.rect(window, blue, padA)


class Block:
    def __init__(self, color, size, position, points, hits):
        self.color = color
        self.size = [100, 30]
        self.position = position
        self.points = points
        self.hits = hits
        self.rect = pygame.Rect(self.position, self.size)
    
    def drawBlock(self):
        pygame.draw.rect(window, self.color, self.rect)
        
    def collide(self, ball):
        global score
        
        if self.rect.colliderect(ball):
            self.hits -= 1
            score += self.points
            ball.speed[1] = -ball.speed[1]
            if self.hits == 0:
                return True
            else:
                return False
        else:
            return False

class SpeedBlock(Block):
    def __init__(self, position):
        Block.__init__(self, red, 100, position, 5, 1)
    
    def collide(self, ball):
        global score
        
        if self.rect.colliderect(ball):
            print("Hit SpeedBlock")
            score += self.points
            ball.speed[1] = -(ball.speed[1]-random.randint(1,2))
            return True
        else:
            return False

class MultiBall(Block):
    def __init__(self, position):
        Block.__init__(self, grey, 100, position, 10, 1)
    
    def collide(self, ball):
        global score
        
        if self.rect.colliderect(ball):
            print("Hit MultiBall")
            score += self.points
            ball.speed[1] = -ball.speed[1]
            
            #During Ball Spawn, location will be half way across the block and below the bottom
            aball = Ball(red, [self.position[0]+self.rect.width//2,self.position[1]+self.rect.height*2])
            #Ball Always goes straight down
            aball.speed = [0,2]
            balls.append(aball)
            
            return True
        else:
            return False

class Ball:
    def __init__(self, color, location):
        
        self.color = color
        self.location = location
        self.radius = 20
        self.speed = [0,0]
        self.thickness = 0
        self.rect = pygame.draw.circle(window, white, self.location, self.radius, self.thickness)

    def drawBall(self):
        global screen_size, score, lives
        #If the ball hits the right edge of screen bounce.
        self.location[1] += self.speed[1]
        self.location[0] += self.speed[0]
        
        self.rect = pygame.draw.circle(window, self.color, self.location, self.radius, self.thickness)
        
        #If ball hits right side, bounce it
        if self.rect.right >= screen_size[0]:
            self.speed[0] = -self.speed[0]
        #If the ball hits the left side then bounce
        if self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        # If the ball hits the bottom of the screen
        if self.rect.bottom >= screen_size[1]:
            #speed[1] = -speed[1]
            #print("bottom screen triggered")
            self.reset()
            lives -= 1
        # If the ball hits the top of the screen
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
            #print("top screen triggered")
    def reset(self):
        self.location = [screen_size[0]//2, screen_size[1]//2]
        self.speed = [0,0]
        if lives >= 2:
            boom = pygame.mixer.Sound("vineboombassboosted.mp3")
            pygame.mixer.Sound.play(boom)

timer = pygame.time.Clock()

screen_size = [600,800]
#This makes a window
window = pygame.display.set_mode(screen_size)

#sound Attributes

DiePlaying=0

#Ball Attributes
speed = [0, 0]
black = (0,0,0)
white = (255, 255, 255)
lightPurple = (150, 111, 214)
grey = (100, 100, 100)
red = (255, 0, 0)
radius = 20
location = [500, 300]
thickness = 0
BallSpeeds = [[0,1],[0,2],[0,3],[1,1], [1,2], [1,3], [-1, 1], [-1, 2], [-1, 3], [2, 1], [2, 2], [2, 3], [-2, 1], [-2, 2], [-2, 3]]

#PaddleA Attributes
aSpeed = 0
leftTop = [screen_size[0]//2, screen_size[1]-30]
widthHeight = [100, 30]
blue = (0, 0, 255)
padA = pygame.Rect(leftTop, widthHeight)

#PaddleB Attributes
bSpeed = 0
blue = (0, 0, 255)



#Scoring Attributes
#print(pygame.font.get_fonts())
pygame.font.init()
GameFont = pygame.font.SysFont("consolas", 30)
score = 0
lives = 3

ball1 = Ball(white, [screen_size[0]//2, screen_size[1]//2])
lvl=1
#Blocks
color_list = [red, blue, lightPurple]
blocks = []
balls = [ball1]
aBlock = MultiBall([0,200])
blocks.append(aBlock)
DisplayedInfo = 0

for j in range(3):
    for i in range(6):
        a_block = Block(random.choice(color_list), 100, [i*100, j*30], random.randint(1,3), random.randint(1,3))
        blocks.append(a_block)

for m in range(6):
    a_block = SpeedBlock([m*100, 90])
    blocks.append(a_block)
blocks2 = []

for i in range(6):
    blocks2.append(SpeedBlock([i*100,0]))
    
for j in range(6):
    blocks2.append(MultiBall([j*100, 30]))
    
for k in range(6):
    blocks2.append(Block(random.choice(color_list), 100, [k*100, 60], 1, 3))
    
player = input("What is your Name?")
conn = makeConn()
makeTable(conn)
HighList = findHighScores(conn)
startScreen = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pygame.mixer.init()
                theMusic = pygame.mixer.music.load("WiiShopMusic.mp3")
                pygame.mixer.music.play(-1)
                startScreen = False
            if event.key == pygame.K_RIGHT:
                if startScreen == False:
                    aSpeed = 4
                #print("Right")
            elif event.key == pygame.K_LEFT:
                if startScreen == False:
                    aSpeed = -4
            elif event.key == pygame.K_SPACE:
                #print("Pressed Space Bar")
                if startScreen == False:
                    if ball1.speed == [0,0]:
                        ball1.speed = random.choice(BallSpeeds)
                else:
                    DisplayedInfo += 1
                    if DisplayedInfo == 3:
                        DisplayedInfo = 0
            elif event.key == pygame.K_p:
                if startScreen == False:
                    storeData(conn)
                    print("Score Saved")
            elif event.key == pygame.K_o:
                retrieveData(conn)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                aSpeed = 0
        
    
    window.fill(black)
    #Is the ball colliding with the paddle?
    if startScreen == True:
        drawHighScoreScreen()
    else:
    
        for ball in balls:
            ball.drawBall()
            Collide(padA, aSpeed, ball)
        drawPaddleA()
        
        for block in blocks:
            block.drawBlock()
            #If collide returns true remove block from blocks list
            for ball in balls:
                if block.collide(ball):
                    blocks.remove(block)
                    if len(blocks) == 0:
                        lvl += 1
                        if lvl == 2:
                            blocks = blocks2
            
        drawScore()
    pygame.display.flip()
    timer.tick(60)
conn.close()
