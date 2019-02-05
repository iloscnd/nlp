import nltk
import random

from nltk.corpus import BracketParseCorpusReader
from nltk import induce_pcfg

treebank = BracketParseCorpusReader("resources/","skladnica_with_heads.txt", )

productions = []
for item in treebank.fileids()[:2]:
    for tree in treebank.parsed_sents(item):
        #tree.draw()
        productions += tree.productions()

grammar = induce_pcfg(nltk.Nonterminal('wypowiedzenie:|'), productions)
print(grammar.start())
#print(grammar.productions())
#print(grammar._lhs_index)
#print(grammar.productions(lhs=grammar.start()))

#print(grammar.productions(lhs=nltk.Nonterminal("wypowiedzenie:|mogę")))
#print(grammar.productions(lhs=nltk.Nonterminal("znakkonca:|.")))

used_symbols = []
def generate_symbols(symbol):

    if nltk.grammar.is_terminal(symbol):

        used_symbols.append(symbol)
        
        return [str(symbol)]
    
    prods = grammar.productions(lhs=symbol)
    children = [ prod.rhs() for prod in prods ]
    probs = [prod.prob() for prod in prods]

    max_iters = 5
    iters = 0
    good = False

    while not good and iters < max_iters:
        iters += 1    

        new_child  = random.choices(children, probs, k=1)[0]
        good = True
        for child in new_child:
            if child in used_symbols:
                good = False
                break


    res = []
    for child in new_child:
        res += generate_symbols(child)
    return res

def generate_with_word(start_word):
    start_symbol = nltk.Nonterminal("wypowiedzenie:|"+start_word)

    result = generate_symbols(start_symbol)

    print(" ".join(result))



good_start_words = []

for line in open("resources/skladnica_with_heads.txt", "r"):
    e = line.find(" ")
    s = len("(wypowiedzenie:|")
    
    good_start_words.append(line[s:e])


if __name__ == "__main__":
    

    for i in range(15):
        generate_with_word(random.choice(good_start_words))

