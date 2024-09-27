import math
import icecream
import typing
from trees import Operation
import funcs


def get_term(operation: str, operators: typing.Iterable, start_index: int = 0) -> str:
    returned_str: str = ""
    found_operators: bool = False
    for i in range(start_index, len(operation)):
        char = operation[i]
        if char == " ":
            continue

        if char == "-" and returned_str == "":
            returned_str = "-"
            continue

        if char == ".":
            if "." not in returned_str:
                returned_str += "."
            else:
                raise ValueError(f"trop de points dans {returned_str}")
        
        if char.isdigit():
            returned_str += char

        if char in operators and not found_operators and i > 0:
            return (returned_str, start_index, char)
        
    return (returned_str, start_index, "")

def get_operation(operation: str, operators: typing.Iterable) -> Operation:
    index = -1
    first_term = ""
    operator = ""
    second_term = ""

    for char in operation:
        index += 1
        icecream.ic(char, index)
        if char == " ":
            continue

        if char == '-' and first_term == "":
            first_term = "-"

        if char == ".":
            if "." not in first_term:
                first_term += "."
            else:
                raise ValueError("mais chef (deux points)")
        
        if char.isdigit():
            first_term += char

        if char in operators:
            operator = char
            break


    for i in range(index + 1, len(operation)):
        char = operation[i]
        icecream.ic(char, i)
        if char == " ":
            continue

        if char == '-' and second_term == "":
            second_term = "-"

        if char == ".":
            if "." not in second_term:
                second_term += "."
            else:
                raise ValueError("mais chef (deux points)")
        
        if char.isdigit():
            second_term += char

        if char in operators:
            raise ValueError("chef tu fous quoi (trop d'opérateurs ptet)")

    try:
        float(first_term)
    except ValueError:
        print(">> manque le premier chiffre")
        quit(1)
    
    try:
        float(second_term)
    except ValueError:
        print(">> manque le 2e chiffre")
        quit(1)

    
    return Operation(float(first_term), operator, float(second_term))

        

def main():
    OPERATORS = {
        "+": funcs.add,
        "-": funcs.sub,
        "*": funcs.mult,
        "^": funcs.pow,
        "/": funcs.div,
        ":": funcs.fdiv,
        "%": funcs.mod
    }
    
    while True:
        operation: Operation = get_operation(input(">> "), OPERATORS.keys())
        result = operation.get_result(OPERATORS)
        print(f"> {result}")
        if "n" in input(">> quit <y/n> ? "):
            break



if __name__ == "__main__":
    main()