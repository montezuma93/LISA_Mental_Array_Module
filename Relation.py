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

class North:
    mean = Mean.High
    agent_x_lxr_units = 0
    agent_y_lxr_units = -2
    referent_x_lxr_units = 0
    referent_y_lxr_units = 2

class South:
    mean = Mean.Low
    agent_x_lxr_units = 0
    agent_y_lxr_units = 2
    referent_x_lxr_units = 0
    referent_y_lxr_units = -2

class West:
    mean = Mean.Low
    agent_x_lxr_units = -2
    agent_y_lxr_units = 0
    referent_x_lxr_units = 2
    referent_y_lxr_units = 0

class East:
    mean = Mean.High
    agent_x_lxr_units = 2
    agent_y_lxr_units = 0
    referent_x_lxr_units = -2
    referent_y_lxr_units = 0

class NorthWest:
    mean = Mean.High
    agent_x_lxr_units = -2
    agent_y_lxr_units = 2
    referent_x_lxr_units = 2
    referent_y_lxr_units = -2

class NorthEast:
    mean = Mean.High
    agent_x_lxr_units = 2
    agent_y_lxr_units = 2
    referent_x_lxr_units = -2
    referent_y_lxr_units = -2

class SouthWest:
    mean = Mean.Low
    agent_x_lxr_units = -2
    agent_y_lxr_units = -2
    referent_x_lxr_units = 2
    referent_y_lxr_units = 2

class SouthEast:
    mean = Mean.Low
    agent_x_lxr_units = 2
    agent_y_lxr_units = -2
    referent_x_lxr_units = -2
    referent_y_lxr_units = 2

