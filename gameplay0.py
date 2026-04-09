import copy
import os
import subprocess
import sys
import argparse

# Global variables
r, c = 0,0
grid = []
targets = set()
Y_row, Y_col = -1, -1
active_powerup = None

# Variables for reset
orig_grid = []
orig_targets = set()
orig_Y_row, orig_Y_col = -1, -1

def file_to_basic_grid(file_name):
    with open(filename, 'r', encoding='utf-8') as f:
        rc = str(f.readline()) #reads first line
        comma = rc.index(",")  
        rows = int(rc[0:comma]) #isolates row
        b_grid = [f.readline() for _ in range(rows)] #each line is a list

def initial_load(b_grid):
    global r, c, grid, targets, Y_row, Y_col, active_powerup
    global orig_grid, orig_targets, orig_Y_col, orig_Y_row

    r, c = len(b_grid), len(b_grid[0])
    targets = set()
    Y_row, Y_col = -1, -1
    active_powerup = None
    grid = []

    for i in range(r):
        row = b_grid[i]
        grid_row = []
        for j in range(c):
            tile = row[j]
            if tile == "Y":
                Y_row, Y_col = i,j
                grid_row.append('.')
            elif tile == "_":
                targets.add((i,j))
                grid_row.append('.')
            elif tile in ("B", '}','X', '^', '|', '.'):
                grid_row.append(tile)
            else:
                grid_row.append(tile)
        grid.append(grid_row) #each line is now separated
    #Y and _ are "." since they constantly change

    #save initial state for resets
    orig_grid = copy.deepcopy(grid)
    orig_targets = copy.deepcopy(targets)
    orig_Y_row = Y_row
    orig_Y_col = Y_col

def reset():
    global grid, targets, Y_row, Y_col, active_powerup

    grid = copy.deepcopy(orig_grid)
    targets = copy.deepcopy(orig_targets)
    Y_row = orig_Y_row
    Y_col = orig_Y_col
    active_powerup = None

def grid_displayed():
    # initially displays "." for all tiles
    display = [["." for _ range(c)] for _ in range(r)]

    for i in range(r):
        for j in range(c):
            if grid[i][j] == "." and (i,j) in targets:
                display[i][j] = "_" # "_" never changes, only overlapped
            else:
                display[i][j] = grid[i][j] #everything is as is
    display[Y_row][Y_col] = "Y"
    return display

def got_powerup():
    # checks if tile stepped on is a powerup
    global grid, active_powerup
    standing = grid[Y_row][Y_col]
    if standing in ['X', '^']:
        active_powerup = standing
        grid[Y_row][Y_col] = '.'

def moveset(user_input):
    user_input = user_input.lower()

    if user_input == "!":
        reset()

    # w/s moves up/down one row, a/d moves left/right one col
    moves = {"w":(-1,0), "a":(0,-1), "s":(1,0), "d":(0,1)}

    if user_input not in moves:
        return 

    Y_row_move, Y_col_move = moves[user_input]

    y_moving(Y_row_move, Y_col_move)

def winner():
    global targets
    # checks if all targets have a box to return a win
    
    for tar_y, tar_x in targets:
        if grid[tar_y][tar_x] != "B":
            return False
    return True

def y_moving(Y_row_move, Y_col_move):
    global grid, Y_row, Y_col, active_powerup
    # handles all necessary movements

    # moving thru powerups, empty tiles, bananas
    if ...

        # player steps on banana
        while ...

    # player has smash powerup
    if ...

    # player is pushing a box
    if ...

    # player is against a pillar
    if ...

def game_render():
    # renders the display
    ...

    # prints how many targets are filled
    boxes_on_targets = ...
    print(...)

    # prints the active powerup
    activated_pr = ...
    print(...)

def player_interaction():
    # handles player inputs

