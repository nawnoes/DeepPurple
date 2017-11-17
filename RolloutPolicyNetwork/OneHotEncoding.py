'''
20일 알파고 모델 학습시키기 위해 사용 
testSym으로 확인 결과 이상 없음.
'''


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
        self.symcolomn= ['8','7','6','5','4','3','2','1']
        self.position = chess.SQUARE_NAMES
        self.symPosition = self.makeSymPosition()  # a8~h1까지
        self.position4096 = []
        self.symMove4096 = []
        self.onehot4096 = self.makeOneHot4096()
        self.symOnehot4096 = self.makeSymmetryOnehot4096()


    def all(self):
        for i in range(64):
            print("index ",i," =",self.position[i])

    def makeOneHot4096(self):
        #position에 명령어들을 리스트로 입력한다.
        startPosition = copy.deepcopy(self.position)
        endPosition = copy.deepcopy(self.position)
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

    def makeSymmetryOnehot4096(self):
        startPosition = copy.deepcopy(self.symPosition)
        endPosition = copy.deepcopy(self.symPosition)
        onehot = np.eye(4096)
        dic = {}
        k = 0
        for i in range(64):
            for j in range(64):
                move = startPosition[i] + endPosition[j]
                moveIndex = k
                dic[move] = onehot[moveIndex]
                self.symMove4096.append(move)
                # print("move : ",move, " index : ",moveIndex)
                k += 1
        # print("move : ", move, " index : ", moveIndex , " k: ",k)
        return dic
    #4096에서 사용
    def uciMoveToOnehot(self,move):
        #uci명령어 move를 입력 받아 4096bit의 one hot을 반환
        return np.ndarray.tolist(self.onehot4096[move[:4]])
    def moveToSymmetryOnehot(self,move):
        return np.ndarray.tolist(self.symOnehot4096[move])

    def move2symmetryMove(self, move):
        index = self.position4096.index(move)
        return self.symMove4096[index]

    def symmetryMove2move(self, symMove):
        index = self.symMove4096.index(symMove)
        return self.position4096[index]

    def get4096Position(self):
        return self.position4096

    def getSymPosition(self):
        return self.symMove4096

    def makeSymPosition(self):
        startPosition = []
        # 64개의 대칭 포지션 생성
        for i in self.symcolomn:
            for j in self.row:
                startPosition.append(j + i)
        return startPosition


    def onehotToMove4096(self, onehot):
        #Onehot을 Move로 바꿔주는 함수
        #onehot = [0,0,0,...,1,0,...] -> 'h7'으로 바꿔줌
        for move, oh in self.onehot4096.items():
            if np.array_equal(oh,onehot):
                return move
    def onehotToSymmetryMove4096(self, onehot):
        #Onehot을 Move로 바꿔주는 함수
        #onehot = [0,0,0,...,1,0,...] -> 'h7'으로 바꿔줌
        for move, oh in self.symOnehot4096.items():
            if np.array_equal(oh,onehot):
                return move

    def indexToMove4096(self, index ):
        #0~63사이의 index를 입력하면 move를 반환해준다
        return self.position4096[index]


