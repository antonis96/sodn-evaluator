p(R) :- R(a).
q(R) :- not p(R).

k(a).

l :- p(k).
l1 :- q(k).