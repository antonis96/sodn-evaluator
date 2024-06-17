from typing import *
from components import *


def add_prefixed_fact(program: Program, prefix: str, fact: Fact) -> None:
    predicate = f"{prefix}_{fact.head.predicate}"
    new_fact = Fact(PredicateHead(predicate, fact.head.args))
    program.add_fact(new_fact)

def transform_rule(rule: Rule, dt_program: Program, ndf_program: Program) -> None:
    head = rule.head
    body = rule.body
    
    dt_head = PredicateHead(f"dt_{head.predicate}", head.args)
    ndf_head = PredicateHead(f"ndf_{head.predicate}", head.args)

    dt_body = []
    ndf_body = []

    for literal in body:
        predicate = literal.atom.predicate
        args = literal.atom.args
        negated = literal.negated

        if not literal.atom.predicate.islower(): # if we have a predicate variable
            dt_body.append(literal)
            ndf_body.append(literal)
            continue
            
        if negated:
            dt_body.append(Literal(Atom(f"ndf_{predicate}", args, literal.atom.predicate_type), negated=True))
            ndf_body.append(Literal(Atom(f"dt_{predicate}", args, literal.atom.predicate_type), negated=True))
        else:
            dt_body.append(Literal(Atom(f"dt_{predicate}", args, literal.atom.predicate_type)))
            ndf_body.append(Literal(Atom(f"ndf_{predicate}", args, literal.atom.predicate_type)))

    dt_rule = Rule(dt_head, dt_body)
    ndf_rule = Rule(ndf_head, ndf_body)

    dt_program.add_rule(dt_rule)
    ndf_program.add_rule(ndf_rule)

def transform_program(program: Program) -> Tuple[Program, Program]:
    dt_program = Program(
        types={f"dt_{k}": t for k, t in program.types.items()},
        predicates=[f"dt_{p}" for p in program.predicates]
    )
    ndf_program = Program(
        types={f"ndf_{k}": t for k, t in program.types.items()},
        predicates=[f"ndf_{p}" for p in program.predicates]
    )
    for fact in program.facts:
        add_prefixed_fact(dt_program, "dt", fact)
        add_prefixed_fact(ndf_program, "ndf", fact)

    for rule in program.rules:
        transform_rule(rule, dt_program, ndf_program)

    return dt_program, ndf_program
