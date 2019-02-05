import nltk
import random

from nltk.corpus import BracketParseCorpusReader
from nltk import induce_pcfg

treebank = BracketParseCorpusReader("resources/","skladnica_no_heads.txt", )

productions = []
for item in treebank.fileids()[:2]:
    for tree in treebank.parsed_sents(item):
        #tree.draw()
        productions += tree.productions()

grammar = induce_pcfg(nltk.Nonterminal('wypowiedzenie:'), productions)
print(grammar.start())
#print(grammar.productions())
#print(grammar._lhs_index)
#print(grammar.productions(lhs=grammar.start()))


def generate_symbols(symbol, depth):

    if nltk.grammar.is_terminal(symbol):
        return [str(symbol)], depth
    
    prods = grammar.productions(lhs=symbol)
    children = [ prod.rhs() for prod in prods ]
    probs = [prod.prob() for prod in prods]

    new_child  = random.choices(children, probs, k=1)[0]

    res = []
    depth_children = 0
    for child in new_child:
        res_child, depth_child = generate_symbols(child, depth + 1)
        res += res_child
        depth_children = max(depth_children, depth_child)

    return res, depth_children

def generate_with_length(l, d):

    depth = 0
    result = []

    while len(result) < l - 1 or len(result) > l + 1 or depth > d:
        #print(" ".join(result), "is bad getting new one")
        result, depth = generate_symbols(grammar.start(), -1)


    print(" ".join(result))



if __name__ == "__main__":
    
    for i in range(15):
        generate_with_length(7, 4)

