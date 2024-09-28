import math
import icecream
import typing
from trees import Operation, Term, Component
import funcs


def get_term(operation: str, operators: typing.Iterable,  start_index: int = 0) -> tuple[str]:
    returned_str: str = ""
    found_operators: bool = False 
    for i in range(start_index, len(operation)):
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


def is_complete(op: Operation, operators) -> bool:
    return not (math.isnan(op.first_term.get_result(operators)) or math.isnan(op.second_term.get_result(operators)))

def combine_operations(op1: Operation, op2: Operation, operators: dict) -> Operation:
    """merges two operations with the same priority level"""
    if is_complete(op1, operators) and is_complete(op2, operators):
        return None
    elif is_complete(op1, operators):
        if math.isnan(op2.first_term.get_result(None)):
            op2.first_term = op1
        else:
            op2.second_term = op1
        return op2
    else:
        if math.isnan(op1.first_term.get_result(None)):
            op1.first_term = op2
        else:
            op1.second_term = op2
        return op1


def merge_operations(operations: typing.Iterable[Operation], operators: dict) -> Operation:
    "merges len(operations) operations with the same priority level"
    if len(operations) < 2: 
        return operations[0]
  
    has_nan: list[Operation] = [i for i in operations if i.hasnan()]
    try:
        has_not_nan: Operation = tuple(i for i in operations if not i.hasnan())[0] # ps: il ne peut y en avoir qu'un
    except IndexError:
        final_op = has_nan[0]
    else:
        final_op = combine_operations(has_not_nan, has_nan[0], operators)
    
    if len(has_nan) > 1:
        for curr_op in has_nan[1::]:
            final_op = combine_operations(final_op, curr_op, operators)
    icecream.ic(final_op)
    return final_op


def place_at_nan(op1: Operation, op2: Operation) -> bool:
    """
    places op2 where these is nan in op1\n
    returns wether it found nan in a branch
    """
    if not op1.hasnan():
        return False
    
    if type(op1.first_term) == Operation:
        if place_at_nan(op1.first_term, op2) is True:
            return True
        else:
            place_at_nan(op1.second_term, op2  )    
    elif type(op1.first_term) == Term:
        if op1.first_term.hasnan():
            op1.first_term = op2
            return True

    if type(op1.second_term) == Operation:
        if place_at_nan(op1.second_term, op2) is True:
            return True
    elif type(op1.second_term) == Term:
        if op1.second_term.hasnan():
            op1.second_term = op2
            return True
        else:
            return False
    return False #on sait jamais
        

def get_operation(operation: str, operators: typing.Iterable, priorities: dict[str, int], parenthesis: bool = False) -> Operation:
    index = 0
    terms: list[str] = []
    operations: dict[int, list[Operation]] = dict.fromkeys(range(max(priorities.values()) + 1))

    # creating terms
    # in the form of: 5+5 -> ['5', '+', '5']
    while True: 
        term = get_term(operation, operators.keys(), index)
        if len(terms) > 0 and terms[-1] == term[0][0] == "-":# si ya un - opérateur puis un pour négatif
            term = (term[0][1::], term[1], term[2]) # on enlèle celui pour le négatif
        terms.append(term[0])
        index = int(term[1])
        if term[2] == "":
            break
        else:
            terms.append(term[2])
    icecream.ic(terms)
    
    if terms[0] in operators.keys() or not terms[0].isdigit():
        print(f"SyntaxError: \"{terms[0]}\"")
        quit(-1)

    #filling the operatons dict
    for index in range(max(priorities.values()), -1, -1):# de 2 à 0 généralement
        for i, term in enumerate(terms):# terms(5+5) -> (0, '5'), (1, '+'), (2, '5')
            if term in operators.keys() and 0 < i < len(terms) - 1 and priorities[term] == index:
                if operations[priorities[term]] is None: 
                    operations[priorities[term]] = []

                operations[priorities[term]].append(Operation(
                    Term(float(terms[i - 1])),
                    term,
                    Term(float(terms[i + 1])),
                    parenthesis=True)
                )
                terms[i - 1], terms[i], terms[i + 1] = str(math.nan), None, str(math.nan) #[i-1] -> 5, [i] -> +,     
            
            elif term not in operators.keys(): #tkt j'avis pas envie de rajouter une couche de if
                try: float(term)
                except ValueError:
                    print(f">> {term} n'est pas un chiffre")
                    quit(-1)
                except TypeError: pass
    

    #creating the binaty tree
    for index, value in operations.items():
        if value is not None:
            value = merge_operations(value, operators)
            value.parenthesis = True
            operations[index] = [value]
    icecream.ic(operations)
            
    #merging all the operatoins into one
    for i in reversed(range(max(priorities.values()))):
        print(i)
        if place_at_nan(operations[i][0], operations[i + 1][0]) is False:
            print(f">> Je sais pas comment t'as fait mais ya un problème ici -> {operations[i][0]}")
            quit(-1)
    icecream.ic(operations)
    return operations[min(priorities.values())][0]

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
        operation: Operation = get_operation(input(">> "), OPERATORS, PRIORITIES)
        result = operation.get_result(OPERATORS)
        print(f"> {result}")
        if "y" in input(">> quit <y/n> ? "):
            break



if __name__ == "__main__":
    main()
