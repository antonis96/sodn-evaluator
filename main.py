import copy
import argparse
from parser.parse import parse
from evaluator.double_program import transform_program
from evaluator.evaluate import (
    initialize_over_approximation,
    initialize_under_approximation, 
    evaluate_facts, 
    variable_predicate_atov,
    combine_literal_evaluations
)

def main():
    parser = argparse.ArgumentParser(description='Datalog Program Parser')
    parser.add_argument('--input_file', required=True, help='Path to the Datalog program file')
    parser.add_argument('--output_file', help='Path to the output file')

    args = parser.parse_args()


    program = parse(args.input_file)
    dt_program, ndf_program = transform_program(program)

    current_under_approximation = {
        predicate: initialize_under_approximation(dt_program, predicate)
        for predicate in dt_program.predicates
    }

    current_over_approximation = {
        predicate: initialize_over_approximation(ndf_program, predicate)
        for predicate in ndf_program.predicates
    }


    types = {**dt_program.types, **ndf_program.types}
    current_under_approximation = evaluate_facts(dt_program,current_under_approximation)
    current_over_approximation = evaluate_facts(ndf_program,current_over_approximation)

    rule = dt_program.rules[0]
    evals = []
    for l in rule.body:
        v = variable_predicate_atov(l)
        evals.append(variable_predicate_atov(l))
    
    a = combine_literal_evaluations(evals)
    print(a)
    # # while True:

    #     new_over_approximation = process_rules(ndf_program, types, current_under_approximation, current_over_approximation, 'ndf')
    #     new_under_approximation = process_rules(dt_program, types, current_under_approximation, current_over_approximation, 'dt')
       
    #     if compare_dicts_of_dataframes(current_under_approximation, new_under_approximation) and compare_dicts_of_dataframes(current_over_approximation, new_over_approximation):
    #         break

    #     current_under_approximation = copy.deepcopy(new_under_approximation)
    #     current_over_approximation = copy.deepcopy(new_over_approximation)


    #     print_approximation(current_under_approximation)
    #     print_approximation(current_over_approximation)

if __name__ == "__main__":
    main()
