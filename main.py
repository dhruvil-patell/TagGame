# Importing and Initializing PyGame Libary
import pygame
import time
import random
pygame.init()

# Creating The Screen Using PyGame
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dhruvils Game")
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (screen_width, screen_height))


# Creating Players 
player_width = 30
player_height = 35
player = pygame.image.load("player.png").convert_alpha()
player = pygame.transform.scale(player, (player_width, player_height))
player2 = pygame.image.load("player2.png").convert_alpha()
player2 = pygame.transform.scale(player2, (player_width, player_height))

    # This to make it easier for the flipping of sprites when different keys clicked
def character(picture_name): 
    character = pygame.image.load(picture_name).convert_alpha()
    character = pygame.transform.scale(character, (player_width, player_height))
    return character


# Game Aspects
score_player1 = 0
score_player2 = 0
tag = 0

bonus_active = True
bonus2_active = True
starting = True
bones_x = random.randint(100, 700)
time_elapsed = 0


# Player Movment
groundLevel = 380 - player_height
x = 0
x2 = 300
y = groundLevel
y2 = groundLevel

gravity = 1 
gravity2 = 1      

player1_jump_strength = 15
player2_jump_strength = 15
player1_speed = 6
player2_speed = 6  

y_velocity = 0
y_velocity2 = 0

start_time = time.time()
last_collision_time = 0  

Jumping = False
Jumping2 = False



# Tagging game variables
current_tagger = 1  
round_duration = 30 
round_start_time = time.time()


# Creating & Drawing Platforms
def platform(x, y, width):
    r = pygame.Rect(x, y, width, 10)
    return r
def draw(r, red, green, blue):
    pygame.draw.rect(screen, (red, green, blue), r)
def create_map(*platforms):
    return list(platforms)


# keeping the players inside the screen
def inside(x, x2):
    if x < 0:
        x = 0
    if x >= screen_width:
        x = 780
    if x2 < 0:
        x2 = 0 
    if x2 >= screen_width:
        x2 = 780
    return x, x2

# Different Maps
map1 = create_map(platform(200, 300, 100), platform(400, 250, 100), platform(600, 200, 100), platform(360, 150, 100))
map2 = create_map(platform(300, 300, 100), platform(400, 150, 100), platform(600, 250, 100), platform(200, 160, 100))
map3 = create_map(platform(random.randint(0, 100), random.randint(220, 350), 100), platform(random.randint(200, 300), random.randint(150, 300), 100), platform(random.randint(400, 500), random.randint(100, 250), 100), platform(random.randint(600, 700), random.randint(180, 320), 100))
map4 = create_map(platform(200, 300, 100), platform(300, 250, 100), platform(600, 250, 50), platform(360, 150, 200))
map5 = create_map(platform(300, 300, 100), platform(360, 160, 100), platform(600, 200, 50), platform(150, 250, 100), platform(450, 260, 100), platform(600, 130, 100))
map_selection = map1

# Extra Extra
clock = pygame.time.Clock()
font = pygame.font.Font("font.ttf", 40) 
font2 = pygame.font.Font("font.ttf", 20) 

powerup_sound = pygame.mixer.Sound("powerUp.wav")
switch_sound = pygame.mixer.Sound("switchPlayer.wav")
tagged_sound = pygame.mixer.Sound("hitHurt.wav")
ending_sound = pygame.mixer.Sound("endingSound.mp3")

pygame.mixer.music.load("backgroundMusic.wav")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

# Adding Background To Screen
    screen.blit(background, (0, 0))
    ground = pygame.Rect(0, 380, screen_width, 20)
    pygame.draw.rect(screen, (0, 233, 136), ground)


# Picking The Map & Drawing It On To The Screen
    if keys[pygame.K_1]:
        map_selection = map1
    if keys[pygame.K_2]:
        map_selection = map2
    if keys[pygame.K_3]:
        map3 = create_map(platform(random.randint(0, 700), random.randint(100, 370), 100), platform(random.randint(0, 700), random.randint(100, 370), 100), platform(random.randint(0, 700), random.randint(100, 370), 100), platform(random.randint(0, 700), random.randint(100, 370), 100))
        map_selection = map3   
    if keys[pygame.K_4]:
        map_selection = map4
    if keys[pygame.K_5]:
        map_selection = map5
     
    if map_selection == map1:
        for obj in map1:
            draw(obj, 150, 75, 0)
    elif map_selection == map2:
        for obj in map2:
            draw(obj, 150, 75, 0)
    elif map_selection == map3:
        for obj in map3:
            draw(obj, 150, 75, 0)
    elif map_selection == map4:
        for obj in map4:
            draw(obj, 150, 75, 0)
    elif map_selection == map5:
        for obj in map5:
            draw(obj, 150, 75, 0)
    
