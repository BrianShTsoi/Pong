import pygame, sys, random

def launch_ball():
    global ball_rect, velocity_x, velocity_y, ai1_destination, ai2_destination
    ball_rect.center = (384, random.randint(50, 718))
    velocity_x = random.choice([random.randint(velocity_var, velocity_var*2), -random.randint(velocity_var, velocity_var*2)])
    velocity_y = random.randint(-velocity_var, velocity_var)
    if velocity_x > 0:
        ai1_destination = 384
        ai2_destination = None
    else:
        ai1_destination = None
        ai2_destination = 384

def display_score():
    score_L_surface = game_font.render(str(player_L_score), True, (255, 255, 255))
    score_L_rect = score_L_surface.get_rect(center = (192, 150))
    screen.blit(score_L_surface, score_L_rect)
    score_R_surface = game_font.render(str(player_R_score), True, (255, 255, 255))
    score_R_rect = score_R_surface.get_rect(center = (576, 150))
    screen.blit(score_R_surface, score_R_rect)

def end_display():
    end_surface = game_font.render('END', True, (255, 255, 255))
    end_rect = end_surface.get_rect(center = (384, 384))
    screen.blit(end_surface, end_rect)
    restart_surface = game_small_font.render('RESTART WITH SPACEBAR', True, (255, 255, 255))
    restart_rect = restart_surface.get_rect(center = (384, 618))
    screen.blit(restart_surface, restart_rect)


pygame.init()
screen = pygame.display.set_mode((768, 768))
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 1)
game_font = pygame.font.SysFont(None, 150)
game_small_font = pygame.font.SysFont(None, 50)

# Game Variables

game_active = True
player_L_score = 0
player_R_score = 0

winning_score = 100
velocity_var = 4
#velocity after collision
velocity_var2 = 10
paddle_speed  = 7
collide_force = 1

velocity_x = 0
velocity_y = 0

ai1_destination = None
ai2_destination = None

bg_surface = pygame.Surface((768, 768))
pygame.draw.line(bg_surface, (255, 255, 255), (384, 0), (384, 768))

ball_surface = pygame.Surface((10, 10))
ball_surface.fill((255, 255, 255))
ball_rect = ball_surface.get_rect(center = (384, random.randint(0, 768)))

paddle1_surface = pygame.Surface((11, 45))
paddle1_surface.fill((255, 255, 255))
paddle1_rect = paddle1_surface.get_rect(center = (0, 384))

paddle2_surface = pygame.Surface((11, 45))
paddle2_surface.fill((255, 255, 255))
paddle2_rect = paddle1_surface.get_rect(center = (768, 384))

#Prelaunch ball to set position, velocity and no destination
launch_ball()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Paddle movement and restart
        if event.type == pygame.KEYDOWN :
            keys_pressed = pygame.key.get_pressed()
#            if keys_pressed[pygame.K_DOWN] and paddle1_rect.centery < 768:
#                paddle1_rect.centery += 1
#            if keys_pressed[pygame.K_UP] and paddle1_rect.centery > 0:
#                paddle1_rect.centery -= 1
#            if keys_pressed[pygame.K_s] and paddle2_rect.centery < 768:
#                paddle2_rect.centery += 1
#            if keys_pressed[pygame.K_w] and paddle2_rect.centery > 0:
#                paddle2_rect.centery -= 1
            if keys_pressed[pygame.K_SPACE] and not game_active:
                player_L_score = 0
                player_R_score = 0
                game_active = True


    screen.blit(bg_surface, (0, 0))
    screen.blit(paddle1_surface, paddle1_rect)
    screen.blit(paddle2_surface, paddle2_rect)

    if game_active:
        #Move ball
        ball_rect.centerx += velocity_x
        ball_rect.centery += velocity_y 
        screen.blit(ball_surface, ball_rect)

        #Scoring
        if ball_rect.centerx < -150:
            player_R_score += 1
            launch_ball()

        if ball_rect.centerx > 918:
            player_L_score += 1
            launch_ball()

        #Ball reflection
        if ball_rect.centery < 0 or ball_rect.centery > 768:
            velocity_y *= -1

        #ai1 destination calculation
        if velocity_x < 0 and ai1_destination == None:
            ball_rect_copy = ball_rect.copy()
            velocity_x_copy, velocity_y_copy = velocity_x, velocity_y
            while ball_rect_copy.centerx > 10:
                ball_rect_copy.centerx += velocity_x_copy
                ball_rect_copy.centery += velocity_y_copy
                if ball_rect_copy.centery < 0 or ball_rect_copy.centery > 768:
                    velocity_y_copy *= -1
            ai1_destination = ball_rect_copy.centery 

        #ai1 moving to destination
        if ai1_destination != None:
            if ai1_destination < paddle1_rect.centery and paddle1_rect.centery > 0:
                paddle1_rect.centery -= paddle_speed
            if ai1_destination > paddle1_rect.centery and paddle1_rect.centery < 768:
                paddle1_rect.centery += paddle_speed


        #ai2 destination calculation
        if velocity_x > 0 and ai2_destination == None:
            ball_slope = velocity_y / velocity_x
            ai2_destination = ball_rect.centery + ball_slope*(758 - ball_rect.centerx)
            if ai2_destination < 0:
                ai2_destination *= -1
            if ai2_destination > 768:
                ai2_destination = 1536 - ai2_destination

        #ai2 moving to destination
        if ai2_destination != None:
            if ai2_destination < paddle2_rect.centery and paddle2_rect.centery > 0:
                paddle2_rect.centery -= paddle_speed
            if ai2_destination > paddle2_rect.centery and paddle2_rect.centery < 768:
                paddle2_rect.centery += paddle_speed
        
        #Handle collisions, set destination for ai
        if ball_rect.colliderect(paddle1_rect):
            velocity_x = random.randint(velocity_var2, velocity_var2*2)
            velocity_y = random.randint(-velocity_var2, velocity_var2)
            ai1_destination = 384
            ai2_destination = None

        if ball_rect.colliderect(paddle2_rect):
            velocity_x = -random.randint(velocity_var2, velocity_var2*2)
            velocity_y = random.randint(-velocity_var2, velocity_var2)
            ai1_destination = None
            ai2_destination = 384

        if player_R_score == winning_score or player_L_score == winning_score:
            game_active = False
    
    if not game_active:
        end_display()

    display_score()

    clock.tick(100)
    pygame.display.update()
