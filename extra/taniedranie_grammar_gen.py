import nltk

import sys
import random

import re

s1 = re.compile("[aeiouöóyęą]")
s2 = re.compile("i[aeouöęą]")
def syllabicator(word):
    if word in ".,;:'\"-=!?()\\":
        return 0
    
    return len(s1.findall(word)) -len(s2.findall(word))

suffix_ = re.compile("[^aeiouóöyęą]*[aeioöuóyęą][^aeioöuóyęą]+[aeioöuóyęą]")
def get_suffix(word, syllabs):
    if syllabs == 1:
        match = s1.search(word)
        start = word.find(match.group(0))
        return word[start:].encode('ascii',errors='replace').decode().replace("?","o")
    match = suffix_.search(word[::-1])
    if match:
        start =  word.rfind(match.group(0)[::-1])
        return word[start:].encode('ascii',errors='replace').decode().replace("?","o")
    else:
        return word.encode('ascii',errors='replace').decode().replace("?","o")


def tag_parse(line):
    #tagAndBase(slowo, forma podstawowa, tagi ).
    #print(line)
    
    word, base, tags = line.split(", ")
    word = word[12:-1]
    base = base[1:-1]
    tags = tags[:-3].split(':')

    word = word.replace("\'", "")

    return word, base, tags[0], tags[1:]


    



grammar = open("extra/tanie_dranie_grammar.fcfg", "w")

print("%start S", file=grammar)
print("S -> D D D K", file=grammar)
print("K -> GER ADJ[S=2] DRAN 'endl' V[L=sg,O=ter,T=imperf,S=4] 'tani drań endl '", file=grammar)


rymy = {}
for line in open("list4/skladnicaTagsBases.pl", "r"):
    word, base, typ, tags = tag_parse(line)

    if not all(x.isalpha() for x in word):
        continue

    syllabs = syllabicator(word)
    suffix = get_suffix(word, syllabs)

    if typ == "ger": 
        if syllabs == 4 and tags[0] == 'sg' and tags[1] == 'nom' and tags[3] == 'perf':
            print("GER -> '{}'".format(word), file=grammar)
    elif typ == "fin":
        if syllabs == 4:
            print("V[L={},O={},T={},S={}] -> '{}'".format(tags[0], tags[1], tags[2], syllabs, word), file=grammar)
    elif typ == "subst":
        if tags[0] == 'sg' and tags[1] == 'gen' and tags[2] == 'm1' and syllabs <=5:
            print("N[S={}] -> '{}'".format(syllabs, word), file=grammar)                
            rymy[suffix] = rymy.get(suffix, 0) + 1
            print("N[S={},RYM={}] -> '{}'".format(syllabs, suffix, word), file=grammar)
        if tags[1] == 'gen' and syllabs == 1 and word[-2:] == "ań":
            print("DRAN -> '{}'".format(word), file=grammar)

    elif typ == "adj":
        if tags[0] == 'pl' and tags[1] == 'gen' and tags[2] == 'm1' and syllabs <=5:
            print("ADJ[S={}] -> '{}'".format(syllabs, word), file=grammar)
        

for rym in rymy:
    if rymy[rym] == 1:
        continue
    print("D -> D[RYM={}]".format(rym), file=grammar)
    print("D[RYM={}] -> W[RYM={}] 'endl' W[RYM={}] 'endl'".format(rym,rym,rym), file=grammar)
    print("W[RYM={}] -> GER N[S=2] 'w' N[S=2,RYM={}]".format(rym,rym), file=grammar)
    print("W[RYM={}] -> GER N[S=2] 'z' N[S=2,RYM={}]".format(rym,rym), file=grammar)
    print("W[RYM={}] -> GER 'przez' N[S=3, RYM={}]".format(rym,rym), file=grammar)

grammar.close()
print("Grammar  generated", file=sys.stderr)



grammar = nltk.load('extra/tanie_dranie_grammar.fcfg', format="fcfg", verbose=False)
grammar = nltk.induce_pcfg(grammar.start(), grammar.productions())

print("grammar loaded")


def generate(symbol):


    if nltk.grammar.is_terminal(symbol):
        return [symbol]
    
    prods = grammar.productions(lhs=symbol)
    children = [ prod.rhs() for prod in prods ]
    probs = [prod.prob() for prod in prods]
    print(symbol)
    new_prod  = random.choices(children, probs, k=1)[0]

    res = []
    for child in new_prod:
        res += generate(child)
    return res
    



if __name__ == "__main__":
    
    done = False
    i = 0
    while not done:
        try:
            print(" ".join(generate(grammar.start())).replace("endl ","\n"), end="")
            done  = True
        except:
            print(i)
            i +=1 
