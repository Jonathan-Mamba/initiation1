import abc
from typing import Callable, Any
import math

#c un binary tree
class ExpressionPart(abc.ABC):    
    @abc.abstractmethod
    def get_result(self, operators: dict[str, Callable[list[float, float], float]]) -> float:# polymorphism go crazyyyy
        pass

    @abc.abstractmethod
    def set_parenthesis(self, b: bool):
        pass

    def __repr__(self) -> str:
        return self.__str__()
    

class Term(ExpressionPart):# classe Leaf
    def __init__(self, value: float = 0.0) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return str(self.value)
    
    def get_result(self, _) -> float: #on s'en fout du 2e argument
        return self.value
    
    def set_parenthesis(self, b: bool):
        pass


class ExpressionTree(ExpressionPart):# classe Tree
    def __init__(self, first: ExpressionPart, operator: str, second: ExpressionPart, parenthesis: bool = False) -> None:
        self.first_term = first
        self.operator = operator
        self.second_term = second
        self.parenthesis = parenthesis

    def __str__(self) -> str:
        if self.parenthesis:
            return f"({self.first_term} {self.operator} {self.second_term})" 
        return f"{self.first_term} {self.operator} {self.second_term}" 

    def get_result(self, operators: dict[str, Callable[list[float, float], float]]) -> float:
        return operators.get(self.operator)(self.first_term.get_result(operators), self.second_term.get_result(operators))
    
    def set_parenthesis(self, b: bool):
        self.parenthesis = b
        self.first_term.set_parenthesis(b)
        self.second_term.set_parenthesis(b)