# Input Handling
    if keys[pygame.K_LEFT]:
        x -= player1_speed
        player = character("player_flipped.png")
    if keys[pygame.K_RIGHT]:
        x +=  player1_speed
        player = character("player.png")
    if keys[pygame.K_UP] and Jumping == False:
        y_velocity = -player1_jump_strength
        Jumping = True
    
    if keys[pygame.K_a]:
        x2 -= player2_speed
        player2 = character("player2.png")
    if keys[pygame.K_d]:
        x2 += player2_speed
        player2 = character("player2_flipped.png")
    if keys[pygame.K_w] and Jumping2 == False:
        y_velocity2 =- player2_jump_strength
        Jumping2 = True
    
    x, x2 = inside(x, x2)

    player_hitbox = pygame.Rect(x, y, player_width, player_height)
    player2_hitbox = pygame.Rect(x2, y2, player_width, player_height)                                                    
    screen.blit(player, (x, y))
    screen.blit(player2, (x2, y2))


# Gravity
    y_velocity += gravity
    y += y_velocity
    if y > groundLevel:
        y = groundLevel
        Jumping = False
        y_velocity = 0

    y_velocity2 += gravity2
    y2 += y_velocity2
    if y2 > groundLevel:
        y2 = groundLevel
        Jumping2 = False
        y_velocity2 = 0
     
    for obj in map_selection:
        if player_hitbox.colliderect(obj):
            if player_hitbox.centery < obj.centery:
                y = obj.top - player_height
                Jumping = False
            else:
                y = obj.bottom
            y_velocity = 0

        if player2_hitbox.colliderect(obj):
            if player2_hitbox.centery < obj.centery:
                y2 = obj.top - player_height
                Jumping2 = False
            else:
                y2 = obj.bottom
            y_velocity2 = 0


# Score System Keeping Track of Time and Score
    if player_hitbox.colliderect(player2_hitbox):
        current_time = time.time()
        if current_time - last_collision_time > 1.0:
            tagged_sound.play()
            if current_tagger == 1:
                score_player1 += 1
            else:
                score_player2 += 1
            print(f"Player {current_tagger} scored! P1: {score_player1} P2: {score_player2}")
            last_collision_time = current_time
    if starting == False:
        time_elapsed = time.time() - round_start_time
    elif starting:
        round_start_time = round_duration

    

    if time_elapsed >= round_duration:
        current_tagger = 2 if current_tagger == 1 else 1
        round_start_time = time.time()
        switch_sound.play()
        print(f"Time's up! Now Player {current_tagger}'s turn to tag!")


    time_left = (max(0, int(round_duration - time_elapsed)))
    timer_text = (f"Player {current_tagger}'s turn - Time {time_left}s")
    score_text = (f"P1 {score_player1}  P2 {score_player2}")

    timer_surface = font.render(timer_text, True, (255, 255, 255))
    score_surface = font.render(score_text, True, (255, 255, 255))
    screen.blit(timer_surface, (10, 10))
    screen.blit(score_surface, (10, 50))
    

# Bonuses
    if score_player1 >= 5 or score_player2 >= 5:
        if bonus_active:
            bonuses = pygame.Rect(bones_x, 360, 20, 20)
            pygame.draw.rect(screen, (255, 247, 107), bonuses)
            if player_hitbox.colliderect(bonuses):
                player1_speed += 1
                player1_jump_strength += 2
                screen.blit(background, bonuses, bonuses)
                powerup_sound.play()
                bonus_active = False
            if player2_hitbox.colliderect(bonuses):
                player2_speed += 1
                player2_jump_strength += 2
                screen.blit(background, bonuses, bonuses)
                powerup_sound.play()
                bonus_active = False


# End Game
    if score_player1 >= 15:
        finish_text = ("Player 1 WINS")
        finish_surface = font.render(finish_text, True, (255, 255, 255))
        screen.blit(finish_surface, (screen_width // 2 - finish_surface.get_width() // 2, screen_height // 2 - finish_surface.get_height() // 2))
        pygame.display.update()
        ending_sound.play()
        time.sleep(5)  
        running = False

    elif score_player2 >= 15:
        finish_text = ("Player 2 WINS")
        finish_surface = font.render(finish_text, True, (255, 255, 255))
        screen.blit(finish_surface, (screen_width // 2 - finish_surface.get_width() // 2, screen_height // 2 - finish_surface.get_height() // 2))
        pygame.display.update()
        ending_sound.play()
        time.sleep(5)  
        running = False


    # Starting Screen
    if starting:
        starting_screen = pygame.Rect(0, 0, screen_width, screen_height)
        pygame.draw.rect(screen, (34, 33, 143), starting_screen)
        instructions_text = ("""Press 'S' To Start The Game""")
        instructions_surface = font2.render(instructions_text, True, (255, 105, 31))
        screen.blit(instructions_surface, (290, 180))
        if keys[pygame.K_s]:
            starting = False
    if keys[pygame.K_0]:
        instructions = pygame.Rect(30, 30, screen_width-60, screen_height - 60)
        pygame.draw.rect(screen, (255, 51, 119), instructions)
        
        instructions_text = ("""1. Press 'S' To Start
2. Used WAD To Move Player 2
3. Use Arrow Keys To Move Player 1
4. Yellow Cubes Can Be Used As A
   Power-Up Improve speed and Jump
5. Bell Rings The Other Players Turn
6. First One To 15 Points Wins
7. Rerun to Play Again
8. Use Number Keys To Change Map
9. Use 3 For A Random Map - Doesnt Work
   The Best""")
        instructions_surface = font2.render(instructions_text, True, (255, 255, 255))
        screen.blit(instructions_surface, (40, 40))




    clock.tick(60)

    pygame.display.update()
