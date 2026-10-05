import pygame
import random
pygame.init()
pygame.display.set_caption("Dodge Game")

# Set up display and load game assets
screen = pygame.display.set_mode((600,400))

# Player assets
player_image = pygame.image.load("game_devs/assets/blue_body_circle.png").convert_alpha()
player_image = pygame.transform.scale(player_image,(40,40))

player_face = pygame.image.load("game_devs/assets/face_a.png").convert_alpha()
player_face = pygame.transform.smoothscale(player_face,(27,27))

player_hand = pygame.image.load("game_devs/assets/blue_hand_closed.png").convert_alpha()

player_hand = pygame.transform.smoothscale(player_hand, (20,20))

left_hand = pygame.transform.rotate(player_hand, 180)
right_hand = pygame.transform.flip(player_hand, True, False)
right_hand = pygame.transform.rotate(right_hand, 180)

# Red enemy assets
enemy_image = pygame.image.load("game_devs/assets/red_body_square.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (40,40))

enemy_face = pygame.image.load("game_devs/assets/face_g.png").convert_alpha()
enemy_face = pygame.transform.smoothscale(enemy_face, (27,27))

enemy_hand = pygame.image.load("game_devs/assets/red_hand_closed.png").convert_alpha()
enemy_hand = pygame.transform.smoothscale(enemy_hand, (20,20))

enemy_left_hand = pygame.transform.rotate(enemy_hand, 180)

enemy_right_hand = pygame.transform.flip(enemy_hand, True, False)
enemy_right_hand = pygame.transform.rotate(enemy_right_hand,180)

# Yellow enemy assets
enemy2_image = pygame.image.load("game_devs/assets/yellow_body_rhombus.png").convert_alpha()
enemy2_image = pygame.transform.scale(enemy2_image, (40,40))

enemy2_face = pygame.image.load("game_devs/assets/face_b.png").convert_alpha()
enemy2_face = pygame.transform.smoothscale(enemy2_face, (27,27))

enemy2_hand = pygame.image.load("game_devs/assets/hand_yellow_closed.png").convert_alpha()
enemy2_hand = pygame.transform.smoothscale(enemy2_hand, (20,20))

enemy2_left_hand = pygame.transform.rotate(enemy2_hand, 180)

enemy2_right_hand = pygame.transform.flip(enemy2_hand, True, False)
enemy2_right_hand = pygame.transform.rotate(enemy2_right_hand, 180)

# Background asset
background = pygame.image.load("game_devs/assets/background.jpg").convert()
background = pygame.transform.scale(background, (600,400))

# Game objects
player = pygame.Rect(280,240,40,40)
enemy = pygame.Rect(100,0,40,40)
enemy2 = pygame.Rect(400,0,40,40)

# Game utilities
framerate = pygame.time.Clock()
font = pygame.font.Font(None,36)
game_over_font = pygame.font.Font(None,60)
restart_font = pygame.font.Font(None,36)

# Gameplay settings
enemy_speed = 4
enemy2_speed = 6
enemy2_horizontal_direction = 1
enemy2_horizontal_speed = 3
enemy_horizontal_direction = 1
enemy_horizontal_speed = 2
enemy_direction_timer = 0
player_speed = 5

# Game state and score
running = True
game_state = "start"
score = 0
high_score = 0
start_time = pygame.time.get_ticks()
speed_up_message_time = 0
previous_score = 0

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "start" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_state = "playing"
                start_time = pygame.time.get_ticks()

        if game_state == "game_over" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_state = "playing"
                previous_score = 0
                speed_up_message_time = 0
                score = 0
                player.x = 280
                player.y = 240
                enemy.x = 100
                enemy.y = 0
                enemy2.x = 400
                enemy2.y = 0
                enemy_speed = 4
                enemy2_speed = 6
                enemy2_horizontal_direction = 1
                enemy2_horizontal_speed = 3
                enemy_horizontal_speed = 2
                enemy_direction_timer = 0
                start_time = pygame.time.get_ticks()
    # Gameplay logic
    if game_state == "playing":
        score = (pygame.time.get_ticks() - start_time) // 1000

        if score != previous_score:
            if score == 5 or score == 10:
                speed_up_message_time = pygame.time.get_ticks()

            previous_score = score

        if score > high_score:
            high_score = score

        # Increase difficulty at certain score milestones
        if score >= 10:
            enemy_speed = 9
            enemy2_speed = 10
            enemy2_horizontal_speed = 5
            enemy_horizontal_speed = 4

        elif score >= 5:
            enemy_speed = 6
            enemy2_speed = 8
            enemy2_horizontal_speed = 4
            enemy_horizontal_speed = 3

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed

        if player.left < 0:
            player.left = 0

        if player.right > 600:
            player.right = 600

        enemy.y += enemy_speed
        enemy.x += enemy_horizontal_direction * enemy_horizontal_speed
        enemy_direction_timer += 1

        if enemy_direction_timer >= 60:
            enemy_direction_timer = 0

            if random.randint(1,2) == 1:
                enemy_horizontal_direction *= -1

        if enemy.left < 0:
            enemy.left = 0

        if enemy.right > 600:
            enemy.right = 600

        if enemy.y > 400:
            enemy.y = 0
            enemy.x = random.randint(0,560)
            enemy_horizontal_direction = random.choice([-1, 1])

        enemy2.y += enemy2_speed
        

        if enemy2_horizontal_direction == 1:
            enemy2.x += enemy2_horizontal_speed
        
        else:
            enemy2.x -= enemy2_horizontal_speed

        if enemy2.right > 600:
            enemy2_horizontal_direction = -1

        if enemy2.left < 0:
            enemy2_horizontal_direction = 1

        if enemy2.y > 400:
            enemy2.y = 0
            enemy2.x = random.randint(0,560)
            enemy2_horizontal_direction = random.choice([-1,1])

            while abs(enemy2.x - enemy.x) < 100:
                enemy2.x = random.randint(0,560)

        if player.colliderect(enemy) or player.colliderect(enemy2):
            game_state = "game_over"
    # Draw game
    screen.blit(background, (0,0))

    # Draw characters
    if game_state != "start":
        screen.blit(player_image,player)
        screen.blit(player_face, (player.x + 7, player.y + 7))
        screen.blit(left_hand, (player.x -22, player.y + 15))
        screen.blit(right_hand, (player.x + 42, player.y + 15))
        
        
        screen.blit(enemy_image, enemy)
        screen.blit(enemy_face, (enemy.x + 7, enemy.y + 7))
        screen.blit(enemy_left_hand, (enemy.x - 22, enemy.y + 15))
        screen.blit(enemy_right_hand, (enemy.x + 42, enemy.y + 15))
        screen.blit(enemy2_image, enemy2)
        screen.blit(enemy2_face, (enemy2.x + 7, enemy2.y + 7))
        screen.blit(enemy2_left_hand, (enemy2.x - 22, enemy2.y + 15))
        screen.blit(enemy2_right_hand, (enemy2.x + 42, enemy2.y + 15))

    # Draw start screen
    if game_state == "start":
        start_text = game_over_font.render("Dodge Game",True,(255,255,255))
        screen.blit(start_text,(200,120))

        start_prompt = restart_font.render("Press SPACE to Start", True,(255,255,255))
        screen.blit(start_prompt,(185,190))

    # Draw score
    score_text = font.render(f"Score: {score}",True,(255,255,255))
    screen.blit(score_text,(10,10))

    # Draw high score
    high_score_text = font.render(f"High Score: {high_score}",True,(255,255,255))
    screen.blit(high_score_text,(10,45))

    # Draw speed-up notification
    if speed_up_message_time > 0:
        if pygame.time.get_ticks() - speed_up_message_time < 1000:
            speed_up_text = font.render("SPEED UP!", True,(255,255,255))
            speed_up_rect = speed_up_text.get_rect(center=screen.get_rect().center)
            screen.blit(speed_up_text, speed_up_rect)

    # Draw game-over screen
    if game_state == "game_over":
        game_over_text = game_over_font.render("Game Over", True, (255,255,255))
        screen.blit(game_over_text,(200,150))

        final_score_text = restart_font.render(f"Score: {score}",True,(255,255,255))
        screen.blit(final_score_text,(250,210))

        restart_text = restart_font.render("Press R to Restart", True, (255,255,255))
        screen.blit(restart_text,(205,250))

    # Update display
    pygame.display.flip()
    framerate.tick(60)

pygame.quit()