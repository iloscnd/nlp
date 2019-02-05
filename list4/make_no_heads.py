import re

f = open("resources/skladnica_no_heads.txt", "w")

pattern = re.compile("\|\w* ")

for line in open("resources/skladnica_with_heads.txt", "r"):
    new_line = pattern.sub(" ", line,count=0)
    print(new_line, file=f)


