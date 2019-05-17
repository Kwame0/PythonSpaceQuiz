import pygame, sys, time, random
#from pygame.locals import *
pygame.init()
ScreenWidth = 640; # ScreenWidth & Height must remain the same
ScreenHeight = 720; #
#pygame.display.set_caption("Disinfo Machine") # Title
screen = pygame.display.set_mode((ScreenWidth,ScreenHeight)) # Set the Screen
events = pygame.event.get() # Set the events to check whats going on
playerX = 160 # Starting PlayerX
playerY = 600 # Const PlayerY

## Global Variables
GlobalMouseX = 0;
GlobalMouseY = 0;

pink = (255,200,200)
white = (255,255,255)
black = (0,0,0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
metro_black = (61,61,61)
nice_green = (11,135,0)
green = (0,255,0)
blood_red = (135, 20, 0)
red = (255,0,0)

MaxLevel = 5;
Level = 0;
Score = 0;
LScore = 0;
Health = 100;

#Scenes
Menu = True
Play = False
EndGame = False

Questions = [["Which bus transfers data and commands from external devices","Control"],
             ["Which Instruction Set requires less memory but uses complex hardware ","CISC"]]; # Example - Questions = [["What is 2+2","4"],["What is 5+5","10"]];
QuestionLives = 3;
Topic = "Computing" # Set the topic here
Name = "Not Set"

## Set Colors
StandardFontLarger = pygame.font.SysFont('Booksman', 45)
StandardFontLarge = pygame.font.SysFont('Booksman', 30)
StandardFontMedium = pygame.font.SysFont('Booksman', 18)
StandardFontSmall = pygame.font.SysFont('Booksman', 12)


def Blink():
   pygame.draw.rect(screen, green, ((GlobalMouseX - 5), (GlobalMouseY - 5), 15, 15))

def DrawMenu():
    MenuPosX = ScreenWidth / 4
    MenuPosY = ScreenWidth / 4
    
    # Create
    Title = StandardFontLarger.render("M E N U", 0, white)
    PlayTitle = StandardFontLarge.render("PLAY", 0, black)
    PlayTitleRect = PlayTitle.get_rect()
    pygame.draw.rect(screen, white, (MenuPosX,(MenuPosY + 35), 200, 50)) # Play
    pygame.draw.rect(screen, white, (MenuPosX,(MenuPosY + 95), 200, 50)) # Settings

    # Render
    screen.blit(Title, (MenuPosX, MenuPosY))
    screen.blit(PlayTitle, (MenuPosX, (MenuPosY + 45)))

def DrawGame():
    # Draw Player
    pygame.draw.rect(screen, white, (playerX, playerY, 70, 15))
    pygame.draw.rect(screen, white, ((playerX + 10), (playerY - 20), 10, 20))
    pygame.draw.rect(screen, white, ((playerX + 45), (playerY - 20), 10, 20))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, cyan, (bullet[0], bullet[1], 10, 10))

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, blood_red, (enemy[0], enemy[1], 15, 60))
        pygame.draw.rect(screen, blood_red, (enemy[0] - 10, enemy[1] - 25, 10, 45))
        pygame.draw.rect(screen, blood_red, (enemy[0] + 15, enemy[1] - 25, 10, 45))
    
    # Draw Information Board
    pygame.draw.rect(screen, metro_black, (400,0, 240, 720))
    LevelText = StandardFontLarge.render("Level: " + str(Level), 0, white)
    ScoreText = StandardFontLarge.render("Score: " + str(Score), 0, white)
    NameText = StandardFontLarge.render("Name: " + Name, 0, white)
    TopicText = StandardFontLarge.render("Topic: " + Topic, 0, white)
        # Render Health
    HealthText = StandardFontLarge.render("HP", 0, white)
    pygame.draw.rect(screen, red, (420,265, 200, 20))
    pygame.draw.rect(screen, green, (420,265, (Health * 2), 20))

    screen.blit(TopicText, (420, 35))
    screen.blit(LevelText, (420, 95))
    screen.blit(ScoreText, (420, 135))
    screen.blit(NameText, (420, 175))
    screen.blit(HealthText, (420, 235))
'''
def DrawEnd():
    # Draw Game Over Scene
    pygame.draw.rect(screen, metro_black, (0,0, 640, 720))
    GameOverText = StandardFontLarger.render("Game Over", 0, white)

    screen.blit(GameOverText, (300, 100))'''

bullets = [];
enemies = [];

def ResetStats():
    global Level # Use the global variable Level
    global Score # Use the global variable Score
    global LScore # Use the global variable Level Score
    global Health # Use the global variable Health
    global playerX  # Use the global variable playerX
    Level = 0; # Set the current Level to 0
    Score = 0; # Set the current Score to 0
    LScore = 0; # Set the LevelScore to 0
    Health = 100; # Set the Health to default 100
    playerX = 160; # Set the player position to default

