from .core import Coord

class Tetromino:
    
    def __init__(self):
        self.shapes = {
            "I" : {
                0 : [Coord(0,0), Coord (0,1), Coord(0,2) , Coord(0,3)],
                1 : [Coord(0,0), Coord (1,0), Coord(2,0) , Coord(3,0)]
            },
            "O" : {
                0 : [Coord(0,0), Coord (0,1), Coord(1,0) , Coord(1,1)],
            },
            "T" : {
                0 : [Coord(0, 1), Coord (1, 1), Coord(1,2) , Coord(1,0)], # upside down T
                1 : [Coord(0,0), Coord (1,0), Coord(2,0) , Coord(1,1)], # anti-clockwise 90 T
                2 : [Coord(0,0), Coord(0,1), Coord(0,2), Coord(1,1)], #
                3 : [Coord(0,1), Coord(1,0), Coord(1,1), Coord(2,1)]
            },
            "J" : {
                0 : [Coord(0,1), Coord (1, 1), Coord(2,1) , Coord(2,0)],
                1 : [Coord(0,0), Coord (1,0), Coord(2,0) , Coord(1,1)],
                2 : [Coord(0,0), Coord(1,0), Coord(1,1), Coord(1,2)],
                3 : [Coord(0,0), Coord(0,1), Coord(0,2), Coord(1,2)]
            },
            "L" : {
                0 : [Coord(0,0), Coord (1, 0), Coord(2,0) , Coord(2,1)],
                1 : [Coord(0,0), Coord(0,1) , Coord(0,2), Coord (1,0)],
                2 : [Coord(0,0), Coord(0,1), Coord(1,1), Coord(2,1)],
                3 : [Coord(0,2), Coord(1,0), Coord(1,1), Coord(1,2)]
            },
            "S" : {
                0 : [Coord(0,0), Coord(0,1), Coord(1,1), Coord(1,2)],
                1 : [Coord(0,1), Coord(1,1), Coord(1,0), Coord(2,0)],
                2 : [Coord(0,1), Coord(0,2), Coord(1,0), Coord(1,1)],
                3 : [Coord(0,0), Coord(1,0), Coord(1,1), Coord(2,1)]
            }

        }

        self.num_rotations = {
            "I" : 2,
            "O" : 1,
            "T" : 4,
            "J" : 4,
            "L" : 4,
            "S" : 4

        }
    
    def get_shape(self,name):
        return self.shapes.get(name)
    
    def get_num_rotation(self, name):
        return self.num_rotations.get(name)