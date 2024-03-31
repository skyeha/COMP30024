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
    
    # Get the path that we should place the tetromino block along 
    path = aStar(starting_points[0], target, initial_state)

    
    
    # valid_dir = direction_check(starting_points[0], initial_state)
    path = {k: path[k] for k in sorted(path, key=lambda x: list(path.keys()).index(x), reverse=True)}
    print(path)
    
    for _, valid_node in path.items():
        for shape in "IOTJLS":
            next_state = place_block(valid_node, )
    # test = place_block(valid_dir[0], "S", 0, initial_state)

    # path search
    # path = aStar(starting_points[0], target, initial_state)
    # path = {k: path[k] for k in sorted(path, key=lambda x: list(path.keys()).index(x), reverse=True)}

    

    # print(render_board(test, target, ansi = True))

    return None

# Check for possible shape that can be place along the path
def possible_shape(path: dict[Coord, Coord]):
    path_length = len(path)

    shape = []
    while path_length != 0:
        if path_length - 4 > 0:
            for i in range(4):
                

# Need an algorithm that checks for fully occupied column/row
def direction_check(coord: Coord, board: dict[Coord, PlayerColor]) -> list:
    valid_dir = []

    for dir in Direction:
        next_node = coord + dir.value
        if board.get(next_node) == None:
            valid_dir.append(next_node)
    return valid_dir


# Function for placing the block
def place_block(coord: Coord, shape: str, rotation : int, curr_state : dict[Coord,PlayerColor]):
    """
        Place a tetromino piece and check if that placement is valid
    """
    block = Tetromino().get_shape(shape)
    block = block.get(rotation)

    # Check for the need of adjustmenting block due to offset
    if Coord(0,0) in block:
        offset = 0
    elif Coord(1,0) in block:
        offset = 1
    elif Coord(2,0) in block:
        offset = 2

    block_coord = []
    next_state = curr_state

    for i in range(len(block)):
        new_coord = Coord((coord.r + block[i].r - offset) % BOARD_N,(coord.c + block[i].c) % BOARD_N )
        if curr_state.get(new_coord) != None: # check for overlap
            return None # can't place the block
        next_state[new_coord] = PlayerColor.RED
    
    return next_state
   
    

# compute heuristic for A* search using manhattan distance
def heuristic(node: Coord, target: Coord)-> int:
    return abs(node.r - target.r) + abs(node.c - target.c)

def deadlock_check (start: Coord, target: Coord, board: dict[Coord,PlayerColor]) -> bool:
    return True if aStar(start, target, board) == None else aStar(start, target, board)


# A* search implementation (can be used for checking deadlocks)
def aStar(start: Coord, target: Coord, board: dict[Coord, PlayerColor]):
    # store g-score of each cell (i.,e mahattan distance between start and n)
    g_score = { cell : float('inf') for cell , _ in board.items()}
    g_score[start] = 0

    # store f-score of each cell -> sum of g_score + heuristic
    f_score = { cell : float('inf') for cell , _ in board.items()}
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