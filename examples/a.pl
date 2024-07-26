q(a) :- not q(a).
h(R) :- not p(R).
p(R) :- not R(a).
k :- h(q).