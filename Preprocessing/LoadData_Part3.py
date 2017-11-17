import chess.pgn
import Board2Array as BA
from OneHotEncoding import OneHotEncode as OHE
import copy
import sys
import pickle
'''
사용법 :

 # 폴더경로를 이용해 rd객체 하나를 생성
rd = pgn_reader('./test/test.pgn')

# get_data()메소드를 이용하면, index 몇번쨰 수인지, input 보드상태, output 명령어, r 승패결과
#index는 명령어가 몇번째 둔 수인지 나타내는 숫자. 홀수면 백, 짝수면 흑.
index, input, output, r = rd.get_data()


'''

def read_games(f): # pgn파일을 불러와 한 게임 별로 배열로 만들어 리턴함
    gs = []
    i=0
    print("\nPgn 배열로 변환!")
    while True:
        try:
            g = chess.pgn.read_game(f)
            gs.append(g) # 현재 포인터가 가르키는 게임을 리턴하고 다음 게임으로 포인터 이동
            if i%10 ==0 :
                print(i,' ', end='', flush=True)
            i = i+1
        except KeyboardInterrupt:
            raise
        except:
            continue

        if not g: # 현재 포인터가 비어 있으면 yield 중지
            break
    gs.pop()
    #print("Num of Games in The file : ",len(gs))
    return gs # yield 는 한방에 return 하지 않고 배열로 하나하나 추가 해놓고 다 끝나면 통째로 리턴

class pgn_reader:
    def __init__(self,filename=None):
        self.gs = []
        self.len = 0
        self.filename = filename
        self.load_games()
        #init을 수행하면
    def __del__(self):
        print("소멸자 작동!")

    def set_pgn(self,filename):
        self.filename = filename

    def load_games(self):
        f = open(self.filename)
        self.gs = read_games(f)
        self.len = len(self.gs)

    def print_games(self):
        for i in range(self.len):
            self.info_game(i)
    def info_game(self, n):
        if(n >= self.len):
            return
        print(self.gs[n].headers)
    def get_game(self, g):
        gns = []
        result = ""
        gn = g.end()
        move_num = 0
        headers = g.headers
        while gn:
            gns.append((move_num, gn, gn.board().turn))

            move_num += 1
            gn = gn.parent
        result=g.headers['Result']
        return gns, result


    def allData(self,last = False):

        ba = BA.Board2Array()
        print("\n게임변환")
        for i in range(self.len):
            if i % 10 == 0:
                print(i, ' ', end='', flush=True)
                gameNodes, result = self.get_game(self.gs[i]) # i번째 게임을

            for j in range(len(gameNodes)-2): #처음부터 끝까지 입력과 출력으로 받음.
                input = []
                output = []
                results = []
                b = gameNodes[len(gameNodes) -(j+1)-2][1].board()
                b = ba.board2array(b)
                board = b
                #input 변환
                input.append(board)

                #output변환
                move = gameNodes[len(gameNodes) - j - 2][1].move
                move_str = move.__str__()
                output.append(self.outputToGrid(move_str)) # move의 string을 저장

                #result변환
                results.append(self.getResultOnehot(result))

                if j < 30:
                    with open('openGame.txt', 'ab') as f:
                        tmp = input, output, results
                        pickle.dump(tmp,f)
                elif j>=30 and j < 60:
                    with open('middleGame.txt', 'ab') as f:
                        tmp = input, output, results
                        pickle.dump(tmp,f)
                elif j>=60 :
                    with open('endGame.txt', 'ab') as f:
                        tmp = input, output, results
                        pickle.dump(tmp,f)


    def getResultOnehot(self,str):
        rm = {'1-0': [1, 0, 0, 0], '0-1': [0, 1, 0, 0], '1/2-1/2': [0, 0, 1, 0],'*': [0, 0, 0, 1]}  # 게임의 끝, ( 백승 = 1, 흑승 = -1, 무승부, 0 )
        return rm[str]

    def outputToGrid(self,move):
        #출발점과 도착점으로 이루어진 move를 격자 모양으로 만드는것
        output=[]
        uciOutput=None
        ohe = OHE() #OHE객체 생성
        uciOutput = ohe.uciMoveToOnehot(move) #4096 onehot


        return uciOutput


