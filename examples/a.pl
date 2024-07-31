succ(0,1).
succ(1,2).
succ(2,3).
succ(3,4).
succ(4,5).
succ(5,6).
succ(6,7).
succ(7,8).
succ(8,9).


num(0).
num(Y) :- succ(X,Y), num(X).

even(X) :- num(X), succ(X,Y), not even(Y).
odd(X) :- not even(X).

num_2(X) :- even(X).
num_2(X) :- odd(X).


parent(a, b).
parent(a, c).
parent(b, d).
parent(c, e).

male(a).
male(b).
male(d).
female(c).
female(e).

sibling(X, Y) :- parent(Z, X), parent(Z, Y), not same_person(X, Y).

same_person(a, a).
same_person(b, b).
same_person(c, c).
same_person(d, d).
same_person(e, e).

grandparent(X, Y) :- parent(X, Z), parent(Z, Y).

uncle(X, Y) :- male(X), sibling(X, Z), parent(Z, Y).

aunt(X, Y) :- female(X), sibling(X, Z), parent(Z, Y).

cousin(X, Y) :- parent(Z, X), parent(W, Y), sibling(Z, W).
