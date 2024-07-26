import copy
import argparse
from parser.parse import parse
from evaluator.double_program import transform_program
from evaluator.evaluate import (
    initialize_over_approximation,
    initialize_under_approximation, 
    evaluate_facts, 
    process_rules,
    print_approximation,
    compare_dicts_of_dataframes,
    handle_query,
    filter_rules_without_idb_predicates
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
    filtered_dt_program = filter_rules_without_idb_predicates(dt_program,'dt')
    filtered_ndf_program = filter_rules_without_idb_predicates(ndf_program,'ndf')

    new_over_approximation = process_rules(filtered_ndf_program, types, current_under_approximation, current_over_approximation, 'ndf') 
    new_under_approximation = process_rules(filtered_dt_program, types, current_under_approximation, current_over_approximation, 'dt')


    current_under_approximation = copy.deepcopy(new_under_approximation)
    current_over_approximation = copy.deepcopy(new_over_approximation)

    for i in range(0,5):
    # while True:

        new_over_approximation = process_rules(ndf_program, types, current_under_approximation, current_over_approximation, 'ndf')
        new_under_approximation = process_rules(dt_program, types, current_under_approximation, current_over_approximation, 'dt')
        # print("Edw")
        # if compare_dicts_of_dataframes(current_under_approximation, new_under_approximation) and True: # compare_dicts_of_dataframes(current_over_approximation, new_over_approximation):
        #     break
        
        current_under_approximation = copy.deepcopy(new_under_approximation)
        current_over_approximation = copy.deepcopy(new_over_approximation)
        

    print_approximation(current_under_approximation)
    print_approximation(current_over_approximation)


    # while True:
    #     question = input("?-  ")
        
    #     if question.lower() == 'exit':
    #         print("Exiting.")
    #         break
        
    #     answer = handle_query(question)
    #     print("Answer:", answer)


if __name__ == "__main__":
    main()
