# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

from .core import PlayerColor, Coord, PlaceAction, BOARD_N, Direction
from .utils import render_board
from .shape import *
from queue import PriorityQueue 


def search(
    board: dict[Coord, PlayerColor], 
    target: Coord
) -> list[PlaceAction] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `PlayerColor` instances.  
        `target`: the target BLUE coordinate to remove from the board.
    
    Returns:
        A list of "place actions" as PlaceAction instances, or `None` if no
        solution is possible.
    """

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    print(render_board(board, target, ansi=True))

    actions = {}


    # Need to get the coordinates of the starting red point
    starting_points = [coord for coord,color in board.items() if color.value == 0]
    

    initial_state = current_state(board)
    
    valid_dir = direction_check(starting_points[0], initial_state)
    print(valid_dir)
    
    test = place_block(valid_dir[0], "S", 2, initial_state)

    # path search
    # path = aStar(starting_points[0], target, initial_state)
    # path = {k: path[k] for k in sorted(path, key=lambda x: list(path.keys()).index(x), reverse=True)}

    # initial_state[Coord((7 + 0) % BOARD_N , (9+1) % BOARD_N)] = PlayerColor.RED
    # initial_state[Coord(7 % BOARD_N, 10 % BOARD_N)] = PlayerColor.RED
    # initial_state[Coord(7 % BOARD_N, 11 % BOARD_N)] = PlayerColor.RED
    # initial_state[Coord(7 % BOARD_N, 12 % BOARD_N)] = PlayerColor.RED

    # initial_state[Coord(8 % BOARD_N, 9 % BOARD_N)] = PlayerColor.RED
    # initial_state[Coord(8 % BOARD_N, 10 % BOARD_N)] = PlayerColor.RED
    # initial_state[Coord(8 % BOARD_N, 11 % BOARD_N)] = PlayerColor.RED
    # initial_state[Coord(8 % BOARD_N, 12 % BOARD_N)] = PlayerColor.RED

    print(render_board(test, target, ansi = True))

    return None


# Need an algorithm that checks for fully occupied column/row
def direction_check(coord: Coord, board: dict[Coord, PlayerColor]) -> list:
    valid_dir = []

    for dir in Direction:
        next_node = coord + dir.value
        if board.get(next_node) == None:
            valid_dir.append(next_node)
    return valid_dir


# Function for placing the block
def place_block(coord: Coord, shape: str, rotation : int, board : dict[Coord,PlayerColor]):
    block = Block().get_shape(shape)
    block = block.get(rotation)

    # Check for the need of adjustment the block due to offset
    if Coord(0,0) in block:
        offset = 0
    elif Coord(1,0) in block:
        offset = 1
    elif Coord(2,0) in block:
        offset = 2

    if placement_check(coord, board, block):
        for i in range(len(block)):
            place = Coord((coord.r + block[i].r - offset) % BOARD_N , (coord.c + block[i].c) % BOARD_N)
            board[place] = PlayerColor.RED
    #         return True
    # return False
    return board
   
    

def placement_check(coord: Coord, board : dict[Coord,PlayerColor], block : list):
    if Coord(0,0) in block:
        offset = 0
    elif Coord(1,0) in block:
        offset = 1
    elif Coord(2,0) in block:
        offset = 2

    for i in range(len(block)):
        new_coord = Coord((coord.r + block[i].r - offset) % BOARD_N,(coord.c + block[i].c) % BOARD_N )
        if board.get(new_coord) != None:
            return False # overlaps with an occupied cell
    return True

# compute heuristic for A* search using manhattan distance
def heuristic(node: Coord, target: Coord)-> int:
    return abs(node.r - target.r) + abs(node.c - target.c)

def deadlock_check (start: Coord, target: Coord, board: dict[Coord,PlayerColor]) -> bool:
    return True if aStar(start, target, board) == None else aStar(start, target, board)


# A* search implementation (can be used for checking deadlocks)
def aStar(start: Coord, target: Coord, board: dict[Coord, PlayerColor]):
    # store g-score of each node (i.,e mahattan distance between start and n)
    g_score = { node : float('inf') for node , _ in board.items()}
    g_score[start] = 0

    # store f-score of each node -> sum of g_score + heuristic
    f_score = { node : float('inf') for node , _ in board.items()}
    f_score[start] = heuristic(start, target) 

    open = PriorityQueue()
    open.put((f_score[start], heuristic(start, target), start))
    
    path = {} 

    while not open.empty():
        current_node = open.get()[2]

        if current_node == target:
            break

        for dir in Direction:
            if board.get(current_node.__add__(dir.value)) == None or current_node.__add__(dir.value) == target:
                child_node = current_node.__add__(dir.value) 

                temp_g_score = g_score[current_node] + 1
                temp_f_score = temp_g_score + heuristic(child_node, target)

                if temp_f_score < f_score[child_node]:
                    g_score[child_node] = temp_g_score
                    f_score[child_node] = temp_f_score
                    open.put((temp_f_score, heuristic(child_node, target), child_node))
                    path[child_node] = current_node

    # check for cases of deadlock
    if target not in path:
        return None
    
    final_path = {}     
    tracker = target
    while tracker != start:
        final_path[path[tracker]] = tracker
        tracker = path[tracker]

    return final_path

def current_state(board: dict[Coord,PlayerColor]) -> dict[Coord, PlayerColor]:
    grid = {}
    for r in range(BOARD_N):
        for c in range(BOARD_N):
            if Coord(r,c) in board:
                grid[Coord(r,c)] = board.get(Coord(r,c))
            else:
                grid[Coord(r,c)] = None
    return grid