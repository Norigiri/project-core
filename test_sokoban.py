import sokoban

level0 = [
  ["|", ".", "x", "|", "|", "|"],
  ["Y", ".", ".", ".", ".", "_"],
  [".", ".", "B", ".", ".", "."],
  ["|", ".", ".", ".", "|", "|"]
]

level1 = [
  [".", ".", ".", ".", "|", "|", "|"],
  ["x", "Y", "B", ".", ".", ".", "."],
  [".", "}", ".", ".", "B", "|", "|"],
  [".", ".", ".", "x", ".", "|", "_"]
]

level2 = [
  [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
  [".", "^", ".", ".", ".", ".", ".", "x", ".", "."],
  [".", ".", ".", ".", "Y", "}", "}", ".", ".", "."],
  [".", "|", ".", ".", ".", ".", "B", "B", ".", "."],
  ["|", "_", "|", ".", ".", ".", ".", ".", "_", "."]
]

level3 = [
  ["|", "|", "|", "|", "|", "x", "|", "|"],
  ["|", "|", "|", ".", ".", ".", ".", "|"],
  ["_", ".", "B", "|", "|", "|", ".", "|"],
  ["|", "|", "|", "|", "|", "|", ".", "|"]
]

level4 = [
  [".", ".", ".", ".", "x", ".", ".", ".", ".", ".", ".", "."],
  [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "B", "B"],
  ["|", "}", "}", "x", "^", ".", ".", ".", ".", ".", "B", "B"],
  [".", ".", ".", ".", ".", ".", ".", ".", "B", "B", "Y", "^"] 
]


def move_looper(moves_string):
    # loops moves so it looks cleaner while testing
    for move in moves_string:
        sokoban.moveset(move)

def test_initial_load():
    # To add more tests, input a level grid as seen above
    # Assert the level as seen below with the row, col of Y
    # The assertion is based on the range 0 to n-1
    
    sokoban.initial_load(level0)

    # tests Y position (Note: (-1,-1) means Y does not exist)
    assert sokoban.Y_row == 1
    assert sokoban.Y_col == 0

    # tests how many targets and their positions
    assert (1,5) in sokoban.targets
    assert len(sokoban.targets) == 1

    # tests if Y is moving accordingly
    move_looper("ddddsasaaw")
    assert sokoban.Y_row == 2
    assert sokoban.Y_col == 1

    # tests if Y picked up a powerup, correctly identified, and correctly replaced
    move_looper("wwd")
    assert sokoban.active_powerup == "x"
    assert sokoban.grid[0][2] == "."

    # tests if Y used up smash
    move_looper("d")
    assert sokoban.active_powerup is None # power up used
    assert sokoban.grid[0][3] == "." # wall broken

    # tests if when Y pushed a box, the box moved
    move_looper("ssa")
    assert sokoban.grid[2][2] == "."
    assert sokoban.grid[2][1] == "B"

    # tests if reset worked
    sokoban.moveset("!") # best case is to observe if all destroyed, moved, and picked up are returned
    assert sokoban.Y_row == 1
    assert sokoban.Y_col == 0
    assert sokoban.grid[2][2] == "B" # og box spot
    assert sokoban.grid[0][3] == "|" # wall returned
    assert sokoban.grid[0][2] == "x" # power up returned

        # keep note that we only called sokoban.initial_load(level0) once
        # thus all moves done within each level are saved which is why reset works

#---------------------------------------------------------------------------------------------

    # LEVEL 1 ASSERTIONS 
    # this follows same format as above, with added tests for the following
    # Slipping on bananas, winning the game, and smashing boxes

    sokoban.initial_load(level1)

    assert sokoban.Y_row == 1
    assert sokoban.Y_col == 1
    assert (3,6) in sokoban.targets
    assert len(sokoban.targets) == 1

    move_looper("dwds") # tests both Y moving and box moving
    assert sokoban.Y_row == 1
    assert sokoban.Y_col == 3
    assert sokoban.grid[2][3] == "B"
    move_looper("aala") 
    # l is an invalid move but since we are unit testing
    # it cannot physically ignore l, thus the last a should be registered
    assert sokoban.Y_row == 1
    assert sokoban.Y_col == 0

    # tests if Y slips on the banana
    move_looper("ds") # slips downwards
    assert sokoban.Y_row == 3
    assert sokoban.Y_col == 1
    sokoban.moveset("w") # slips upwards
    assert sokoban.Y_row == 1
    assert sokoban.Y_col == 1

    # tests if smash also breaks boxes
    move_looper("addds")
    assert sokoban.active_powerup == None
    assert sokoban.grid[2][3] == "."

    # tests if Y won the game
    move_looper("sddaawwdsasdd") 
    # sequence moving Y to break the wall 
    # covering the target and moving the box
    assert sokoban.winner() is True

    sokoban.moveset("!")
    assert sokoban.Y_row == 1
    assert sokoban.Y_col == 1
    assert sokoban.grid[1][0] == "x"
    assert sokoban.grid[3][3] == "x"
    assert sokoban.grid[1][2] == "B"
    assert sokoban.grid[2][4] == "B"

#---------------------------------------------------------------------------------------------

    # LEVEL 2 ASSERTIONS 
    # this follows same format as above, with added tests for the following
    # Strength powerup, moving multiple boxes

    sokoban.initial_load(level2)
    assert sokoban.Y_row == 2
    assert sokoban.Y_col == 4
    assert (4,1) in sokoban.targets
    assert (4,8) in sokoban.targets
    assert len(sokoban.targets) == 2

    move_looper("dw") # tests both banana slipping and smash powerup
    assert sokoban.Y_row == 1
    assert sokoban.Y_col == 7
    assert sokoban.active_powerup == "x"
    assert sokoban.grid[1][7] == "."
    move_looper("sassaa") # tests wall breaking
    assert sokoban.grid[4][2] == "."
    assert sokoban.active_powerup is None

    # tests if strength powerup is working
    move_looper("wwwadddddddssa")
    assert sokoban.active_powerup == "^"
    assert sokoban.grid[1][1] == "."
    assert sokoban.grid[3][5] == "B" #box on [3][6] moved left
    assert sokoban.grid[3][6] == "B" #box on [3][7] moved left

    # winning the game with multiple targets
    move_looper("aaawaaswddssaawdddddwds")
    assert sokoban.winner() is True

    sokoban.moveset("!")
    assert sokoban.Y_row == 2
    assert sokoban.Y_col == 4
    assert sokoban.grid[1][7] == "x"
    assert sokoban.grid[3][6] == "B" 
    assert sokoban.grid[3][7] == "B" 
    assert sokoban.grid[4][2] == "|"

#---------------------------------------------------------------------------------------------

    # LEVEL 3 ASSERTIONS
    # Y does not exist, so any moves should not change Y's positions
    # it is impossible to win in this map

    sokoban.initial_load(level3)
    assert sokoban.Y_row == -1
    assert sokoban.Y_col == -1
    assert (2,0) in sokoban.targets
    assert len(sokoban.targets) == 1

    move_looper("asadasfsdasadwaawad")
    assert sokoban.Y_row == -1
    assert sokoban.Y_col == -1

    sokoban.moveset("!")
    assert sokoban.Y_row == -1
    assert sokoban.Y_col == -1

    assert sokoban.winner() is False

#---------------------------------------------------------------------------------------------

    # LEVEL 4 ASSERTIONS
    # there are no targets, so it is impossible to lose
    # the condition to win is vacuously true, thus always wins

    sokoban.initial_load(level4)
    assert sokoban.Y_row == 3
    assert sokoban.Y_col == 10
    assert sokoban.targets == set()
    assert len(sokoban.targets) == 0

    # initial box positions and wall
    assert sokoban.grid[3][9] == "B"
    assert sokoban.grid[3][8] == "B"
    assert sokoban.grid[2][10] == "B"
    assert sokoban.grid[1][10] == "B"
    assert sokoban.grid[2][11] == "B"
    assert sokoban.grid[1][11] == "B"
    assert sokoban.grid[2][0] == "|"

    move_looper("dwsawsa") # set of moves that tests if all boxes were moved
    assert sokoban.Y_row == 3
    assert sokoban.Y_col == 9
    assert sokoban.active_powerup == "^"
    assert sokoban.grid[3][9] == "."
    assert sokoban.grid[3][8] == "B"
    assert sokoban.grid[3][7] == "B"
    assert sokoban.grid[2][10] == "."
    assert sokoban.grid[1][10] == "B"
    assert sokoban.grid[0][10] == "B"
    assert sokoban.grid[2][11] == "."
    assert sokoban.grid[1][11] == "B"
    assert sokoban.grid[0][11] == "B"

    # tests if powerups overwrite one another
    move_looper("wwwaaaaa")
    assert sokoban.active_powerup == "x"
    move_looper("ss")
    assert sokoban.active_powerup == "^"
    sokoban.moveset("a")
    assert sokoban.active_powerup == "x"

    # tests if slipping on bananas with smash breaks the wall
    sokoban.moveset("a")
    assert sokoban.active_powerup == None
    assert sokoban.grid[2][0] == "."

    assert sokoban.winner() is True

    sokoban.moveset("!")
    assert sokoban.Y_row == 3
    assert sokoban.Y_col == 10
    assert sokoban.grid[3][9] == "B"
    assert sokoban.grid[3][8] == "B"
    assert sokoban.grid[2][10] == "B"
    assert sokoban.grid[1][10] == "B"
    assert sokoban.grid[2][11] == "B"
    assert sokoban.grid[1][11] == "B"
    assert sokoban.grid[2][0] == "|"
    assert sokoban.grid[0][4] == "x"
    assert sokoban.grid[2][3] == "x"
    assert sokoban.grid[2][4] == "^"
