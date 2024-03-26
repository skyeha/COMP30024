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

    # Need to modify board to know which path is movable 

    # Need to get the coordinates of the starting red point
    # starting_points = [(coord,color) for coord,color in board.items() if color.value == 0]
   
    grid = create_grid(board)
   


    # return [
    #     PlaceAction(Coord(2, 5), Coord(2, 6), Coord(3, 6), Coord(3, 7)),
    #     PlaceAction(Coord(1, 8), Coord(2, 8), Coord(3, 8), Coord(4, 8)),
    #     PlaceAction(Coord(5, 8), Coord(6, 8), Coord(7, 8), Coord(8, 8)),
    # ]
    return None


# compute heuristic for A* search using manhattan distance
def heuristic(node: Coord, target: Coord)-> int:
    return abs(node.r - target.r) + abs(node.c - target.c)

def aStar(start: Coord, target: Coord, board: dict[Coord, PlayerColor]):
    g_score = { node : float('inf') for node , _ in board.items()}
    g_score[start] = 0
    f_score = { node : float('inf') for node , _ in board.items()}
    f_score[start] = heuristic(start, target) 

    open = PriorityQueue()
    open.put((f_score[start], heuristic(start, target), start))

    while not open.empty():
        current_node = open.get()[2]

        if current_node == target:
            break

        while child_node == None:
            if is_empty(curent_node)
            
def is_empty(board: dict[Coord, PlayerColor], node: Coord) -> bool:
    return True if board.get(Coord) == None else False      


def create_grid(board: dict[Coord,PlayerColor]) -> dict[Coord, PlayerColor]:
    grid = {}
    for r in range(BOARD_N):
        for c in range(BOARD_N):
            if Coord(r,c) in board:
                grid[Coord(r,c)] = board.get(Coord(r,c))
            else:
                grid[Coord(r,c)] = None
    return grid