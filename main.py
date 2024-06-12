import sys
import argparse
from parser.parse import parse
from evaluator.double_program import transform_program
from evaluator.evaluate import initialize_over_approximation,initialize_under_approximation, atov

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

    r = dt_program.rules[0]
    l = r.body[0]
    atov(l, current_under_approximation, current_over_approximation)


if __name__ == "__main__":
    main()
