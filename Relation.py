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

class LxrDirection(Enum):
    Minus = "Minus"
    Plus = "Plus"
    Zero = "Zero"


class North:
    is_marked = False
    mean = Mean.Low
    agent_x_lxr_units = LxrDirection.Zero
    agent_y_lxr_units = LxrDirection.Minus
    referent_x_lxr_units = LxrDirection.Zero
    referent_y_lxr_units = LxrDirection.Plus

class South:
    is_marked = False
    mean = Mean.High
    agent_x_lxr_units = LxrDirection.Zero
    agent_y_lxr_units = LxrDirection.Plus
    referent_x_lxr_units = LxrDirection.Zero
    referent_y_lxr_units = LxrDirection.Minus

class West:
    is_marked = False
    mean = Mean.Low
    agent_x_lxr_units = LxrDirection.Minus
    agent_y_lxr_units = LxrDirection.Zero
    referent_x_lxr_units = LxrDirection.Plus
    referent_y_lxr_units = LxrDirection.Zero

class East:
    is_marked = False
    mean = Mean.High
    agent_x_lxr_units = LxrDirection.Plus
    agent_y_lxr_units = LxrDirection.Zero
    referent_x_lxr_units = LxrDirection.Minus
    referent_y_lxr_units = LxrDirection.Zero

class NorthWest:
    is_marked = True
    mean = Mean.Low
    agent_x_lxr_units = LxrDirection.Minus
    agent_y_lxr_units = LxrDirection.Minus
    referent_x_lxr_units = LxrDirection.Plus
    referent_y_lxr_units = LxrDirection.Plus

class NorthEast:
    is_marked = True
    mean = Mean.Low
    agent_x_lxr_units = LxrDirection.Plus
    agent_y_lxr_units = LxrDirection.Minus
    referent_x_lxr_units = LxrDirection.Minus
    referent_y_lxr_units = LxrDirection.Plus

class SouthWest:
    is_marked = True
    mean = Mean.Low
    agent_x_lxr_units = LxrDirection.Minus
    agent_y_lxr_units = LxrDirection.Plus
    referent_x_lxr_units = LxrDirection.Plus
    referent_y_lxr_units = LxrDirection.Minus

class SouthEast:
    is_marked = True
    mean = Mean.High
    agent_x_lxr_units = LxrDirection.Plus
    agent_y_lxr_units = LxrDirection.Plus
    referent_x_lxr_units = LxrDirection.Minus
    referent_y_lxr_units = LxrDirection.Minus

