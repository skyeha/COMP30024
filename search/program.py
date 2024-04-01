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
    path = aStar(starting_points[1], target, initial_state)

    
    
    # valid_dir = direction_check(starting_points[0], initial_state)
    path = {k: path[k] for k in sorted(path, key=lambda x: list(path.keys()).index(x), reverse=True)}
    
    asd = path_breakdown(path)
    print(asd)
    
    

    # path search
    # path = aStar(starting_points[0], target, initial_state)
    # path = {k: path[k] for k in sorted(path, key=lambda x: list(path.keys()).index(x), reverse=True)}

    

    # print(render_board(test, target, ansi = True))

    return None

# Breaking the path down to segments of 4 cells
def path_breakdown(main_path: dict[Coord, Coord]):
    path_length = len(main_path)
    

    path_pieces = []
    while path_length != 0:
        path = []
        path_items = list(main_path.items())
        if (path_length) - 4 > 0:
            for i in range(4):
                path.append(path_items[i][1])
                main_path.pop(path_items[i][0])
            path_pieces.append(path)
            path_length = path_length - 4
        else:
            for i in range(path_length):
                path.append(path_items[i][1])
                main_path.pop(path_items[i][0])
            path_pieces.append(path)
            path_length = 0
    return path_pieces
                

# Need an algorithm that checks for fully occupied column/row
def generate_possible_tetromino(shape: str, base_coord: Coord, board: dict[Coord, PlayerColor]):
    """
        Generate possible rotation of the specified Tetromino shape that can be placed
    """
    for rotation in Tetromino().get_shape(shape):
        offset = get_offset(rotation)
        action_coord = []
        for tetro_coord in rotation:
            new_coord = Coord((base_coord.r + tetro_coord.r - offset) % BOARD_N, (base_coord.c + tetro_coord.c) % BOARD_N)
            if board.get(new_coord) != None:
                continue
            action_coord.append(new_coord)
        yield rotation, action_coord

def successor(base_coord: Coord, board: dict[Coord, PlayerColor]):
    """
        Generate all possible state that we can get from the 19 pieces of tetrominoes
    """
    for shape in Tetromino().shapes.keys():
        for rotation , action_coord in generate_possible_tetromino(shape, base_coord, board):
            if not action_coord:
                continue
            successor_state = board
            for coord in action_coord:
                successor_state[coord] = PlayerColor.RED
            yield (action_coord, successor_state)

            
def get_offset(shape: list):
    if Coord(0,0) in shape:
        return 0
    elif Coord(1,0) in shape:
        return 1
    elif Coord(2,0) in shape:
        return 2
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
    
    return next_state , new_coord
   
    

# compute heuristic for A* search using manhattan distance
def heuristic(node: Coord, target: Coord)-> int:
    return abs(node.r - target.r) + abs(node.c - target.c)


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
                next_state = place_block 

                temp_g_score = g_score[current_node] + 1
                temp_f_score = temp_g_score + heuristic(child_node, target)

                ## append the current board to the queue,
                ## children node should be change to node in the tetromino that is closes to the target
                

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