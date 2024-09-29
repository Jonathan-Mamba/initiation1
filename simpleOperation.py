

class StringOperation:
    def __init__(self, first: str, operator: str, second: str) -> None:
        self.first = first
        self.operator = operator
        self.second = second

    def __repr__(self) -> str:
        return f"({self.first} {self.operator} {self.second})"