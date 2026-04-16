import copy

from file_functions import emoji_to_text
from gameplay import laro_position, mushroom_total, text_to_move, grass_or_others, tool_interaction, laro_movement, no_print_gameplay_loop

level0 = [
['🌲', '🌲', '🌲'],
['🟦', '🟦', '🟦'],
['🌲', '🌲', '🌲'] ]

level1 = [
["🌲", "🌲", "🌲", "🌲", "🌲"], 
["🌲", "🪓", "🧑",  "🍄", "🌲"], 
["🌲", "🌲", "🌲", "🌲", "🌲"] ]

level2 = [
["🌲","🌲","🌲","🌲","🌲","🌲","🌲","🌲","🌲"],
["🌲","🟩","🟩","🟩","🍄","🟩","🟩","🟩","🌲"],
["🌲","🟩","🟩","🟩","🟦","🟩","🟩","🟩","🌲"],
["🌲","🟩","🟩","🟩","🪨","🟩","🌲","🟩","🌲"],
["🌲","🟩","🌲","🟩","🧑","🌲","🌲","🟩","🌲"],
["🌲","🟩","🪓","🟩","🟩","🔥","🟩","🟩","🌲"],
["🌲","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🌲"],
["🌲","🟩","🟩","🟩","🟩","🟩","🟩","🟩","🌲"],
["🌲","🌲","🌲","🌲","🌲","🌲","🌲","🌲","🌲"], ]

level3 = [
['🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲'],
['🌲', '🧑', '🌲', '🍄', '🟩', '🟩', '🟩', '🌲'],
['🌲', '🟩', '🌲', '🌲', '🌲', '🌲', '🟩', '🌲'],
['🌲', '🟩', '🟩', '🍄', '🟩', '🟩', '🍄', '🌲'],
['🌲', '🟦', '🟦', '🟦', '🟦', '🟦', '🟦', '🌲'],
['🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲'] ]

level4 = [
['🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲'],
['🌲', '🟩', '🟩', '🟩', '🟦', '🍄', '🌲'],
['🌲', '🟩', '🟩', '🟩', '🟦', '🟩', '🌲'],
['🌲', '🧑', '🪨', '🪨', '🟦', '🟦', '🌲'],
['🌲', '🟩', '🟩', '🟩', '🟦', '🟩', '🌲'],
['🌲', '🟩', '🟩', '🟩', '🟦', '🍄', '🌲'],
['🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲'] ]

level5 = [
['🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲'],
['🌲', '🟦', '🟦', '🟩', '🟩', '🧑', '🟩', '🪨', '🌲'],
['🌲', '🪓', '🟦', '🟩', '🟦', '🟩', '🟦', '🟦', '🌲'],
['🌲', '🟩', '🟦', '🟩', '🟦', '🟩', '🌲', '🟩', '🌲'],
['🌲', '🟩', '🟩', '🟩', '🟦', '🟩', '🌲', '🍄', '🌲'],
['🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲'] ]

memory = [[(12, 3), (23, 13)], [(1, 23), (67, 6)],
[(0, 0), (1, 2)], [(1, 45), (5, 67)], [(146, 23), (87, 99)], ]


def test_laro_position():
    # To add to this test, input the grid of your map into the
    # laro_position function and assert it with the (rows, cols)
    # of Laro in the map.
    assert laro_position(level0) == None
    assert laro_position(level1) == (1, 2)
    assert laro_position(level2) == (4, 4)
    assert laro_position(level3) == (1, 1)
    assert laro_position(level4) == (3, 1)
    assert laro_position(level5) == (1, 5)


def test_mushroom_total():
    # To add to this test, input the grid of your map into the
    # mushroom_total function and assert it with the number of
    # mushrooms in the map.
    assert mushroom_total(level0) == 0
    assert mushroom_total(level1) == 1
    assert mushroom_total(level2) == 1
    assert mushroom_total(level3) == 3
    assert mushroom_total(level4) == 2
    assert mushroom_total(level5) == 1


