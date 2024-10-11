import argparse
import re
from parser.parse import parse
from evaluator.double_program import transform_program
from evaluator.utils import (
    initialize_approximation,
    evaluate_facts,
    get_approximation_string,
    extract_herbrand_universe,
)
from evaluator.evaluate_fixpoints import evaluate_alternating_fp

def main():
    parser = argparse.ArgumentParser(description='Datalog Program Parser')
    parser.add_argument('--input_file', required=True, help='Path to the Datalog program file')
    parser.add_argument('--output_file', help='Path to the output file')

    args = parser.parse_args()

    program = parse(args.input_file)
    dt_program, ndf_program = transform_program(program)

    import copy

    initial_program = copy.deepcopy(dt_program)
    initial_program.rules = [r for r in initial_program.rules if not any(l.atom.predicate.startswith("ndf") and not re.match(r"^ndf_[A-Z]", l.atom.predicate) for l in r.body)]


    herbrand_universe = extract_herbrand_universe(program)
    current_under_approximation = {
        predicate: initialize_approximation(dt_program, predicate)
        for predicate in dt_program.predicates
    }

    current_over_approximation = {
        predicate: initialize_approximation(ndf_program, predicate)
        for predicate in ndf_program.predicates
    }

    types = {**dt_program.types, **ndf_program.types}

    current_under_approximation = evaluate_facts(dt_program, current_under_approximation)
    current_over_approximation = evaluate_facts(ndf_program, current_over_approximation)

    dt, ndf = evaluate_alternating_fp(dt_program, ndf_program, initial_program, types, current_under_approximation, current_over_approximation, herbrand_universe)
    
    under_approx_str = get_approximation_string(dt)
    over_approx_str = get_approximation_string(ndf)

    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write("Under Approximation:\n")
            f.write(under_approx_str)
            f.write("\nOver Approximation:\n")
            f.write(over_approx_str)
    else:
        print("Under Approximation:")
        print(under_approx_str)
        print("Over Approximation:")
        print(over_approx_str)


if __name__ == "__main__":
    main()
