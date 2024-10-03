import math
from typing import Tuple

import icecream
import typing
from trees import ExpressionTree, Term
from simpleOperation import StringOperation
import funcs


def get_part(operation: str, operators: typing.Iterable, start_index: int = 0) -> tuple[str, str, str]:
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


def get_parts(input_string: str, operators: typing.Iterable) -> list[str]:
    """
    creating expression_parts
    in the form of: 5+5 -> ['5', '+', '5']
    """

    index = 0
    parts: list[str] = []
    while True:
        part = get_part(input_string, operators, index)
        if len(parts) > 0 and parts[-1] == part[0][0] == "-":  # si ya un - opérateur puis un pour négatif
            part = (part[0][1::], part[1], part[2])  # on enlèle celui pour le négatif
        parts.append(part[0])
        index = int(part[1])
        if part[2] == "":
            break
        else:
            parts.append(part[2])
    return parts


def get_operation(input_string: str, operators: typing.Iterable, priorities: dict[str, int],
                  parenthesis: bool = False) -> ExpressionTree | None:
    if input_string == "":
        print(">> Entrée vide")
        return None

    expression_parts: list[str] = get_parts(input_string, operators)
    string_operations: dict[int, list[StringOperation]] = dict.fromkeys(range(max(priorities.values()) + 1))

    if expression_parts[0] in operators or not expression_parts[0].isdigit():
        print(f"SyntaxError: \"{input_string}\"")
        quit(-1)

    #filling the operations dict
    for index in range(max(priorities.values()), -1, -1):  # de 2 à 0 généralement
        for i, part in enumerate(expression_parts):  # expression_parts(5+5) -> (0, '5'), (1, '+'), (2, '5')
            if part in operators and 0 < i < len(expression_parts) - 1 and priorities[part] == index:
                if string_operations[priorities[part]] is None:
                    string_operations[priorities[part]] = []

                j = len(string_operations[priorities[part]])

                string_operations[priorities[part]].append(StringOperation(
                    expression_parts[i - 1],
                    part,
                    expression_parts[i + 1]
                ))
                expression_parts[i - 1], expression_parts[i], expression_parts[
                    i + 1] = f"@{index}{j}", None, f"@{index}{j}"  # ex[i-1]=5, ex[i]=+, ex[i+1]=5

            elif part not in operators and part is not None and part[
                0] != "@":  #tkt j'avis pas envie de rajouter une couche de if
                try:
                    float(part)
                except ValueError:
                    print(f">> {part} n'est pas un chiffre")
                    quit(-1)
                except TypeError:
                    pass

    #creating the binaty tree
    expressions_dict: dict[int, list[ExpressionTree]] = {i: [None] for i in range(max(priorities.values()) + 1)}

    for i in range(max(priorities.values()) + 1)[::-1]:
        if string_operations[i] is None:
            continue

        for j, op in enumerate(string_operations[i]):
            icecream.ic(string_operations, expressions_dict, (i, j))
            print()
            if op.operator == "@":
                continue

            if op.first[0] == "@":
                first_term = get_value(string_operations, expressions_dict, op.first)
                set_value(string_operations, op.first, (str(i), "@", str(0)))
            else:
                first_term = Term(float(op.first))

            if op.second[0] == "@":
                second_term = get_value(string_operations, expressions_dict, op.second)
                set_value(string_operations, op.second, (str(i), "@", str(0)))
            else:
                second_term = Term(float(op.second))

            expressions_dict[i][0] = ExpressionTree(
                first_term,
                op.operator,
                second_term,
                True
            )

    icecream.ic(string_operations, expressions_dict)
    final_expression = expressions_dict[min(priorities.values())][-1]
    final_expression.set_parenthesis(True)
    icecream.ic(final_expression)
    return final_expression


def get_value(string_operations: dict[int, list[StringOperation]], expressions_dict: dict[int, list[ExpressionTree]],
              str_ptr: str) -> ExpressionTree:
    if str_ptr[0] != "@":
        raise ValueError(f"\"{str_ptr}\" does not contain @ at the beginning")
    elif len(str_ptr) != 3:
        raise ValueError(f"\"{str_ptr}\" has not a lenght of 3")

    str_op: StringOperation = string_operations[int(str_ptr[1])][int(str_ptr[2])]
    if str_op.operator == "@":
        return expressions_dict[int(str_op.first)][int(str_op.second)]

    if str_op.first[0] == "@":
        f = get_value(string_operations, expressions_dict, str_op.first)
    else:
        f = Term(float(str_op.first))

    if str_op.second[0] == "@":
        s = get_value(string_operations, expressions_dict, str_op.second)
    else:
        s = Term(float(str_op.second))

    return ExpressionTree(f, str_op.operator, s)


def set_value(string_operations: dict[int, list[StringOperation]], str_ptr: str, value: tuple[str, str, str]):
    if str_ptr[0] != "@":
        raise ValueError(f"\"{str_ptr}\" does not contain @ at the beginning")
    elif len(str_ptr) != 3:
        raise ValueError(f"\"{str_ptr}\" has not a lenght of 3")

    string_operations[int(str_ptr[1])][int(str_ptr[2])] = StringOperation(*value)


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
        operation: ExpressionTree = get_operation(input(">> "), OPERATORS.keys(), PRIORITIES)
        result: float = operation.get_result(OPERATORS)
        print(f"> {result}")
        if "y" in input(">> quit <y/n> ? "):
            break


if __name__ == "__main__":
    main()
