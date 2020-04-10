import pygame
import pygame.gfxdraw
import random
import os

pygame.mixer.init()

pygame.init()


# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Creating window
screen_width = 900
screen_height = 600
line_width= 2 #border_width
gameWindow = pygame.display.set_mode((screen_width+line_width, screen_height+line_width))



# Game Title
pygame.display.set_caption("Snake Game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for i in range(len(snk_list)):
        if(i%2 ==0):
            pygame.gfxdraw.filled_circle(gameWindow, snk_list[i][0]+10, snk_list[i][1]+10, 15, color)
        else:
            pygame.gfxdraw.filled_circle(gameWindow, snk_list[i][0]+10, snk_list[i][1]+10, 15, white)

def welcome():
    exit_game = False
    pygame.mixer.music.load('Music/background.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)
    while not exit_game:
        gameWindow.fill((200,210,229))
        text_screen("Welcome to Snake Game", black, 260, 250)
        text_screen("Press Enter To Play", black, 300, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    gameloop()

        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    
    # Check if highscore file exists
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    target_x = random.randint(20, screen_width / 2)
    target_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60
    while not exit_game:
        if game_over:
            gameWindow.fill(white)
            if(score > int(highscore) ):
                with open("highscore.txt", "w") as f:
                    f.write(str(score))
                text_screen("Congratulations!!", red, 260, 170)
                text_screen("You have made a High Score", red, 180, 220)
                text_screen("Game Over! Press Enter To Continue", red, 120, 265)
            else:
                text_screen("Game Over! Press Enter To Continue", red, 100, 250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score +=10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - target_x)<6 and abs(snake_y - target_y)<6:
                score +=10
                pygame.mixer.music.load('Music/eating.mp3')
                pygame.mixer.music.play()
                target_x = random.randint(20, screen_width / 2)
                target_y = random.randint(20, screen_height / 2)
                snk_length +=5

            gameWindow.fill(white)
            # top line
            pygame.draw.rect(gameWindow, red, [0,0,screen_width,line_width])
            # bottom line
            pygame.draw.rect(gameWindow, red, [0,screen_height,screen_width,line_width])
            # left line
            pygame.draw.rect(gameWindow, red, [0,0,line_width, screen_height])
            # right line
            pygame.draw.rect(gameWindow, red, [screen_width,0,line_width, screen_height+line_width])
            #Showing Score and HighScore on Game window
            font1 = pygame.font.SysFont(None, 35)
            screen_text = font1.render("Your Score: " + str(score) + "  Highscore: "+str(highscore), True, red)
            gameWindow.blit(screen_text, [5,5])
            
            pygame.gfxdraw.filled_circle(gameWindow, target_x, target_y, 15, red)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            print("head:",head)
            print(snk_list)
            snk_list.insert(0,head)
            print(snk_list)
            if len(snk_list)>snk_length:
                del snk_list[-1]

            if head in snk_list[1:]:
                game_over = True
                pygame.mixer.music.load('Music/background.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.1)            
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('Music/background.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.1)
                
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()
