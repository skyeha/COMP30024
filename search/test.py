from enum import Enum
import core

class Direction(Enum):
    
    Down = (0,-1)
    Up = (0,1)
    Left = (-1,0)
    Right = (1,0)


x = core.Coord(1,2)
y = core.Coord(1,2)
print(x + y)
