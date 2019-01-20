%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Dictionary
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


:- [skladnicaTagsBases].

hasTag(Word, Tag) :- tagAndBase(Word,_Base,Tag).

hasTag(w, prep:loc).
 
:- op(1050, xfx, ==>).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% GRAMMAR
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


likeAdj(adj:L:P:R:_, L, P, R).
likeAdj(ppas:L:P:R:_, L, P, R).
likeAdj(pact:L:P:R:_, L, P, R).

likeSubst(subst:L:P:R, L, P, R).
likeSubst(ger:L:P:R, L, P, R).
likeSubst(depr:L:P:R, L, P, R).

numBrev(brev:PUN, Abbr, L, P, R, T) :- tagAndBase(Abbr, Base, brev:PUN), tagAndBase(_, Base, num:L:P:R:T).


np(L,P,R) ==> adj(L,P,R), np(L,P,R).
np(L,P,R) ==> np(L, P, R), adj(L,P,R).
np(L,P,R) ==> np(L,P,R), prep(P2), np(_,P2,_).
np(L,P,R) ==> num(L,P,R, congr), np(L,P,R).
np(L,P,R) ==> num(L,P,R, rec), np(L,gen,R).
np(L,P,R) ==> np(L,P,R), np(_,gen,_).


np(pl,P,R1) ==> np(_,P,R1), [i], np(_,P,_R2).
np(pl,P,R1) ==> np(_,P,R1), [,], np(_,P,_R2).

np(L,P,R) ==> [X], {hasTag(X,Tag), likeSubst(Tag, L, P, R)}.
%np(L,P,R) ==> [X], {hasTag(X,subst:L:P:R)}.
%np(L,P,R) ==> [X], {hasTag(X,ger:L:P:R)}.
%np(L,P,R) ==> [X], {hasTag(X,depr:L:P:R)}.


np(L,P,R) ==> num(L,P,R, _), ['zł'].
np(L,P,R) ==> num(L,P,R, _), ['r'], ['.'].


adj(L,P,R) ==> adj(L,P,R), [i], adj(L,P,R).
adj(L,P,R) ==> adj(L,P,R), [,], adj(L,P,R).
adj(L,P,R) ==> [X], {hasTag(X, Tag), likeAdj(Tag,L,P,R)}.

prep(P) ==> [X], {hasTag(X, prep:P)}.
prep(P) ==> [X], {hasTag(X, prep:P:wok)}.

num(L, P, R, T) ==> [X], {hasTag(X, num:L:P:R:T)}.

num(L,P,R, T) ==> [Abbr], ['.'], {numBrev(brev:pun, Abbr, L, P, R, T)}.
num(L,P,R, T) ==> [Abbr], {numBrev(brev:npun, Abbr, L, P, R, T)}.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Parse
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
commasToList((X,Y), [X|Rest]) :- 
   !, commasToList(Y,Rest).
commasToList(X,[X]).   


allign( [[W]| Rest], [W|T], Alligment) :-
   !,allign(Rest, T, Alligment). 
allign( [At|Rest], Ts, [ (At,Pref) | ARest]):-
   Pref = [_|_],
   append(Pref, RestT, Ts),
   allign(Rest, RestT, ARest).
allign( [{C}], [], []) :- C.
allign( [], [], []).


   
parse(A,TokensToParse) :-
   (A ==> Right),
   commasToList(Right, ListRight),
   allign(ListRight, TokensToParse, Alligment),
   parsePairs(Alligment).
   
parsePairs([]).
parsePairs([(A,L)| Rest]):-
   parse(A,L),
   parsePairs(Rest).

writeList([A]) :- write(A),!.
writeList([A|As]):- write(A), write(' '),writeList(As).
   
parse0 :-
   %see('list4/phrases'),
   parsing.
   %seen.

parsing :-
   repeat,
   read(L),
   analyze(L),
   L = end_of_file,!.

analyze(end_of_file) :-
   write('DONE!'), nl, !.
analyze(L) :-   
   length(L,N),
   N < 12,
   parse(np(_,_,_), L),
   write('GOOD:'),
   writeList(L),nl,
   !.
analyze(L) :-
   write('BAD:'),
   writeList(L),nl,
   !.


:- parse0, halt.
