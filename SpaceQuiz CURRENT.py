import pygame, sys, time, random, webbrowser
#from pygame.locals import *
pygame.mixer.init()
pygame.init()
pygame.display.set_caption('Space Shooter Quiz')
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

LaserSound = pygame.mixer.Sound("Laser.wav");
ExplosionSound = pygame.mixer.Sound("Explosion.wav");
CrashSound = pygame.mixer.Sound("Collision.wav");
#JetSound = pygame.mixer.Sound("Jet.wav");

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
gameendblue = (66,134,244)
gameendred = (216,53,13)

MaxLevel = 5; # Default 5
Level = 0;
Score = 0;
LScore = 0;
ScoreToLevel = 10; # Default 10
Health = 100;
EnemySpeed = 0.85;
playerSpeed = 0.5;

#Scenes
Menu = True
Play = False

Notification = False
GameEnded = False

Questions = [["Which bus transfers data and commands from external devices","Control"],
             ["Which Instruction Set requires less memory but uses complex hardware ","CISC"]]; # Example - Questions = [["What is 2+2","4"],["What is 5+5","10"]];
QuestionLives = 3;
Topic = "Computing" # Set the topic here

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
    PlayScores = StandardFontLarge.render("SCORES", 1, black)
    Description = StandardFontMedium.render("The Objective of this Game is to make it to the final level by shooting down alien ships", 1, white)
    Description2 = StandardFontMedium.render("You will be asked a question at the end of every level, and you will have 3 attempts to get it right", 1, white)
    Description3 = StandardFontMedium.render("When you answer correclty you will proceed to the next level. When you lose your score will be saved", 1, white)
    Description4 = StandardFontMedium.render("When you answer incorrectly, the correct answer will be revealed to you", 1, white)
    Description5 = StandardFontMedium.render("Your ship will heal itself upon every new level and the game will increase in difficulty", 1, white)
    PlayTitleRect = PlayTitle.get_rect()
    pygame.draw.rect(screen, white, (MenuPosX,(MenuPosY + 35), 200, 50)) # Play
    pygame.draw.rect(screen, white, (MenuPosX,(MenuPosY + 95), 200, 50)) # Settings

    # Render
    screen.blit(Title, (MenuPosX, MenuPosY))
    screen.blit(PlayTitle, ((MenuPosX + 5), (MenuPosY + 50)))
    screen.blit(PlayScores, ((MenuPosX + 5), (MenuPosY + 110)))
    screen.blit(Description, ((MenuPosX - 100 ), (MenuPosY + 200)))
    screen.blit(Description2, ((MenuPosX - 100 ), (MenuPosY + 215)))
    screen.blit(Description3, ((MenuPosX - 100 ), (MenuPosY + 230)))
    screen.blit(Description4, ((MenuPosX - 100 ), (MenuPosY + 245)))
    screen.blit(Description5, ((MenuPosX - 100 ), (MenuPosY + 260)))


def DrawGame():
    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, white, (int(star[0]),int(star[1])), 1, 1)
        
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
    TopicText = StandardFontLarge.render("Topic: " + Topic, 0, white)
        # Render Health
    HealthText = StandardFontLarge.render("HP", 0, white)
    pygame.draw.rect(screen, red, (420,265, 200, 20))
    pygame.draw.rect(screen, green, (420,265, (Health * 2), 20))

    screen.blit(TopicText, (420, 35))
    screen.blit(LevelText, (420, 95))
    screen.blit(ScoreText, (420, 135))
    screen.blit(HealthText, (420, 235))
    
def DrawNotification():
    global Notification
    # Draw Notification Background
    if(Notification == True):
       pygame.draw.rect(screen, white, (150,200,315,125));
       NotificationText = StandardFontLarge.render("Open the Python Shell", 0, red)
       screen.blit(NotificationText, (200,250))
    else:
       pass;

bullets = [];
enemies = [];
stars = [];

def GoToMenu():
    global Play;
    global Menu;
    Play = False; # Turn off the game graphics
    Menu = True; # Turn on the menu graphics
    ResetStats(); # Restart User stats

def Save():
    name = input("My name is ");
    if(len(name) > 10):
        print("Your name is too long");
        Save();
    file = open("scores.txt", "a")
    file.write("\n" + name + " scored " + str(Score) + "! " + name + " lost the game at Level " + str(Level) +"!")
    print("Your Score has been saved!");

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
    global Notification; # Use the global variable Notification
    global EnemySpeed;
    global playerSpeed;
    global Health;
    global Level
    Notification = True;
    print("Picking a random question...");
    questionLength = len(Questions) - 1; # Get the length of the array of questions
    questionArray = Questions[random.randint(0,questionLength)]; # Get a random question and its answer from the array of questions
    questionInput = input(questionArray[0]); # Ask the question to the player and save the response 

    if(questionInput.lower() == questionArray[1].lower()): # Convert the players answer to lowercase and the questions answer to lowercase and check if they match
        print("Well done! Proceed +3 Score \n"); # Tell the player the answer is correct
        Score += 3; # Award an extra 3 points
        if(Health < 75):
            Health+=25; # Heal the Player
        Notification = False;
        QuestionLives = 3; # Set the number of lives on a question to 3
        EnemySpeed += 0.1; # Increase difficulty
        playerSpeed += 0.1; # Balance the difficulty of the game
    else: #  If the answers do not match
        if(QuestionLives == 0): # If they have ran out of lives to answer the question
            #Play = False;
            print("GAME OVER! Thank you for revising! \n"); # Tell the player the game is over and
            Save();
            GoToMenu();
            Nofitication = False;
            ResetStats(); # Restart User stats
        else:
            QuestionLives -= 1; # Take away a life
            print("Oh no! You lose a life! " + str(QuestionLives) + " ❤ Left"); # Print how many lives left
            print("The correct answer was " + str(questionArray[1]) + " \n");
            AskQuestion(); # Ask the questiona gain (recursion)
        
