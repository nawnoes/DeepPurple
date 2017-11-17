fread =  open('count.txt','r')
c = fread.read()
c= int(c)

c += 1
f.write(str(c),)
f.close()
print(c)