import math
import icecream
import typing
from trees import Operation, Term
import funcs





def has_no_nan(op: Operation) -> bool:
    if type(op.first_term) == Operation == type(op.second_term):
        return True
    elif type(op.first_term) == Term:
        return not (math.isnan(op.first_term.value))
    else:
        return not (math.isnan(op.second_term.value))


def combine_operations(op1: Operation, op2: Operation) -> Operation:
    """merges two operations with the same priority level"""
    if has_no_nan(op1):
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


def merge_operations(operations: typing.Iterable[Operation]) -> Operation:
    "merges len(operations) operations with the same priority level"
    if len(operations) < 2: 
        return operations[0]
  
    has_nan: list[Operation] = [i for i in operations if i.hasnan()]
    try:
        has_not_nan: Operation = tuple(i for i in operations if not i.hasnan())[0] # ps: il ne peut y en avoir qu'un
    except IndexError: #si y'en a pas 
        final_op = has_nan[0]
    else:
        final_op = combine_operations(has_not_nan, has_nan[0])
    
    if len(has_nan) > 1:
        for curr_op in has_nan[1::]:
            final_op = combine_operations(final_op, curr_op)
    return final_op


def place_at_nan(op1: Operation, op2: Operation) -> bool:
    """
    - places op2 where these is nan in op1\n
    - returns wether it found NaN in a branch
    """
    if not op1.hasnan():
        return False
    
    if type(op1.first_term) == Operation:
        if place_at_nan(op1.first_term, op2) is True:
            return True
        else:
            place_at_nan(op1.second_term, op2)    
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


def get_part(operation: str, operators: typing.Iterable,  start_index: int = 0) -> tuple[str]:
    returned_string: str = ""
    found_operators: bool = False 
    for i in range(start_index, len(operation)):
        char = operation[i]
        if char in (" ", "(", ")"):
            continue

        if char == "-" and returned_string == "":
            returned_string = "-"
            continue

        if char == ".":
            if "." not in returned_string:
                returned_string += "."
            else:
                raise ValueError(f"trop de points dans {returned_string}")
        
        if char.isdigit():
            returned_string += char

        if char in operators and not found_operators and i > start_index:
            return (returned_string, str(i), char)
        
    return (returned_string, str(i), "")


def get_parts(input_string: str, operators: typing.Iterable):
    index = 0   
    parts: list[str] = [] 
    while True: 
        part = get_part(input_string, operators, index)
        if len(parts) > 0 and parts[-1] == part[0][0] == "-":# si ya un - opérateur puis un pour négatif
            part = (part[0][1::], part[1], part[2]) # on enlèle celui pour le négatif
        parts.append(part[0])
        index = int(part[1])
        if part[2] == "":
            break
        else:
            parts.append(part[2])
    return parts

def get_operation(input_string: str, operators: typing.Iterable, priorities: dict[str, int], parenthesis: bool = False) -> Operation:
    
    expression_parts: list[str] = get_parts(input_string, operators)
    operations_dict: dict[int, list[Operation]] = dict.fromkeys(range(max(priorities.values()) + 1))

    # creating expression_parts
    # in the form of: 5+5 -> ['5', '+', '5']
    
    icecream.ic(expression_parts)
    
    if expression_parts[0] in operators or not expression_parts[0].isdigit():
        print(f"SyntaxError: \"{input_string}\"")
        quit(-1)

    #filling the operatons dict
    for index in range(max(priorities.values()), -1, -1):# de 2 à 0 généralement
        for i, part in enumerate(expression_parts):# expression_parts(5+5) -> (0, '5'), (1, '+'), (2, '5')
            if part in operators and 0 < i < len(expression_parts) - 1 and priorities[part] == index:
                if operations_dict[priorities[part]] is None: 
                    operations_dict[priorities[part]] = []

                operations_dict[priorities[part]].append(Operation(
                    Term(float(expression_parts[i - 1])),
                    part,
                    Term(float(expression_parts[i + 1])),
                    parenthesis=True)
                )
                expression_parts[i - 1], expression_parts[i], expression_parts[i + 1] = str(math.nan), None, str(math.nan) #ex[i-1] -> 5, ex[i] -> +,     
            
            elif part not in operators: #tkt j'avis pas envie de rajouter une couche de if
                try: float(part)
                except ValueError:
                    print(f">> {part} n'est pas un chiffre")
                    quit(-1)
                except TypeError: pass
    

    #creating the binaty tree
    icecream.ic(operations_dict)
    for index, value in operations_dict.items():
        if value is not None:
            value = merge_operations(value)
            value.parenthesis = True
            operations_dict[index] = [value]
    icecream.ic(operations_dict)
            
    #merging all the operatoins into one
    for i in reversed(range(max(priorities.values()))):
        icecream.ic(operations_dict[i], i)
        if place_at_nan(operations_dict[i][0], operations_dict[i + 1][0]) is False:
            print(f">> Je sais pas comment t'as fait mais ya un problème ici -> {operations_dict[i][0]}")
            print(">> Je crois je sais enft je travaille dessus")
            quit(1)


    icecream.ic(operations_dict[0])
    return operations_dict[min(priorities.values())][0]



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
        result: float = operation.get_result(OPERATORS)
        print(f"> {result}")
        if "y" in input(">> quit <y/n> ? "):
            break



if __name__ == "__main__":
    main()
