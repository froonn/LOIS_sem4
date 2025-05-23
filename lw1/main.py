from logical_interpreter import parse

try:
    first_formula = parse(input('Enter first formula: '))
    second_formula = parse(input('Enter second formula: '))

    print(first_formula == second_formula)
except:
    print('Invalid formula')