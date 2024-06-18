succ(0,1).
succ(1,2).
succ(2,3).

even(X) :- succ(X,Y), not even(Y).

