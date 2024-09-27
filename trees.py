import abc
from typing import Callable, Any
import math


class Component(abc.ABC):
    @abc.abstractmethod
    def get_result(self, operators: dict[str, Callable[list[float, float], float]]) -> float:
        return operators.get(self.operator)(self.first_term, self.second_term)
    

class Term(Component):
    def __init__(self, value: float = 0.0) -> None:
        self.value = value
    
    def get_result(self, operators: dict[str, Callable[[], float]]) -> float:
        return self.value


class Operation(Component):
    def __init__(self, first: float, operator: str, second: float, parenthesis: bool = False) -> None:
        self.first_term = first
        self.operator = operator
        self.second_term = second
        self.parenthesis = parenthesis

    def __str__(self) -> str:
        return f"{'(' if self.parenthesis else ''}{self.first_term} {self.operator} {self.second_term}{')' if self.parenthesis else ''}" 
    
    def get_result(self, operators: dict[str, Callable[list[float, float], float]]) -> float:
        return super().get_result(operators)