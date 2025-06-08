import time
from logical_interpreter import parse

while True:
    try:
        first_formula_str = input('Enter first formula: ')
        if first_formula_str.lower() == 'exit':
            break
        start_time_1 = time.perf_counter()
        first_formula = parse(first_formula_str)
        end_time_1 = time.perf_counter()
        parse_time_1 = (end_time_1 - start_time_1) * 1000
        print(f'Time to parse first formula: {parse_time_1:.4f} ms')

        second_formula_str = input('Enter second formula: ')
        if second_formula_str.lower() == 'exit':
            break
        start_time_2 = time.perf_counter()
        second_formula = parse(second_formula_str)
        end_time_2 = time.perf_counter()
        parse_time_2 = (end_time_2 - start_time_2) * 1000
        print(f'Time to parse second formula: {parse_time_2:.4f} ms')

        start_time_compare = time.perf_counter()
        are_equivalent = (first_formula == second_formula)
        end_time_compare = time.perf_counter()
        compare_time = (end_time_compare - start_time_compare) * 1000
        print(f'Time to compare formulas: {compare_time:.4f} ms')

        print('Formulas are equivalent\n' if are_equivalent else 'Formulas are not equivalent\n')

    except SyntaxError as e:
        print(f'Invalid formula: {e}\n')
    except Exception as e:
        print(f'An unexpected error occurred: {e}\n')
