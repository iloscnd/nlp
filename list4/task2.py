import nltk
import sys


grammar = open("list4/task2grammar.fcfg", "w")

print("%start S", file=grammar)
print("S -> NP[L=?l,P=?p,R=?r]", file=grammar)
print("NP[L=?l,P=?p,R=?r] -> NP[L=?l,P=?p,R=?r] NP[L=?l2,P=gen,R=?r2]", file=grammar)
print("NP[L=?l,P=?p,R=?r] -> ADJ[L=?l,P=?p,R=?r] NP[L=?l,P=?p,R=?r]", file=grammar)
print("NP[L=?l,P=?p,R=?r] -> NP[L=?l,P=?p,R=?r] ADJ[L=?l,P=?p,R=?r]", file=grammar)
print("NP[L=?l,P=?p,R=?r] -> N[L=?l,P=?p,R=?r]", file=grammar)



for line in open("list4/skladnicaTagsBases.pl", "r"):
    if line.find("subst:") > 0:
        word_begin = line.find("'")
        word_end = line.find("'", word_begin + 1)
        word = line[word_begin: word_end +1]       

        tag_begin = line.find("subst:")
        l = line[tag_begin + 6: tag_begin+8]
        p_end = line.find(":", tag_begin+9)
        p = line[tag_begin + 9: p_end]
        r = line[p_end+1: -3]
        print("N[L={},P={},R={}] -> {}".format(l,p,r, word), file=grammar)

    elif line.find("ger:") > 0:
        word_begin = line.find("'")
        word_end = line.find("'", word_begin + 1)
        word = line[word_begin: word_end +1]       

        tag_begin = line.find("ger:")
        l = line[tag_begin + 4: tag_begin+6]
        p_end = line.find(":", tag_begin+7)
        p = line[tag_begin + 7: p_end]
        r = line[p_end+1: line.find(":", p_end+1)]
        print("N[L={},P={},R={}] -> {}".format(l,p,r, word), file=grammar)

    elif line.find("adj:") > 0:
        word_begin = line.find("'")
        word_end = line.find("'", word_begin + 1)
        word = line[word_begin: word_end +1]       

        tag_begin = line.find("adj:")
        l = line[tag_begin + 4: tag_begin+6]
        p_end = line.find(":", tag_begin+7)
        p = line[tag_begin + 7: p_end]
        r = line[p_end+1: -7]
        print("ADJ[L={},P={},R={}] -> {}".format(l,p,r, word), file=grammar)

    elif line.find("ppas:") > 0:
        word_begin = line.find("'")
        word_end = line.find("'", word_begin + 1)
        word = line[word_begin: word_end +1]       
        tag_begin = line.find("ppas:")
        l = line[tag_begin + 5: tag_begin+7]
        p_end = line.find(":", tag_begin+8)
        p = line[tag_begin + 8: p_end]
        r = line[p_end+1: line.find(":", p_end+1)]
        print("ADJ[L={},P={},R={}] -> {}".format(l,p,r, word), file=grammar)
    else:
        pass
        word_begin = line.find("'")
        word_end = line.find("'", word_begin + 1)
        word = line[word_begin: word_end +1]       
        print("BAD ->", word, file=grammar)
grammar.close()
print("Grammar  generated", file=sys.stderr)


# nltk.data.show_cfg('list4/task2grammar.fcfg')
cp = nltk.load_parser('list4/task2grammar.fcfg', trace=0)

print("parser loaded", file=sys.stderr)


def parse_tokens(tokens):
    if len(tokens) >  5:
        return False

    try:
        num_trees =0
        for _ in cp.parse(tokens):
            num_trees += 1
            break
    except(ValueError):
        return False
    
    return num_trees > 0

for phrase in open("list4/phrases", "r"):
    
    tokens = phrase[2:-4].split("', '")
    if parse_tokens(tokens):
        print("GOOD:", end=" ")
    else:
        print("BAD:", end=" ")
    print(" ".join(tokens))

    


