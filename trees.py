import abc
from typing import Callable, Any
import math

#c un binary tree
class Component(abc.ABC):    
    @abc.abstractmethod
    def get_result(self, operators: dict[str, Callable[list[float, float], float]]) -> float:# polymorphism go crazyyyy
        pass
    
    @abc.abstractmethod
    def hasnan(self) -> bool:
        pass

    def __repr__(self) -> str:
        return self.__str__()
    

class Term(Component):# classe Leaf
    def __init__(self, value: float = 0.0) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return str(self.value)
    
    def get_result(self, _) -> float: #on s'en fout du 2e argument
        return self.value
    
    def hasnan(self) -> bool:
        return math.isnan(self.value)


class Operation(Component):# classe Tree
    def __init__(self, first: Component, operator: str, second: Component, parenthesis: bool = False) -> None:
        self.first_term = first
        self.operator = operator
        self.second_term = second
        self.parenthesis = parenthesis

    def __str__(self) -> str:
        return f"{'(' if self.parenthesis else ''}{self.first_term} {self.operator} {self.second_term}{')' if self.parenthesis else ''}" 
    
    def get_result(self, operators: dict[str, Callable[list[float, float], float]]) -> float:
        return operators.get(self.operator)(self.first_term.get_result(operators), self.second_term.get_result(operators))
    
    def hasnan(self) -> bool:
        return self.first_term.hasnan() or self.second_term.hasnan() 