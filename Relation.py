from enum import Enum

class Relation(Enum):
    North = "North"
    South = "South"
    West = "West"
    East = "East"
    NorthWest = "NorthWest"
    NorthEast = "NorthEast"
    SouthWest = "SouthWest"
    SouthEast = "SouthEast"

class Mean(Enum):
    High = "High"
    Low = "Low"

class Direction(Enum):
    Minus = "Minus"
    Plus = "Plus"
    Zero = "Zero"


class North:
    is_marked = False
    mean = Mean.Low
    agent_x_direction = Direction.Zero
    agent_y_direction = Direction.Minus
    referent_x_direction = Direction.Zero
    referent_y_direction = Direction.Plus

class South:
    is_marked = False
    mean = Mean.High
    agent_x_direction = Direction.Zero
    agent_y_direction = Direction.Plus
    referent_x_direction = Direction.Zero
    referent_y_direction = Direction.Minus

class West:
    is_marked = False
    mean = Mean.Low
    agent_x_direction = Direction.Minus
    agent_y_direction = Direction.Zero
    referent_x_direction = Direction.Plus
    referent_y_direction = Direction.Zero

class East:
    is_marked = False
    mean = Mean.High
    agent_x_direction = Direction.Plus
    agent_y_direction = Direction.Zero
    referent_x_direction = Direction.Minus
    referent_y_direction = Direction.Zero

class NorthWest:
    is_marked = True
    mean = Mean.Low
    agent_x_direction = Direction.Minus
    agent_y_direction = Direction.Minus
    referent_x_direction = Direction.Plus
    referent_y_direction = Direction.Plus

class NorthEast:
    is_marked = True
    mean = Mean.Low
    agent_x_direction = Direction.Plus
    agent_y_direction = Direction.Minus
    referent_x_direction = Direction.Minus
    referent_y_direction = Direction.Plus

class SouthWest:
    is_marked = True
    mean = Mean.Low
    agent_x_direction = Direction.Minus
    agent_y_direction = Direction.Plus
    referent_x_direction = Direction.Plus
    referent_y_direction = Direction.Minus

class SouthEast:
    is_marked = True
    mean = Mean.High
    agent_x_direction = Direction.Plus
    agent_y_direction = Direction.Plus
    referent_x_direction = Direction.Minus
    referent_y_direction = Direction.Minus

