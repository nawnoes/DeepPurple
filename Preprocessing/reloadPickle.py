import pickle

with open('endGame.txt','rb') as f:
     endG=pickle.load(f)
with open('middleGame.txt', 'rb') as f:
    middleG = pickle.load(f)
with open('openGame.txt', 'rb') as f:
    openG = pickle.load(f)

print(endG)
print(middleG)
print(openG)