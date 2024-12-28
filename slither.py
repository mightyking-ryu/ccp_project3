import pygame as pg
import os
from functions import WIDTH, HEIGHT, MAX_FRUITS
from functions import draw_blocks, check_collide, check_surround, create_fruits, create_rotten_fruits, \
    difficulty, move, initialization, create_super_fruits, create_paralyze_fruits


SCREENRECT = pg.Rect(0,0,WIDTH,HEIGHT)

# Text color
RED = (255, 0, 0)

# Snake color
WHITE = (255, 255, 255)
PINK = (255, 204, 229)
LIGHT_GREEN = (200, 255, 200)
LIGHT_PINK = (255, 230, 230)

# Background color
BLACK = (0, 0, 0)
GREEN = (0, 51, 25)
DARK_BLUE = (0, 0, 51)
DARK_RED = (153, 0, 0)
PURPLE = (51, 0, 102)

# Fruit color
BLUE = (102, 178, 255)
ORANGE = (255, 128, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 51)
RED = (255, 0, 0)

# Difficulty
LEVEL_CHANGE = 30
NUM_ROTTEN_FRUITS = 70
NUM_SUPER_FRUITS = 5
NUM_PARALYZE_FRUITS = 3
MUSIC_VOLUME = 0.05

# FPS
FPS = 15

# Winning length
WINNING_LENGTH = 100

main_dir = os.path.split(os.path.abspath(__file__))[0]

