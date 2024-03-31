# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress
# python -m search < test-vis1.csv

from .core import PlayerColor, Coord, PlaceAction, BOARD_N
from .utils import render_board
import heapq
from itertools import product

def heuristic(board, target):
    target_row, target_col = target.r, target.c
    # Count the number of empty spaces in the target row and column.
    empty_spaces_row = BOARD_N - sum(1 for coord in board if coord.r == target_row)
    empty_spaces_col = BOARD_N - sum(1 for coord in board if coord.c == target_col)
    
    # Focus on the line (row or column) that is closer to completion.
    min_empty_spaces = min(empty_spaces_row, empty_spaces_col)
    
    # Assuming an average case where a single tetromino placement affects 2-3 spaces towards the goal.
    estimated_moves_to_goal = min_empty_spaces / 2.5
    
    return estimated_moves_to_goal

tetromino_shapes = {
    'I': [
        [(0, 0), (1, 0), (2, 0), (3, 0)],  # Vertical
        [(0, 0), (0, 1), (0, 2), (0, 3)]   # Horizontal
    ],
    'O': [
        [(0, 0), (0, 1), (1, 0), (1, 1)]  # Only one orientation
    ],
    'T': [
        [(1, 0), (0, 1), (1, 1), (1, 2)],  # Up
        [(0, 1), (1, 0), (1, 1), (2, 1)],  # Right
        [(0, 0), (0, 1), (0, 2), (1, 1)],  # Down
        [(0, 0), (1, 0), (2, 0), (1, 1)]   # Left
    ],
    'S': [
        [(0, 1), (0, 2), (1, 0), (1, 1)],  # Initial
        [(0, 0), (1, 0), (1, 1), (2, 1)],  # Rotated 90 degrees
        [(0, 1), (0, 2), (1, 0), (1, 1)],  # Rotated 180 degrees (Same as initial)
        [(0, 0), (1, 0), (1, 1), (2, 1)]   # Rotated 270 degrees (Same as 90 degrees)
    ],
    'Z': [
        [(0, 0), (0, 1), (1, 1), (1, 2)],  # Initial
        [(0, 1), (1, 0), (1, 1), (2, 0)],  # Rotated 90 degrees
        [(0, 0), (0, 1), (1, 1), (1, 2)],  # Rotated 180 degrees (Same as initial)
        [(0, 1), (1, 0), (1, 1), (2, 0)]   # Rotated 270 degrees (Same as 90 degrees)
    ],
    'J': [
        [(0, 0), (1, 0), (1, 1), (1, 2)],  # Initial
        [(0, 1), (1, 1), (2, 1), (2, 0)],  # Rotated 90 degrees
        [(0, 0), (0, 1), (0, 2), (1, 2)],  # Rotated 180 degrees
        [(0, 0), (0, 1), (1, 0), (2, 0)]   # Rotated 270 degrees
    ],
    'L': [
        [(0, 2), (1, 0), (1, 1), (1, 2)],  # Initial
        [(0, 0), (0, 1), (1, 1), (2, 1)],  # Rotated 90 degrees
        [(0, 0), (0, 1), (0, 2), (1, 0)],  # Rotated 180 degrees
        [(0, 1), (1, 1), (2, 0), (2, 1)]   # Rotated 270 degrees
    ]
}

def generate_tetromino_placements(shape, board):
    """Generate all valid placements for a given tetromino shape."""
    for rotation in tetromino_shapes[shape]:
        for r, c in product(range(BOARD_N), repeat=2):
            if valid_placement(board, rotation, Coord(r, c)):
                yield rotation, Coord(r, c)

def valid_placement(board, tetromino, base_coord):
    # Check if the placement of a tetromino starting from base_coord is valid
    for rel_coord in tetromino:
        coord = Coord((base_coord.r + rel_coord[0]) % BOARD_N, (base_coord.c + rel_coord[1]) % BOARD_N)
        if coord in board:  # Check for overlap
            return False
    return True

def successors(board):
    # Generate successors by attempting to place every tetromino in every possible position and rotation.
    for shape in tetromino_shapes.keys():
        for rotation, base_coord in generate_tetromino_placements(shape, board):
            new_board = dict(board)
            action_coords = []
            for rel_r, rel_c in rotation:
                coord = Coord((base_coord.r + rel_r) % BOARD_N, (base_coord.c + rel_c) % BOARD_N)
                new_board[coord] = PlayerColor.RED
                action_coords.append(coord)
            if action_coords:  # Ensure action_coords is not empty
                yield (PlaceAction(*action_coords), new_board)

def is_goal(board, target):
    # Check if the target Blue token has been removed from the board
    return target not in board

def a_star_search(board, target):
    start_state = board
    frontier = [(heuristic(board, target), 0, 0)]  # Initial state with heuristic, cost, and state ID
    explored = set()
    path_dict = {0: []}  # Maps state IDs to paths (lists of actions)
    board_dict = {0: start_state}  # Maps state IDs to board states
    id_counter = 1  # Start with 1 since 0 is used for the initial state

    while frontier:
        est, cost, state_id = heapq.heappop(frontier)
        current_path = path_dict[state_id]
        current_board = board_dict[state_id]
        
        if is_goal(current_board, target):
            return current_path
        
        explored.add(state_id)
        
        for action, resulting_board in successors(current_board):
            # Generate a new state ID for this potential successor
            new_state_id = id_counter
            id_counter += 1
            
            # Only proceed if this board state hasn't been explored
            if new_state_id not in explored:
                new_path = current_path + [action]
                path_dict[new_state_id] = new_path
                board_dict[new_state_id] = resulting_board
                
                new_cost = cost + 1
                est = new_cost + heuristic(resulting_board, target)
                heapq.heappush(frontier, (est, new_cost, new_state_id))
    
    return None



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
    print(render_board(board, target, ansi=False))

    # Do some impressive AI stuff here to find the solution...
    # ...
    # ... (your solution goes here!)
    # ...

    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    return a_star_search(board, target)
