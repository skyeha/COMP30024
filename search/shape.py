from .core import *

class I_shape:

    def __init__(self):
        self.shapes = {
            0 : [Coord(0,0), Coord (0,1), Coord(0,2) , Coord(0,3)],
            1 : [Coord(0,0), Coord (1,0), Coord(2,0) , Coord(3,0)]
        }

class O_shape:

    def __init__(self):
        self.shapes = {
            0 : [Coord(0,0), Coord (0,1), Coord(1,0) , Coord(1,1)],
        }

class T_shape:

    def __init__(self):
        self.shapes = {
            0 : [Coord(0, 1), Coord (1, 1), Coord(1,2) , Coord(1,0)],
            1 : [Coord(0,0), Coord (1,0), Coord(2,0) , Coord(1,1)],
            2 : [Coord(0,0), Coord(0,1), Coord(0,2), Coord(1,1)],
            3 : [Coord(0,1), Coord(0,1), Coord(1,1), Coord(2,1)]
        }

class J_shape:

    def __init__(self):
        self.shapes = {
            0 : [Coord(0,1), Coord (1, 1), Coord(2,1) , Coord(2,0)],
            1 : [Coord(0,0), Coord (1,0), Coord(2,0) , Coord(1,1)],
            2 : [Coord(0,0), Coord(1,0), Coord(1,1), Coord(1,2)],
            3 : [Coord(0,0), Coord(0,1), Coord(0,2), Coord(1,2)]
        }

class L_shape:

    def __init__(self):
        self.shapes = {
            0 : [Coord(0,0), Coord (1, 0), Coord(2,0) , Coord(2,1)],
            1 : [Coord(0,0), Coord(0,1) , Coord(0,2), Coord (1,0)],
            2 : [Coord(0,0), Coord(0,1), Coord(1,1), Coord(2,1)],
            3 : [Coord(0,2), Coord(1,0), Coord(1,1), Coord(1,2)]
        }

class Z_shape:
    
    def __init__(self):
        self.shape = {
            0 : [Coord(0,0), Coord(0,1), Coord(1,1), Coord(1,2)],
            1 : [Coord(0,1), Coord(1,1), Coord(1,0), Coord(2,0)]
        }

class S_shape:
    
    def __init__(self):
        self.shape = {
            0 : [Coord(0,1), Coord(0,2), Coord(1,0), Coord(1,1)],
            1 : [Coord(0,0), Coord(1,0), Coord(1,1), Coord(2,1)]
        }