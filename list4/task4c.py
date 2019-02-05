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




##get types

def get_type(lhs):



    left = lhs.find("[")
    right = lhs.rfind("]")
    
    if left == -1:
        return None
    return lhs[left:right+1]


types = {}

for prod in productions:
    if nltk.grammar.is_terminal(prod.rhs()[0]):
       
        
        typ = get_type(str(prod.lhs()))

        if typ is None:
            continue

        #print(prod.rhs()[0])
        #print(prod)
        #print(typ)


        if typ not in types:
            types[typ] = []
        
        rhs = str(prod.rhs()[0])

        if rhs not in types[typ]:
            types[typ].append(rhs)





#print(types)

print("types ")



def generate_symbols(symbol, depth, parent):

    if nltk.grammar.is_terminal(symbol):
        
        typ = get_type(str(parent))
        if typ is None:
            #print(parent)
            new_symbol = str(symbol)
            typ = str(parent)
        else:
            new_symbol = random.choice(types[typ])


        return [typ, new_symbol], depth
    
    prods = grammar.productions(lhs=symbol)
    children = [ prod.rhs() for prod in prods ]
    probs = [prod.prob() for prod in prods]

    new_child  = random.choices(children, probs, k=1)[0]

    res = []
    depth_children = 0
    for child in new_child:
        res_child, depth_child = generate_symbols(child, depth + 1, symbol)
        res += res_child
        depth_children = max(depth_children, depth_child)

    return res, depth_children

def generate_with_length(l, d):

    depth = 0
    result = []

    while len(result) < l - 2 or len(result) > l + 2 or depth > d:
        #print(" ".join(result), "is bad getting new one")
        result, depth = generate_symbols(grammar.start(), -1, None)


    print(" ".join(result))



if __name__ == "__main__":
    
    generate_with_length(10, 4)

