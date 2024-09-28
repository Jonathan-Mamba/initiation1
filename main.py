import math
import icecream
import typing
from trees import Operation, Term, Component
import funcs


def get_term(operation: str, operators: typing.Iterable,  start_index: int = 0) -> tuple[str]:
    returned_str: str = ""
    found_operators: bool = False
    print("\nNew call ")
    for i in range(start_index, len(operation)):
        icecream.ic(returned_str, i)
        char = operation[i]
        if char in (" ", "(", ")"):
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

        if char in operators and not found_operators and i > start_index:
            return (returned_str, str(i), char)
        
    return (returned_str, str(i), "")


def get_operation(operation: str, operators: typing.Iterable, priorities: dict[str, int], parenthesis: bool = False) -> Operation:
    index = 0
    terms: list[str] = []
    operations: dict[int, list[Operation]] = dict.fromkeys(range(max(priorities.values())))

    _i = 0
    icecream.ic(operation)
    while True:
        term = get_term(operation, operators, index)
        if len(terms) > 0 and terms[-1] == term[0][0] == "-":# si ya un - opérateur puis un pour négatif
            term = (term[0][1::], term[1], term[2]) # on enlèle celui pour le négatif
        terms.append(term[0])

        index = int(term[1])
        icecream.ic(terms, index)
        if term[2] == "":
            break
        else:
            terms.append(term[2])
        _i += 1

    for i, term in enumerate(terms):
        if term is None:
            continue

        if term in operators:
            if 0 < i < len(terms) - 1:
                if operations[priorities[term]] is None: 
                    operations[priorities[term]] = []
                
                operations[priorities[term]] = Operation(float(terms[i - 1]), term, float(terms[i + 1]))
                terms[i - 1], terms[i], terms[i + 1] = None, None, None #on sait jamais
        
        else:
            try: float(term)
            except ValueError:
                print(f">> {term} n'est pas un chiffre")
                quit(-1)
    
    icecream.ic(operations)
    for i in range(max(priorities.values()), 0, -1):
        
        for j in range(1, len(operations[i])):
            operations[i][j]

    
    return Operation(Term(0), "+", Term(0))

        

def main():
    OPERATORS: dict[str, typing.Callable] = {
        "+": funcs.add,
        "-": funcs.sub,
        "*": funcs.mult,
        "^": funcs.pow,
        "/": funcs.div,
        ":": funcs.fdiv,
        "%": funcs.mod
    }

    PRIORITIES: dict[str, int] = {
        "+": 0,
        "-": 0,
        "*": 1,
        "^": 2,
        "/": 1,
        ":": 1,
        "%": 1
    }
    
    while True:
        operation: Operation = get_operation(input(">> "), OPERATORS.keys(), PRIORITIES)
        result = operation.get_result(OPERATORS)
        print(f"> {result}")
        if "y" in input(">> quit <y/n> ? "):
            break



if __name__ == "__main__":
    main()