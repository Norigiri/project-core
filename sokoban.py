import copy
import os
import subprocess
import sys
import argparse
import time

# Global variables
r, c = 0,0
grid = []
targets = set()
Y_row, Y_col = -1, -1
active_powerup = None
powerup_names = {"x": "Smash - Go thru walls once", 
                "^": "Strength - Push multiple boxes at once"}

# Variables for reset
orig_grid = []
orig_targets = set()
orig_Y_row, orig_Y_col = -1, -1

def file_to_basic_grid(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        rc = f.readline().strip() #reads first line, separated by space
        rows = int(rc.split()[0]) #isolates row
        basic_grid = [f.readline().strip().split() for _ in range(rows)] #each line is a list

        initial_load(basic_grid)

def initial_load(basic_grid):
    global r, c, grid, targets, Y_row, Y_col, active_powerup
    global orig_grid, orig_targets, orig_Y_col, orig_Y_row

    r, c = len(basic_grid), len(basic_grid[0])
    targets = set()
    Y_row, Y_col = -1, -1
    active_powerup = None
    grid = []

    for i in range(r):
        row = basic_grid[i]
        grid_row = []
        for j in range(c):
            tile = row[j]
            if tile == "Y":
                Y_row, Y_col = i,j
                grid_row.append('.')
            elif tile == "_":
                targets.add((i,j))
                grid_row.append('.')
            elif tile in ("B", '}','x', '^', '|', '.'):
                grid_row.append(tile)
            else:
                grid_row.append(tile)
        grid.append(grid_row) # each line is now its own list

    #Y_position is saved as "." since we will be putting Y on top of the spaces
    # "_" is saved as "." to differentiate if Y or B is also on top of the target

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
    # initially displays "." for all non powerup, banana or pillars
    display = [["." for _ in range(c)] for _ in range(r)]

    for i in range(r):
        for j in range(c):
            if grid[i][j] == "." and (i,j) in targets: # checks if target area is empty
                display[i][j] = "_" # "_" never changes, only overlapped
            else:
                display[i][j] = grid[i][j] #everything is as is
    display[Y_row][Y_col] = "Y" 
    return display

def got_powerup():
    # checks if tile stepped on is a powerup
    global grid, active_powerup
    standing = grid[Y_row][Y_col]
    if standing in ['x', '^']:
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
    # if there is no target, automatically win

    for tar_row, tar_col in targets:
        if grid[tar_row][tar_col] != "B":
            return False
    return True

def y_moving(Y_row_move, Y_col_move):
    global grid, Y_row, Y_col, active_powerup
    # handles all necessary movements

    new_Yrow, new_Ycol = Y_row + Y_row_move, Y_col + Y_col_move

    # checks if where Y is going to move to is within bounds
    if not (0 <= new_Yrow < r and 0 <= new_Ycol < c):
        return

    gonna_move_to = grid[new_Yrow][new_Ycol]

    # moving thru powerups, empty tiles, bananas
    if gonna_move_to in [".", "x", "^", "}"]:
        Y_row, Y_col = new_Yrow, new_Ycol
        got_powerup() 

        # player steps on banana
        while grid[Y_row][Y_col] == "}":
            slip_Yrow, slip_Ycol = Y_row + Y_row_move, Y_col + Y_col_move

            if not (0 <= slip_Yrow < r and 0 <= slip_Ycol < c):
                break
            next_tile = grid[slip_Yrow][slip_Ycol]

            # player is slipping with smash powerup
            if active_powerup == "x" and next_tile in ["|","B"]:
                grid[slip_Yrow][slip_Ycol] = "."
                active_powerup = None
                Y_row, Y_col = slip_Yrow, slip_Ycol
                got_powerup()
                break
            elif next_tile in ["|","B"]:
                break
            else:
                Y_row, Y_col = slip_Yrow, slip_Ycol
                got_powerup()
                if grid[Y_row][Y_col] != "}":
                    break

    # player has smash powerup
    if active_powerup == "x" and gonna_move_to in ["|","B"]:
        grid[new_Yrow][new_Ycol] = "."
        active_powerup = None
        Y_row, Y_col = new_Yrow, new_Ycol
        got_powerup()
        return

    # player is pushing a box
    if gonna_move_to == "B":
        if active_powerup == "^":
            boxes = 0
            check_row, check_col = new_Yrow, new_Ycol #used to see if long train of boxes

            while 0 <= check_row < r and 0 <= check_col < c and grid[check_row][check_col] == "B":
                boxes += 1
                check_row += Y_row_move
                check_col += Y_col_move

            # checks if train of boxes can be pushed to the space
            if not (0 <= check_row < r and 0 <= check_col < c):
                return
            if grid[check_row][check_col] != ".":
                return

            grid[check_row][check_col] = "B"
            grid[new_Yrow][new_Ycol] = "."
            Y_row, Y_col = new_Yrow, new_Ycol
            got_powerup()
            return

        else:
            new_brow, new_bcol = new_Yrow + Y_row_move, new_Ycol + Y_col_move
            
            if not (0 <= new_brow < r and 0 <= new_bcol < c): #within bounds
                return
            if grid[new_brow][new_bcol] != ".": #box doesnt move if not empty tile
                return

            grid[new_brow][new_bcol] = "B"
            grid[new_Yrow][new_Ycol] = "."
            Y_row, Y_col = new_Yrow, new_Ycol
            got_powerup()
            return

    # player is against a pillar
    if gonna_move_to == "|":
        return

def game_render():
    # renders the display
    display = grid_displayed()
    for row in display:
        print(" ".join(row))

    # prints how many targets are filled
    filled_targets = sum(1 for tar_row, tar_col in targets if grid[tar_row][tar_col] == "B")
    print(f"\nYou have filled {filled_targets}/{len(targets)} targets")

    # prints the active powerup
    activated_pr = powerup_names[active_powerup] if active_powerup else "None"
    print(f"\nActive Powerup: {activated_pr}")

def gameplay_loop():
    # handles player inputs and looping
    while True:
        os.system('cls' if os.name == 'nt' else 'clear') #checks os to clear terminal
        game_render()

        if winner():
            print("\nYou won the game!")
            break

        print("\nAccepted moves: W / A / S / D / !")
        player_moves = input("\nEnter your moves:").strip()

        for move in player_moves:
            if move.lower() not in {"w","a","s","d","!"}:
                print("\n")
                print(f"{move} is not a valid move. All other moves are disregarded")
                time.sleep(1.5)
                break
            moveset(move)

            if winner():
                break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--stage_file', default="level00.txt", help="Stage file to load")
    parser.add_argument('-m', '--moves', type=str, help="Moveset to execute")
    parser.add_argument('-o', '--output_file', type=str, help="File to write the final state")

    args = parser.parse_args()

    file_to_basic_grid(args.stage_file)

    if args.moves and args.output_file:
        for move in args.moves:
            if move.lower() not in {"w","a","s","d","!"}:
                break
            moveset(move)
            if winner():
                break

        with open(args.output_file, "w", encoding="utf-8") as f:
            if winner():
                f.write("CLEAR\n")
            else:
                f.write("NO CLEAR\n")

            display = grid_displayed()
            f.write(f"{r} {c}\n")
            for row in display:
                f.write(" ".join(row) + "\n")
    else:
        gameplay_loop()

if __name__ == "__main__":
    main()
