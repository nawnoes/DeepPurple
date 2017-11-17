'''체스판의 각 위치를 64 bit onehot encoding으로 변환하기 위해 사용'''


'''
사전형 자료형에서 value로 key값 찾는 방법
(1)
for name, age in mydict.items(): #mydict에 아이템을 하나씩 접근해서, key, value를 각각 name, age에 저장
    if age == search_age:
        print name
(2)
[name for name, age in mydict.items() if age == search_age]

[예제]
dic={'name': 'pei', 'age': 12, 'love': 'who'}
for key,value in dic.items():
    if value == 'who':
	    print(key) # value로 key값을 얻어낼 수 있다.
'''
import numpy as np
import copy
import chess

class OneHotEncode:
    def __init__(self):
        self.row = ['a','b','c','d','e','f','g','h']
        self.colomn = ['1','2','3','4','5','6','7','8']
        self.position = chess.SQUARE_NAMES
        self.position4096 = []
        self.onehot = self.makeOneHot()
        self.onehot4096 = self.makeOneHot4096()

    def all(self):
        for i in range(64):
            print("index ",i," =",self.position[i])

    def makeOneHot(self):
        #position에 명령어들을 리스트로 입력한다.
        onehot=np.eye(64)
        dic = {}
        for i in range(64):
            dic[self.position[i]]=onehot[i]
        return dic

    def makeOneHot4096(self):
        #position에 명령어들을 리스트로 입력한다.
        startPosition = copy.deepcopy(self.position)
        endPosition = copy.deepcopy(startPosition)
        onehot4096=np.eye(4096)

        dic = {}
        k=0
        for i in range(64):
            for j in range(64):
                move = startPosition[i]+endPosition[j]
                moveIndex = k
                dic[move]=onehot4096[moveIndex]
                self.position4096.append(move)
                # print("move : ",move, " index : ",moveIndex)
                k+=1

        # print("move : ", move, " index : ", moveIndex , " k: ",k)
        return dic

    def uciMoveToOnehot(self,move):
        #uci명령어 move를 입력 받아 4096bit의 one hot을 반환
        return np.ndarray.tolist(self.onehot4096[move[:4]])

    def moveToOnehot(self,move):
        #move를 입력 받아 64bit One Hot을 반환
        return self.onehot[move]

    def moveToIndex(self,move):
        #move가 들어있는 index를 0~63의 숫자로 반환
        return self.position.index(move)

    def onehot(self):
        return self.onehot

    def onehotToMove(self, onehot):
        #Onehot을 Move로 바꿔주는 함수
        #onehot = [0,0,0,...,1,0,...] -> 'h7'으로 바꿔줌
        for move, oh in self.onehot.items():
            if np.array_equal(oh,onehot):
                return move
    def onehotToMove4096(self, onehot):
        #Onehot을 Move로 바꿔주는 함수
        #onehot = [0,0,0,...,1,0,...] -> 'h7'으로 바꿔줌
        for move, oh in self.onehot4096.items():
            if np.array_equal(oh,onehot):
                return move

    def indexToMove(self, x ):
        #0~63사이의 index를 입력하면 move를 반환해준다
        return self.position[x]
    def indexToMoveXY(self,x,y):
        #0~7 사이의 index 2개를 입력하면 해당 좌표의 move를 반환
        return self.position[ (x+1)*(y+1)-1]

    def indexToMove4096(self, index ):
        #0~63사이의 index를 입력하면 move를 반환해준다
        return self.position4096[index]


