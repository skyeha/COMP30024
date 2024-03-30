class TShape:
    def __init__(self):
        self.shapes = {
            0: {(0, 1): 1, (1, 1): 1, (2, 1): 1, (1, 0): 1},  # Original shape
            1: {(1, 0): 1, (1, 1): 1, (1, 2): 1, (0, 1): 1},  # 90 degree rotation
            2: {(0, 1): 1, (1, 1): 1, (2, 1): 1, (1, 2): 1},  # 180 degree rotation
            3: {(1, 0): 1, (1, 1): 1, (1, 2): 1, (2, 1): 1}   # 270 degree rotation
        }
        self.num_rotations = len(self.shapes)

class ToroidalBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = {}

    def place_shape(self, shape, x, y, rotation=0):
        shape_dict = shape.shapes[rotation % shape.num_rotations]
        for (dx, dy), value in shape_dict.items():
            new_x = (x + dx - 1) % self.width
            new_y = (y + dy - 1) % self.height
            self.grid[(new_x, new_y)] = value

    def print_board(self):
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                row += str(self.grid.get((x, y), 0)) + " "
            print(row)

# Example usage
board = ToroidalBoard(10, 10)
t_shape = TShape()

# Place the T-shape at position (3, 3) with rotation 2 (180 degree rotation)
board.place_shape(t_shape, 3, 3, rotation=2)

# Print the board to see the shape's position
board.print_board()
