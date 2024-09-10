p(a,b).
tc(R,X,Y) :- R(X,Y).
tc(R,X,Y) :- R(X,Z), tc(R,Z,Y).