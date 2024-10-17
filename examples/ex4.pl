p(a,b,c).

non_subset(P,Q) :- P(X), not Q(X).
subset(P,Q) :- not non_subset(P,Q).

same(P,Q) :- subset(P,Q), subset(Q,P).