# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

from .core import PlayerColor, Coord, PlaceAction, BOARD_N, Direction
from .utils import render_board
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


    

    # path search
    # path = aStar(starting_points[0], target, initial_state)
    # path = {k: path[k] for k in sorted(path, key=lambda x: list(path.keys()).index(x), reverse=True)}

    # for key in path.keys():
    #     if key == target:
    #         break
    #     grid[key] = PlayerColor.RED

    # print(render_board(grid, target, ansi = True))

    return None


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