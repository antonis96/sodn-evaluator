import copy
import argparse
from parser.parse import parse
from evaluator.double_program import transform_program
from evaluator.utils import (
    initialize_over_approximation,
    initialize_under_approximation, 
    evaluate_facts, 
    evaluate_tp,
    print_approximation,
    extract_herbrand_universe,
    evaluate_alternating_fp,
    filter_rules_without_idb_predicates
)

def main():
    parser = argparse.ArgumentParser(description='Datalog Program Parser')
    parser.add_argument('--input_file', required=True, help='Path to the Datalog program file')
    parser.add_argument('--output_file', help='Path to the output file')

    args = parser.parse_args()


    program = parse(args.input_file)
    dt_program, ndf_program = transform_program(program)

    herbrand_universe = extract_herbrand_universe(program)
    current_under_approximation = {
        predicate: initialize_under_approximation(dt_program, predicate)
        for predicate in dt_program.predicates
    }

    current_over_approximation = {
        predicate: initialize_over_approximation(ndf_program, predicate, herbrand_universe)
        for predicate in ndf_program.predicates
    }


    types = {**dt_program.types, **ndf_program.types}

    current_under_approximation = evaluate_facts(dt_program,current_under_approximation)
    current_over_approximation = evaluate_facts(ndf_program,current_over_approximation)
    filtered_dt_program = filter_rules_without_idb_predicates(dt_program,'dt')
    filtered_ndf_program = filter_rules_without_idb_predicates(ndf_program,'ndf')

    
    a,b = evaluate_alternating_fp(dt_program, ndf_program, types, current_under_approximation, current_over_approximation, herbrand_universe)
    print_approximation(a)
    print_approximation(b)
    # while True:
    #     question = input("?-  ")
        
    #     if question.lower() == 'exit':
    #         print("Exiting.")
    #         break
        
    #     answer = handle_query(question)
    #     print("Answer:", answer)


if __name__ == "__main__":
    main()