def test_text_to_move():
    assert text_to_move("W") == [(-1, 0)]
    
    assert text_to_move("s") == [(1, 0)]
    
    assert text_to_move("L") == [(0, -1)]
    
    assert text_to_move("r") == [(0, 1)]
    
    assert text_to_move("p") == [('action', 'pickup')]
    
    assert text_to_move("!") == [('action', 'restart')]
    
    assert text_to_move("m") == [('action', 'nothing')]
    
    assert text_to_move("awsd") == [(0, -1), (-1, 0), (1, 0), (0, 1)]
    
    assert text_to_move("ALwPm!bWs") == [(0, -1), (0, -1), (-1, 0),
    ('action', 'pickup'), ('action', 'nothing'), ('action', 'restart'),
    (1, 0), (-1, 0), (1, 0)]


def test_grass_or_others():
    assert grass_or_others(12, 3, memory) == "⬜"
    assert grass_or_others(23, 13, memory) == "⬜"

    assert grass_or_others(1, 23, memory) == "🪓"
    assert grass_or_others(67, 6, memory) == "🪓"

    assert grass_or_others(0, 0, memory) == "🔥"
    assert grass_or_others(1, 2, memory) == "🔥"

    assert grass_or_others(1, 45, memory) == "💣"
    assert grass_or_others(5, 67, memory) == "💣"

    assert grass_or_others(146, 23, memory) == "🧽"
    assert grass_or_others(87, 99, memory) == "🧽"

    assert grass_or_others(42, 42, memory) == "🟩"
    assert grass_or_others(16, 1, memory) == "🟩"


def modified_movement(grid, move_input):
    grid_copy = copy.deepcopy(grid)
    mushrooms = mushroom_total(grid)
    laro_coords = laro_position(grid)
    memory0 = [[], [], [], [], []]
    laro_item = "Empty"
    move = text_to_move(move_input)[0]
    (grid_copy, laro_coords, mushrooms, memory0, laro_item, validity) = laro_movement(grid_copy,
                    laro_coords, move, mushrooms, memory0, laro_item)
    return (emoji_to_text(grid_copy), memory0, mushrooms)


def test_movement():
    # To add to this test, take the initial state of your map and do
    # a singular move and assert it to the resulting state of the map.
    assert modified_movement(level1, "l") == ([
    'TTTTT',
    'TL.+T',
    'TTTTT' ], [[], [(1, 1),], [], [], []], 1)

    assert modified_movement(level1, "u") == ([
    'TTTTT',
    'TxL+T',
    'TTTTT' ], [[], [], [], [], []], 1)

    assert modified_movement(level1, "b") == ([
    'TTTTT',
    'TxL+T',
    'TTTTT' ], [[], [], [], [], []], 1)

    assert modified_movement(level1, "r") == ([
    'TTTTT',
    'Tx.LT',
    'TTTTT' ], [[], [], [], [], []], 0)

    assert modified_movement(level2, "l") == ([
    'TTTTTTTTT',
    'T...+...T',
    'T...~...T',
    'T...R.T.T',
    'T.TL.TT.T',
    'T.x..*..T',
    'T.......T',
    'T.......T',
    'TTTTTTTTT' ], [[], [], [], [], []], 1)

    assert modified_movement(level2, "u") == ([
    'TTTTTTTTT',
    'T...+...T',
    'T...-...T',
    'T...L.T.T',
    'T.T..TT.T',
    'T.x..*..T',
    'T.......T',
    'T.......T',
    'TTTTTTTTT' ], [[(2, 4),], [], [], [], []], 1)

    assert modified_movement(level2, "b") == ([
    'TTTTTTTTT',
    'T...+...T',
    'T...~...T',
    'T...R.T.T',
    'T.T..TT.T',
    'T.x.L*..T',
    'T.......T',
    'T.......T',
    'TTTTTTTTT' ], [[], [], [], [], []], 1)

    assert modified_movement(level2, "r") == ([
    'TTTTTTTTT',
    'T...+...T',
    'T...~...T',
    'T...R.T.T',
    'T.T.LTT.T',
    'T.x..*..T',
    'T.......T',
    'T.......T',
    'TTTTTTTTT' ], [[], [], [], [], []], 1)

    assert modified_movement(level2, "m") == ([
    'TTTTTTTTT',
    'T...+...T',
    'T...~...T',
    'T...R.T.T',
    'T.T.LTT.T',
    'T.x..*..T',
    'T.......T',
    'T.......T',
    'TTTTTTTTT' ], [[], [], [], [], []], 1)

    # Note that test_movement also serves as a unit test for 
    # entity_moving and tool_interaction, as in each of these assertions
    # entity_moving is used to move Laro around, and tool_interaction
    # can be seen in the first assertion, since the coordinates of the
    # axe has been properly stored in the memory


