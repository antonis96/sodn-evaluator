import sys
import argparse
from parser.parse import parse
from evaluator.double_program import transform_program
def main():
    parser = argparse.ArgumentParser(description='Datalog Program Parser')
    parser.add_argument('--input_file', required=True, help='Path to the Datalog program file')
    parser.add_argument('--output_file', help='Path to the output file')

    args = parser.parse_args()

    try:
        program = parse(args.input_file)
        dt_program, ndf_program = transform_program(program)
        print(dt_program)
        print("-----------------------------")
        print(ndf_program)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
