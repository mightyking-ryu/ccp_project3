import pygame as pg
import random
import itertools
from pymunk import Poly
from shapely.geometry import Point, Polygon
import numpy as np

BLOCK_SIZE = 10
WIDTH = 960
HEIGHT = 720
MAX_FRUITS = 60

# Background color
BLACK = (0, 0, 0)
GREEN = (0, 51, 25)
DARK_BLUE = (0, 0, 51)
DARK_RED = (153, 0, 0)
PURPLE = (51, 0, 102)

# fruit color
BLUE = (102, 178, 255)
ORANGE = (255, 128, 0)
GRAY = (128, 128, 128)

X_ALL = list(range(0, WIDTH, BLOCK_SIZE))
Y_ALL = list(range(0, HEIGHT, BLOCK_SIZE))
POINT_ALL = list(itertools.product(X_ALL, Y_ALL))

field = np.zeros((HEIGHT//BLOCK_SIZE, WIDTH//BLOCK_SIZE))

def difficulty(level):
    """ 
    Adjust difficulty of game 
    
        Parametes:
            level : integer
        
        Returns:
            Tuple (background color, fruit color, number of fruits)

    """
    
    num_fruits = max(MAX_FRUITS - level * 10, 10)

    if level % 5 == 0:
        return BLACK, BLUE, num_fruits
    if level % 5 == 1:
        return GREEN, BLUE, num_fruits
    if level % 5 == 2:
        return DARK_BLUE, BLUE, num_fruits
    if level % 5 == 3:
        return DARK_RED, ORANGE, num_fruits
    if level % 5 == 4:
        return PURPLE, BLUE, num_fruits


def initialization(num_fruits, num_rotten_fruits, num_super_fruits, num_paralyze_fruits):
    """
    Initialize objects

        Parameters:
            num_fruits : integer
            num_rotten_fruits : integer
            num_super_fruits : integer
            num_paralyze_fruits : integer

        Returns :
            snake_head, snake_head_op, snake_blocks, snake_blocks_op, \
                snake_length, snake_length_op, fruits, rotten_fruits, super_fruits, paralyze_fruits

    """
    snake_head = [WIDTH//2 + 50, HEIGHT//2]
    snake_head_op = [WIDTH//2 - 50, HEIGHT//2]
    snake_blocks = [snake_head]
    snake_blocks_op = [snake_head_op]
    snake_length = 1
    snake_length_op = 1
    fruits = list()
    rotten_fruits = list()
    super_fruits = list()
    paralyze_fruits = list()
    create_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, num_fruits)
    create_rotten_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, num_rotten_fruits)
    create_super_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, num_super_fruits)
    create_paralyze_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, num_paralyze_fruits)
    return snake_head, snake_head_op, snake_blocks, snake_blocks_op, \
                snake_length, snake_length_op, fruits, rotten_fruits, super_fruits, paralyze_fruits


def draw_blocks(blocks, screen, color, snake = bool, head_color = None):
    """
    Draw blocks in 'blocks' list

        Parameters:
            blocks : list
            screen : screen object
            color : color of block
            snake : whether snake or fruit
            head_color : snake head color
        
        Returns:
            None

    """
    if len(blocks)==0:
        return
    
    for block in blocks[:-1]:
        pos_x, pos_y = block
        pg.draw.rect(screen, color, [pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE])

    if snake:
        pos_x, pos_y = blocks[-1]
        pg.draw.rect(screen, head_color, [pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE])
    
    else:
        pos_x, pos_y = blocks[-1]
        pg.draw.rect(screen, color, [pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE])


# (optional)
def check_same(block1, block2):
    """ check whether two blocks are same """
    return (block1[0] == block2[0]) & (block1[1] == block2[1])
    

def check_collide(check_block, block_list):
    """ 
    check whether check_block collide with any blocks in block_list 
    return index of collision block in block_list with boolean value

        Parameters: 
            check_block : (int, int)
            block_list : list
        
        Returns: 
            tuple : (bool, int)

    """
    
    is_collide = check_block in block_list
    index = None
    
    if is_collide:
        index = block_list.index(check_block)
        
    return is_collide, index
    

def check_surround(snake_blocks, opponent_head):
    """
    check whether my snake completely surround opponent snake

        Parameters:
            snake_blocks : list
            opponent_head : (int, int)
        
        Return :
            Boolean

    
    point = Point(opponent_head)
    coords = snake_blocks[check_collide(snake_blocks[0], snake_blocks[:-1])[1]:-1]
    polygon = Polygon(coords)
    
    return point.within(polygon)
    """
    
    field.fill(0)
    
    for p in snake_blocks:
        p_x, p_y = p[0]//BLOCK_SIZE, p[1]//BLOCK_SIZE
        field[(p_y, p_x)] = 1
        
    x_init, y_init = opponent_head[0]//BLOCK_SIZE, opponent_head[1]//BLOCK_SIZE
    
    if not flood_fill(x_init, y_init):
        return False
    return True
    