def NoHealth():
    global QuestionLives; # Use the global variable QuestionLives
    global Score; # Use the global variable Score
    global Play; # Use the global variable Play
    global Menu; # Use the global variable Menu
    global Level;
    print("Your spaceship was destroyed! \nGAME OVER! Thank you for revising! \n"); # Tell the player the game is over and
    Save();
    GoToMenu();

def EndLevel():
    global GameEnded; # Check if the game has ended
    global Score; # Get the global player score
    if(GameEnded == False):
        print("The Game Has Ended! Enter your name to Save your Score")
        Save();
        GameEnded = True; # End the game
    pygame.draw.rect(screen, gameendblue, (50,150,315,425));
    NotificationText2 = StandardFontLarger.render("Game Completed!", 0, gameendred)
    NotificationText3 = StandardFontLarge.render("Your Final Score is " + str(Score) + "!", 0, gameendred)
    NotificationText3a = StandardFontLarge.render("Your Score has been saved!", 0, gameendred)
    NotificationText4 = StandardFontLarge.render("Thank you for playing", 0, gameendred)
    screen.blit(NotificationText2, (75,250))
    screen.blit(NotificationText3, (75,295))
    screen.blit(NotificationText3a, (75,325))
    screen.blit(NotificationText4, (75,465))

# Game Loop
while True:
    if(Menu == True):
        screen.fill(metro_black) # Clear Screen
        DrawMenu();
    if(Play == True):
        screen.fill(black) # Clear Screen
        DrawGame();
        DrawNotification();

        if(Health < 1):
            NoHealth(); # If the player loses all their HP, end the game
        
        # Level System
        if (Level != MaxLevel):
            if (LScore < ScoreToLevel): # Default ScoreToLevel is 15 score to level up
                EncounterChance = random.randint(1,850) #  Default encounter rate is 1 every 850 frames
                StarChance = random.randint(1,200) #  Default star spawn rate is 1 every 170 frames
                if(StarChance == 1): # If the star spawn has been chosen
                    StarXSpawn = random.randint(1, 395) # Store a random number along the X axis for the star to spawn at
                    stars.append([StarXSpawn, 0]);
                if(EncounterChance == 1): # If the enemy spawn has been chosen
                    XSpawn = random.randint(10, 350) # Store a random number along the X axis for the enemy to spawn at
                    enemies.append([XSpawn,0]) # Create an enemy with the random X position and Y position at 0
            else:
                AskQuestion(); # If the player has reached the next level then ask a question
                LScore = 0 # Reset the level score counter to 0
                Level += 1; # Proceed the player to the next level.
        if (Level == MaxLevel):
            EndLevel();
            
        #Enemy Control
        tempEnemies = [];
        enemyId = -1;
        for enemy in enemies:
            enemyId += 1;
            enemy[1] += EnemySpeed; # Enemy Speed
            #Collision Detection with Speeding Bullets
            for bullet in bullets:
                #print("Bulletx = " + str(bullet[0]) + "; BulletY = " + str(bullet[1]) + " |  EnemyX = " + str(enemy[0]) + "; EnemyY = " + str(enemy[1]));
                if (bullet[0] < (enemy[0] + 35)) and (bullet[0] > (enemy[0] - 25)):
                    if(bullet[1] < (enemy[1] + 30)) and (bullet[1] > (enemy[1] - 40)):
                        bullet[1] = -1; # Destroy it
                        enemy[1] = (ScreenHeight * 2); # Kill it
                        ExplosionSound.play()# Play Destruction Sound
                        Score += 1;
                        LScore += 1;
                        if(LScore == ScoreToLevel):
                            Notification = True;
                            DrawNotification();
            #Collision Detection with Player
            AlreadyHit = False;
            if(enemy[1] > playerY) and (enemy[1] < (playerY + 0.85)):
                if(enemy[0] > (playerX - 30)) and (enemy[0] < (playerX + 30)):
                    HPL = random.randint(1,30)
                    Health -= HPL;
                    CrashSound.play()
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

        #Star Control
        tempStars = [];
        starId = -1;
        for star in stars:
            starId += 1;
            star[1] += 0.0875;
            if star[1] > ScreenHeight:
                stars.pop(starId)
            else:
                tempStars.append([star[0],star[1]])
        stars = tempStars
        
        # Player Movement
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            if playerX < 330:
                playerX += playerSpeed;
        if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
            if playerX > 0:
                playerX -= playerSpeed;
    
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
            if (GlobalMouseX >= 160) and (GlobalMouseX <= 350) and (GlobalMouseY >= 250) and (GlobalMouseY <= 300):
                webbrowser.open("scores.txt")
        Blink();
        
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                LaserSound.play()
                if len(bullets) == 2: # Change the amount of bullets that should appear on the screen here
                    bullets.pop(0);
                    bullets.append([playerX,playerY]);
                else:
                    bullets.append([playerX,playerY]);
            
    screen.blit(MousePositionText, (10,10))
    pygame.display.flip()       