def modified_no_print_gameplay_loop(grid, move_str):
    original_grid = copy.deepcopy(grid)
    (if_cleared, original_grid) = no_print_gameplay_loop(original_grid, move_str)
    text_grid = emoji_to_text(original_grid)
    return (if_cleared, text_grid)


def test_no_print_gameplay_loop():
    # To add to this test, take the initial state of your map and input
    # a string of moves and assert it to whether the map was cleared
    # and the final state of the map.
    assert modified_no_print_gameplay_loop(level0, "") == ('CLEAR', [
    'TTT', 
    '~~~',
    'TTT' ])

    assert modified_no_print_gameplay_loop(level0, "wfadeawdwa") == ('CLEAR', [
    'TTT',
    '~~~',
    'TTT' ])

    assert modified_no_print_gameplay_loop(level2, "mo") == ('NO CLEAR', [
    'TTTTTTTTT',
    'T...+...T',
    'T...~...T',
    'T...R.T.T',
    'T.T.LTT.T',
    'T.x..*..T',
    'T.......T',
    'T.......T',
    'TTTTTTTTT'])

    assert modified_no_print_gameplay_loop(level2, "uuu") == ('CLEAR', [
    'TTTTTTTTT',
    'T...L...T',
    'T...-...T',
    'T.....T.T',
    'T.T..TT.T',
    'T.x..*..T',
    'T.......T',
    'T.......T',
    'TTTTTTTTT'])

    assert modified_no_print_gameplay_loop(level2, "bllpu") == ('NO CLEAR', [
    'TTTTTTTTT',
    'T...+...T',
    'T...~...T',
    'T...R.T.T',
    'T.L..TT.T',
    'T....*..T',
    'T.......T',
    'T.......T',
    'TTTTTTTTT' ])

    assert modified_no_print_gameplay_loop(level2, "bbb!b") == ('NO CLEAR', [
    'TTTTTTTTT',
    'T...+...T',
    'T...~...T',
    'T...R.T.T',
    'T.T..TT.T',
    'T.x.L*..T',
    'T.......T',
    'T.......T',
    'TTTTTTTTT' ])

    assert modified_no_print_gameplay_loop(level2, "brpu") == ('NO CLEAR', [
    'TTTTTTTTT',
    'T...+...T',
    'T...~...T',
    'T...R...T',
    'T.T..L..T',
    'T.x.....T',
    'T.......T',
    'T.......T',
    'TTTTTTTTT' ])

    assert modified_no_print_gameplay_loop(level2, "brprrrrru") == ('NO CLEAR', [
    '.........',
    '....+....',
    '....~....',
    '....R.T..',
    '..T..TT.L',
    '..x......',
    '.........',
    '.........',
    '.........' ])

    assert modified_no_print_gameplay_loop(level2, "blnpoi!uuu") == ('CLEAR', [
    'TTTTTTTTT',
    'T...L...T',
    'T...-...T',
    'T.....T.T',
    'T.T..TT.T',
    'T.x..*..T',
    'T.......T',
    'T.......T',
    'TTTTTTTTT'])