def main():
    
    # initialize
    level = 0
    close = 0
    win = 0
    back_color = BLACK
    fruit_color = BLUE
    num_fruits = MAX_FRUITS
    num_rotten_fruits = NUM_ROTTEN_FRUITS
    num_super_fruits = NUM_SUPER_FRUITS
    num_paralyze_fruits = NUM_PARALYZE_FRUITS

    # Initialize pygame
    pg.mixer.pre_init(44100,32,2,1024)
    pg.init()
    pg.mixer.get_init()
    
    screen = pg.display.set_mode(SCREENRECT.size)
    pg.display.set_caption("Snake Game")
    pg.mouse.set_visible(0)

    music_dir = os.path.join(main_dir, "data", 'music_0.wav'.format(level))
    pg.mixer.music.load(music_dir)
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(MUSIC_VOLUME)

    screen.fill(GREEN)

    arial_font = pg.font.SysFont("Arial", 50)
    arial_small_font = pg.font.SysFont("Arial", 20)

    start_text = ["Snake Game", "Press ENTER", "Music by \"Smilegate RPG\""]
    
    # start text
    for i, text in enumerate(start_text):
        text_size = arial_font.size(text)
        pos_x = WIDTH // 2 - text_size[0] // 2
        pos_y = HEIGHT // 2 - text_size[1] // 2

        if i == 0:
            pos_y -= 50
            start_surface = arial_font.render(text, 1, BLUE)

        elif i == 1:
            pos_y += 50
            start_surface = arial_font.render(text, 1, WHITE)
        
        elif i == 2:
            pos_x = 755
            pos_y = 690
            start_surface = arial_small_font.render(text, 1, WHITE)

        screen.blit(start_surface, (pos_x, pos_y))

    pg.display.update()

    # wait keyboard input : ENTER
    start = False
    while not start:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
            
                elif event.key == pg.K_RETURN:
                    INIT_KEYSTATE = pg.key.get_pressed()
                    start = True

        pg.time.wait(100)
    
    clock = pg.time.Clock()

    # initialize
    snake_head, snake_head_op, snake_blocks, snake_blocks_op, snake_length, \
        snake_length_op, fruits, rotten_fruits, super_fruits, paralyze_fruits = initialization(num_fruits, num_rotten_fruits, num_super_fruits, num_paralyze_fruits)
    
    key_input = INIT_KEYSTATE
    key_input_op = INIT_KEYSTATE
    
    key_paralyze = 0
    key_paralyze_op = 0
    
    
    while not close:
        
        # when game finished
        if win :
            music_dir = os.path.join(main_dir, "data", 'ending.wav')
            pg.mixer.music.load(music_dir)
            pg.mixer.music.play(-1)
            pg.mixer.music.set_volume(MUSIC_VOLUME)

            # player 1 won
            if win == 1:
                end_text = ["PLAYER 1 WON", "Press ENTER"]
                player_color = PINK

            # player 2 won
            elif win == 2:
                end_text = ["PLAYER 2 WON", "Press ENTER"]
                player_color = LIGHT_GREEN

            # draw
            elif win == 3:
                end_text = ["DRAW", "Press ENTER"]
                player_color = BLUE

            # end text (fade out effect)
            veil = pg.Surface(SCREENRECT.size)
            for fade in range(0, 51, 3):

                veil.set_alpha(fade)
                screen.blit(veil,(0,0))

                for i, text in enumerate(end_text):
                    text_size = arial_font.size(text)
                    pos_x = WIDTH // 2 - text_size[0] // 2
                    pos_y = HEIGHT // 2 - text_size[1] // 2

                    if i:
                        pos_y += 50
                        start_surface = arial_font.render(text, 1, RED)
                    else:
                        pos_y -= 50
                        start_surface = arial_font.render(text, 1, player_color)
                    
                    start_surface.set_alpha(fade * 3)
                    screen.blit(start_surface, (pos_x, pos_y))

                clock.tick(10)
                pg.display.update()
                

            # wait keyboard input : ENTER
            restart = False
            while not restart:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return

                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            return
                    
                        elif event.key == pg.K_RETURN:
                            restart = True
                            key_input = pg.key.get_pressed()
                            key_input_op = pg.key.get_pressed()

                pg.time.wait(100)

           # initialize objects
            snake_head, snake_head_op, snake_blocks, snake_blocks_op, snake_length, \
                snake_length_op, fruits, rotten_fruits, super_fruits, paralyze_fruits = initialization(num_fruits, num_rotten_fruits, num_super_fruits, num_paralyze_fruits)
            win=0
            music_dir = os.path.join(main_dir, "data", 'music_{}.wav'.format(level % 5))
            pg.mixer.music.load(music_dir)
            pg.mixer.music.play(-1)
            pg.mixer.music.set_volume(MUSIC_VOLUME)


        # change level -> music, difficulty
        if level != (snake_length + snake_length_op) // LEVEL_CHANGE:
            level = (snake_length + snake_length_op) // LEVEL_CHANGE
            music_dir = os.path.join(main_dir, "data", 'music_{}.wav'.format(level % 5))
            pg.mixer.music.load(music_dir)
            pg.mixer.music.play(-1)
            pg.mixer.music.set_volume(MUSIC_VOLUME)
            back_color, fruit_color, num_fruits = difficulty(level)
            fruits = list()
            rotten_fruits = list()
            super_fruits = list()
            paralyze_fruits = list()
            create_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, num_fruits)
            create_rotten_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, num_rotten_fruits)
            create_super_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, num_super_fruits)
            create_paralyze_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, num_super_fruits)
            
        screen.fill(back_color)

        # event loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return

        
        # move snakes
        keystate = pg.key.get_pressed()
        condition = (keystate[pg.K_RIGHT] + keystate[pg.K_LEFT] + keystate[pg.K_DOWN] + keystate[pg.K_UP] != 0)
        condition_op = (keystate[pg.K_d] + keystate[pg.K_a] + keystate[pg.K_s] + keystate[pg.K_w] != 0)
        if condition:
            key_input = keystate
        if condition_op:
            key_input_op = keystate
            
        if key_paralyze > 0:
            key_input = INIT_KEYSTATE
            key_paralyze -= 1
        if key_paralyze_op > 0:
            key_input_op = INIT_KEYSTATE
            key_paralyze_op -= 1
        snake_head = move(key_input, 1, snake_head, snake_blocks)
        snake_head_op = move(key_input_op, 2, snake_head_op, snake_blocks_op)

        # delete blocks if length of snake blocks is larger than actual snake_length
        while len(snake_blocks) > snake_length:
            del snake_blocks[0]
        while len(snake_blocks_op) > snake_length_op:
            del snake_blocks_op[0]
            
        # draw objects (snakes, fruits)
        draw_blocks(snake_blocks, screen, LIGHT_GREEN, True, WHITE)
        draw_blocks(snake_blocks_op, screen, LIGHT_PINK, True, PINK)
        draw_blocks(fruits, screen, fruit_color, False)
        draw_blocks(rotten_fruits, screen, GRAY, False)
        draw_blocks(super_fruits, screen, YELLOW, False)
        draw_blocks(paralyze_fruits, screen, RED, False)
        
        # check whether my snake reached winning length
        if snake_length >= WINNING_LENGTH:
            win += 1
        if snake_length_op >= WINNING_LENGTH:
            win += 2


        # score board
        score_surface = arial_small_font.render("1P : {}".format(snake_length), 1, LIGHT_GREEN)
        score_surface_op = arial_small_font.render("2P : {}".format(snake_length_op), 1, PINK)
        screen.blit(score_surface, (0,0))
        screen.blit(score_surface_op, (0,20))
        pg.display.update()

        # check whether snake head collide with fruits 
        is_collide, fruit_index = check_collide(snake_head, fruits)
        is_collide_op, fruit_index_op = check_collide(snake_head_op, fruits)

        if is_collide:
            snake_length += 1
            del fruits[fruit_index]
            create_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, 1)

        if is_collide_op:
            snake_length_op += 1
            del fruits[fruit_index_op]
            create_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, 1)
            
        # check whether snake head collide with super fruits 
        is_collide, super_index = check_collide(snake_head, super_fruits)
        is_collide_op, super_index_op = check_collide(snake_head_op, super_fruits)

        if is_collide:
            snake_length += 3
            del super_fruits[super_index]
            create_super_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, 1)

        if is_collide_op:
            snake_length_op += 3
            del super_fruits[super_index_op]
            create_super_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, 1)

        # check whether snake head collide with rotten fruits
        is_collide_rotten, rotten_index = check_collide(snake_head, rotten_fruits)
        is_collide_rotten_op, rotten_index_op = check_collide(snake_head_op, rotten_fruits)

        if is_collide_rotten:
            snake_length = max(snake_length-3, 1)
            del rotten_fruits[rotten_index]
            create_rotten_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, 1)
        
        if is_collide_rotten_op:
            snake_length_op = max(snake_length_op-3, 1)
            del rotten_fruits[rotten_index_op]
            create_rotten_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, 1)
            
        # check whether snake head collide with paralyze fruits 
        is_collide, paralyze_index = check_collide(snake_head, paralyze_fruits)
        is_collide_op, paralyze_index_op = check_collide(snake_head_op, paralyze_fruits)

        if is_collide:
            key_paralyze_op = 15
            del paralyze_fruits[paralyze_index]
            create_paralyze_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, 1)

        if is_collide_op:
            key_paralyze = 15
            del paralyze_fruits[paralyze_index_op]
            create_paralyze_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, 1)

        # check whether snake head collide with oponent snake head
        if check_collide(snake_head, snake_blocks_op)[0]:
            win += 2
        if check_collide(snake_head_op, snake_blocks)[0]:
            win += 1

        # check whether my snake completely surround opponent snake
        if check_collide(snake_head, snake_blocks[:-1])[0]:
            if check_surround(snake_blocks, snake_head_op):
                win += 1
        if check_collide(snake_head_op, snake_blocks_op[:-1])[0]:
            if check_surround(snake_blocks_op, snake_head):
                win += 2
        
        # cap the framework at ??fps
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pg.quit()




