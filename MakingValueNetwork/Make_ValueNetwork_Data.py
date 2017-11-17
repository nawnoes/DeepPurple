import chess
import numpy as np
import tensorflow as tf
import os
from MakingValueNetwork.GetBestMove import GetBestMove as GBM


class MakeVNData:
    def __init__(self):
        self.chessBoard = chess.Board()
        self.NUMBER_OF_DATA = 30000000 #3천만개 데이터에 대해서 결과 생성
        self.getBestMove = GBM()

    def simulation(self,fen):
        #펜데이터로 경기가 끝날때 까지 진행
        self.chessBoard.set_fen(fen)
        # fen=None
        result=None

        while not self.chessBoard.is_game_over():

            # print("a b c d e f g h")
            # print("---------------")
            # print(self.chessBoard, chr(13))
            # print("---------------")
            # print("a b c d e f g h")
            move, score = self.getBestMove.getBestMove(self.chessBoard)
            #
            # if self.chessBoard.turn:
            #     print("백: ", move, ", score: ",score)
            # else:
            #     print("흑: ", move, ", score: ", score)
            try:
                self.chessBoard.push(chess.Move.from_uci(move))
            except:
                return None,None


        if self.chessBoard.is_game_over():
            print("게임 결과: ", self.chessBoard.result())
            # fen= self.chessBoard.fen()
            result = self.chessBoard.result()

        return fen,result

    def getValueNetworkLearningData(self):

        #Fen기보 데이터를 불러옴
        loadFenTextFile = open('30milionFendata.txt','r')
        try:
            saveCountOfMakedData = open('MakedDataCount.txt','r')
        except:
            COUNT = 0
        else:
            COUNT = int(saveCountOfMakedData.readline())
        #한줄씩 읽어서 chessboard에 Fen으로 삽입

        for i, line in enumerate(loadFenTextFile):
            if COUNT <= i and i < self.NUMBER_OF_DATA:
                fenData= line
                fen = fenData[:-1]
                fen = fen.split(":")
                returnedFen, returnedResult = self.simulation(fen[0])
                if returnedFen == None:
                    continue
                self.savingFenData(returnedFen,returnedResult)
                with open('MakedDataCount.txt','w') as f:
                   f.write(str(i))

        #모든 파일을 읽을때까지 무한 루프
        #매 반복문마다 새로운 파일에 'Fen기보:결과'에 대해 저장
        #모든 과정이 끝나면 makeVNData에서 가치망 데이터 완성.

        None
    def savingFenData(self,fen,result):
        saveFen = open('DataForValueNetwork.txt','a')
        data= fen+":"+result+"\n"
        saveFen.write(data)

if __name__ == "__main__":
    makeValueNetworkData=MakeVNData()
    makeValueNetworkData.getValueNetworkLearningData()