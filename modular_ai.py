import math
from typing import Any, Callable
import numpy as np
import arcade
from constants import *

## MODULAR UTILITY FUNCTIONS

def dist(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


def magnitude(vector):
    return math.sqrt(sum(pow(element, 2) for element in vector))

def norm_vect_btwn(src_pos:tuple[float,float], dest_pos:tuple[float,float]):
    result = np.array(dest_pos) - np.array(src_pos)
    return result / magnitude(result)

def sprite_dist(sprite1: arcade.Sprite, sprite2: arcade.Sprite):
    return ((sprite1.center_x - sprite2.center_x)**2 + (sprite1.center_y - sprite2.center_y)**2) ** 0.5
















## MODULAR CLASSES

class Consideration:
    def __init__(self, weight:float = 1.0):
        self.weight = weight
    
    # # define a virtual method called calculate that returns a float
    def calculate(self) -> float:
        return self.weight
    
    def update(self, dt: float) -> None:
        pass

    def reset(self) -> None:
        pass

class Duration(Consideration):
    def __init__(self,weight:float) -> None:
        super().__init__(weight)
        self.duration = 0.0
    
    def calculate(self) -> float:
        return self.weight * self.duration
    
    def update(self, dt: float) -> None:
        self.duration += dt
    
    def reset(self) -> None:
        self.duration = 0.0

class Distance(Consideration):
    def __init__(self, weight:float, pos1: Callable[[],tuple[float,float]], pos2: Callable[[],tuple[float,float]]) -> None:
        super().__init__(weight)
        self.pos1 = pos1
        self.pos2 = pos2
        self.distance = dist(self.pos1(), self.pos2())
    
    def calculate(self) -> float:
        return self.weight * self.distance
    
    # def update(self, pos1: Callable[[],tuple[float,float]], pos2: Callable[[],tuple[float,float]]) -> None:
    def update(self, dt: float) -> None:
        # self.pos1 = pos1
        # self.pos2 = pos2
        self.distance = dist(self.pos1(), self.pos2())
        pass

    def reset(self) -> None:
        pass

class AboveThreshold(Consideration):
    def __init__(self, weight:float, threshold:float, value: Callable[[],float]) -> None:
        super().__init__(weight)
        self.threshold = threshold
        self.value = value
        self.above = self.value() > self.threshold
    
    def calculate(self) -> float:
        return self.weight * self.above
    
    def update(self, dt: float) -> None:
        self.above = self.value() > self.threshold
    
    def reset(self) -> None:
        pass

class BelowThreshold(Consideration):
    def __init__(self, weight:float, threshold:float, value: Callable[[],float]) -> None:
        super().__init__(weight)
        self.threshold = threshold
        self.value = value
        self.below = self.value() < self.threshold
    
    def calculate(self) -> float:
        return self.weight * self.below
    
    def update(self, dt: float) -> None:
        self.below = self.value() < self.threshold
    
    def reset(self) -> None:
        pass

# class Action:
#     # def __init__(self, target: arcade.Sprite, action: str, *args:Any) -> None:
#     def __init__(self, action_name:str, *args:Any) -> None:
#         # self.target = target
#         self.action_name = action_name
#         self.args = args



def product(considerations: list[Consideration]) -> float:
    weight = considerations[0].calculate()
    for consideration in considerations[1:]:
        weight *= consideration.calculate()
    return weight

def aggregate(considerations: list[Consideration]) -> float:
    weight = 0.0
    for consideration in considerations:
        weight += consideration.calculate()
    return weight

class Option:
    def __init__(self, priority:int, considerations:list[Consideration], actions: list[str], combination = "aggregate", description="") -> None:
        self.priority = priority
        # self.name = name
        self.considerations = considerations
        self.actions = actions
        self.combination = combination
        self.description = description

    def calculate(self) -> float:
        if self.combination == "aggregate":
            return aggregate(self.considerations)
        else:
            return product(self.considerations)
    
    def add_consideration(self, consideration: Consideration) -> None:
        self.considerations.append(consideration)

    def __str__(self) -> str:
        return f"Option: {self.description +' - ' if self.description else  ''}P={self.priority} | W={self.calculate()}"

    def __repr__(self) -> str:
        return self.__str__()

def choose(options: list[Option]) -> Option:
    # filter out all options with weight of 0
    options = [opt for opt in options if opt.calculate() > 0]
    print(options)
    # if no options left, return None
    if len(options) == 0:
        return None
    # find highest priority
    target_priority = max([opt.priority for opt in options])
    # filter out all options with lower priority than highest priority
    best_options = [opt for opt in options if opt.priority == target_priority]
    # choose randomly weighted option based on calculated weight
    return np.random.choice(best_options, p=[opt.calculate() for opt in options])

