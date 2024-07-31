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