def create_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, num):
    """
    create fruits 

        Parameters:
            snake_blocks : list
            snake_blocks_op : list
            fruits : list
            rotten_fruits : list
            super_fruits : list
            paralyze_fruits : list
            num : int

        Returns:
            None

    """
    
    all = POINT_ALL[:]
        
    exclude = snake_blocks + snake_blocks_op + fruits + rotten_fruits + super_fruits + paralyze_fruits
    excluded = []
    
    for i in exclude:
        if i in excluded:
            continue
        all.remove(tuple(i))
        excluded.append(i)
        
    for j in range(num):
        p = random.choice(all)
        all.remove(p)
        fruits.append(list(p))
    
    return
    
        

def create_rotten_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, num):
    """
    create rotten fruits
    
        Parameters:
            snake_blocks : list
            snake_blocks_op : list
            fruits : list
            rotten_fruits : list
            super_fruits : list
            paralyze_fruits : list
            num : int

        Returns:
            None

    """
    
    all = POINT_ALL[:]
        
    exclude = snake_blocks + snake_blocks_op + fruits + rotten_fruits + super_fruits + paralyze_fruits
    excluded = []
    
    for i in exclude:
        if i in excluded:
            continue
        all.remove(tuple(i))
        excluded.append(i)
        
    for j in range(num):
        p = random.choice(all)
        all.remove(p)
        rotten_fruits.append(list(p))
    
    return

def create_super_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits, num):
    """
    create super fruits
    
        Parameters:
            snake_blocks : list
            snake_blocks_op : list
            fruits : list
            rotten_fruits : list
            super_fruits : list
            paralyze_fruits : list
            num : int

        Returns:
            None

    """
    
    all = POINT_ALL[:]
        
    exclude = snake_blocks + snake_blocks_op + fruits + rotten_fruits + super_fruits + paralyze_fruits
    excluded = []
    
    for i in exclude:
        if i in excluded:
            continue
        all.remove(tuple(i))
        excluded.append(i)
        
    for j in range(num):
        p = random.choice(all)
        all.remove(p)
        super_fruits.append(list(p))
    
    return

def create_paralyze_fruits(snake_blocks, snake_blocks_op, fruits, rotten_fruits, super_fruits, paralyze_fruits,num):
    """
    create paralyze fruits
    
        Parameters:
            snake_blocks : list
            snake_blocks_op : list
            fruits : list
            rotten_fruits : list
            super_fruits : list
            paralyze_fruits : list
            num : int

        Returns:
            None

    """
    
    all = POINT_ALL[:]
        
    exclude = snake_blocks + snake_blocks_op + fruits + rotten_fruits + super_fruits + paralyze_fruits
    excluded = []
    
    for i in exclude:
        if i in excluded:
            continue
        all.remove(tuple(i))
        excluded.append(i)
        
    for j in range(num):
        p = random.choice(all)
        all.remove(p)
        paralyze_fruits.append(list(p))
    
    return



# (optinal)
def is_inside(pos):
    
    """ whether pos(int, int) is inside the screen """

    return (0 <= pos[0]) & (pos[0] + BLOCK_SIZE <= WIDTH) & (0 <= pos[1]) & (pos[1] + BLOCK_SIZE <= HEIGHT)

def move(keystate, player, snake_head, snake_blocks):
    """
    Move snake head by keyboard input and append new snake head to snake blocks

        Parameters:
            keystate : dict
            player : int
            snake_head : (int, int)
            snake_blocks : list
        
        Returns:
            snake_head : (int, int)
    """
    
    if player == 1:
        move_right = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
        move_down = keystate[pg.K_DOWN] - keystate[pg.K_UP]

    elif player == 2:
        move_right = keystate[pg.K_d] - keystate[pg.K_a]
        move_down = keystate[pg.K_s] - keystate[pg.K_w]
        
    if (move_right == 0) & (move_down == 0):
        return snake_head[:]

    new_snake_head = snake_head[:]
    
    new_snake_head[0] += move_right * BLOCK_SIZE
    new_snake_head[1] += move_down * BLOCK_SIZE
    
    if not is_inside(new_snake_head):
        return snake_head[:]
    
    snake_blocks.append(new_snake_head[:])
    
    return new_snake_head[:]

def flood_fill(x ,y):

    if x < 0 or x >= len(field[0]) or y < 0 or y >= len(field):
        return False

    if field[y][x] != 0:
        return True
    
    field[y][x] = -1

    if not flood_fill(x+1, y):
        return False
    if not flood_fill(x-1, y):
        return False
    if not flood_fill(x, y+1):
        return False
    if not flood_fill(x, y-1):
        return False
    return True