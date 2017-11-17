
f = open('fen.txt','r')

for i, line in enumerate(f):
    if i >2:
        print(line[:-1])