def AskQuestion():
    global QuestionLives; # Use the global variable QuestionLives
    global Score; # Use the global variable Score
    global Play; # Use the global variable Play
    global Menu; # Use the global variable Menu
    print("Picking a random question...");
    questionLength = len(Questions) - 1; # Get the length of the array of questions
    questionArray = Questions[random.randint(0,questionLength)]; # Get a random question and its answer from the array of questions
    questionInput = input(questionArray[0]); # Ask the question to the player and save the response 

    if(questionInput.lower() == questionArray[1].lower()): # Convert the players answer to lowercase and the questions answer to lowercase and check if they match
        print("Well done! Proceed +3 Score \n"); # Tell the player the answer is correct
        Score += 3; # Award an extra 3 points
        QuestionLives = 3; # Set the number of lives on a question to 3
    else: #  If the answers do not match
        if(QuestionLives == 0): # If they have ran out of lives to answer the question
            #Play = False;
            #EndGame = True;
            print("GAME OVER! Thank you for revising! \n"); # Tell the player the game is over and
            Play = False; # Turn off the game graphics
            Menu = True; # Turn on the menu graphics
            ResetStats(); # Restart User stats
        else:
            QuestionLives -= 1; # Take away a life
            print("Oh no! You lose a life! " + str(QuestionLives) + " ❤ Left \n"); # Print how many lives left
            AskQuestion(); # Ask the questiona gain (recursion)
        
    

class test():
    one = 1;
    two = 2;

    def __init__(self, one, two):
        self.one = one
        self.two =  two


# Game Loop
while True:
    if(Menu == True):
        screen.fill(metro_black) # Clear Screen
        DrawMenu();
    if(Play == True):
        screen.fill(black) # Clear Screen
        DrawGame();

        # Level System | Under Work
        if (Level != MaxLevel):
            if (LScore < 15): # Default is 15 score to level up
                EncounterChance = random.randint(1,851) #  Default encounter rate is 1 every 851 frames
                if(EncounterChance == 1): # If the enemy spawn has been chosen
                    XSpawn = random.randint(10, 350) # Store a random number along the X axis for the enemy to spawn at
                    enemies.append([XSpawn,0]) # Create an enemy with the random X position and Y position at 0
            else:
                AskQuestion(); # If the player has reached the next level then ask a question
                LScore = 0 # Reset the level score counter to 0
                Level += 1; # Proceed the player to the next level.
        '''if(Level == 1) and (Score < 10):
            EncounterChance = random.randint(1,851)
            if(EncounterChance == 1):
                XSpawn = random.randint(10, 350)
                enemies.append([XSpawn,0])'''

        
        #Enemy Control
        tempEnemies = [];
        enemyId = -1;
        for enemy in enemies:
            enemyId += 1;
            enemy[1] += 0.85; # Enemy Speed
            #Collision Detection with Speeding Bullets
            for bullet in bullets:
                #print("Bulletx = " + str(bullet[0]) + "; BulletY = " + str(bullet[1]) + " |  EnemyX = " + str(enemy[0]) + "; EnemyY = " + str(enemy[1]));
                if (bullet[0] < (enemy[0] + 35)) and (bullet[0] > (enemy[0] - 25)):
                    if(bullet[1] < (enemy[1] + 30)) and (bullet[1] > (enemy[1] - 40)):
                        bullet[1] = -1; # Destroy it
                        enemy[1] = (ScreenHeight * 2); # Kill it
                        Score += 1;
                        LScore += 1;
            #Collision Detection with Player
            AlreadyHit = False;
            if(enemy[1] > playerY) and (enemy[1] < (playerY + 0.85)):
                if(enemy[0] > (playerX - 30)) and (enemy[0] < (playerX + 30)):
                    Health -= 20;
            if enemy[1] > ScreenHeight:
                enemies.pop(enemyId)
            else:
                tempEnemies.append([enemy[0],enemy[1]])
                    
        #Bullet Control
        tempBullets = []
        bulletId = -1;
        for bullet in bullets:
            bulletId += 1;
            bullet[1] -= 1; # Bullet Speed
            if bullet[1] < 0:
                bullet.pop(bulletId);
            else:
                tempBullets.append([bullet[0],bullet[1]])
        bullets = tempBullets;
        
        # Player Movement
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_d]:
            if playerX < 330:
                playerX += 0.5;
        if pressed[pygame.K_a]:
            if playerX > 0:
                playerX -= 0.5;
    
    mouseX, mouseY = pygame.mouse.get_pos()
    
    GlobalMouseX = mouseX
    GlobalMouseY = mouseY
    MousePositionText = StandardFontMedium.render("X: " + str(GlobalMouseX) + " Y: " + str(GlobalMouseY), 1, white)
    pygame.draw.rect(screen, red, ((GlobalMouseX - 5), (GlobalMouseY - 5), 15, 15))

    ms = pygame.mouse.get_pressed()
    if ms[0]:
        if Menu == True:
            if (GlobalMouseX >= 160) and (GlobalMouseX <= 350) and (GlobalMouseY >= 195) and (GlobalMouseY <= 245):
                Menu = False;
                Play = True;
                Level = 1;
        Blink();
        
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(bullets) == 2: # Change the amount of bullets that should appear on the screen here
                    bullets.pop(0);
                    bullets.append([playerX,playerY]);
                else:
                    bullets.append([playerX,playerY]);
                #print(bullets); #debug
            
    screen.blit(MousePositionText, (10,10))
    #print("Debugging |" + str(q1.backgroundColor) + " |" + str(q1.invertButtons) + " |" + str(q1.images) + " |");
    pygame.display.flip()       

