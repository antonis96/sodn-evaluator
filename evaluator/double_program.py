from typing import *
from components import *
def is_constant_predicate(literal: Literal) -> bool:
    return literal.predicate.islower()

def tau(term: Union[Atom, Literal, PredicateHead, Argument]) -> Union[Atom, Literal, PredicateHead, Argument]:
    if isinstance(term, Argument):
        # For every term t: τ(t) = t
        return term
    elif isinstance(term, Atom):
        # For every literal l: τ(l(t1, ..., tn))
        predicate, args = term.predicate, term.args
        if is_constant_predicate(term):
            # l' (τ(t1), ..., τ(tn)) if l is constant predicate
            primed_predicate = f"ndf_{predicate}"
            return Atom(primed_predicate, [tau(arg) for arg in args], term.predicate_type)
        else:
            # l (τ(t1), ..., τ(tn)) if l is variable predicate
            return Atom(predicate, [tau(arg) for arg in args], term.predicate_type)
    elif isinstance(term, Literal):
        atom = term.atom
        transformed_atom = tau(atom)
        return Literal(transformed_atom, term.negated)
    elif isinstance(term, PredicateHead):
        predicate, args = term.predicate, term.args
        if is_constant_predicate(term):
            primed_predicate = f"ndf_{predicate}"
            return PredicateHead(primed_predicate, [tau(arg) for arg in args])
        else:
            return PredicateHead(predicate, [tau(arg) for arg in args])
    return term

def transform_rule_dt(rule: Rule) -> Rule:
    head, body = rule.head, rule.body
    new_body = []
    for literal in body:
        if literal.negated:
            negated_literal = literal.atom
            new_body.append(Literal(tau(negated_literal), negated=True))
        else:
            new_body.append(literal)
    return Rule(head, new_body)

def transform_rule_ndf(rule: Rule) -> Rule:
    head, body = rule.head, rule.body
    new_head = tau(head)
    new_body = []
    for literal in body:
        if literal.negated:
            new_body.append(literal)
        else:
            new_body.append(Literal(tau(literal.atom)))
    return Rule(new_head, new_body)

def transform_program(program: Program) -> Tuple[Program, Program]:
    dt_program = Program()
    ndf_program = Program()
    for rule in program.rules:
        dt_program.add_rule(transform_rule_dt(rule))
        ndf_program.add_rule(transform_rule_ndf(rule))
    for fact in program.facts:
        dt_program.add_fact(fact)
        ndf_program.add_fact(Fact(tau(fact.head)))
    return dt_program, ndf_program