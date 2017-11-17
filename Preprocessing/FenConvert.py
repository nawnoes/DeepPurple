import chess
from Symmtry_OneHotEncoding import OneHotEncode as OHE
import os

class FenConvert:
    def __init__(self):
        self.ohe = OHE()
# 턴을 바꾸기 위해 사용했던 함수들


    def turnFen(self, fen):
        fenSplit = fen.split(' ')
        fenBoard = fenSplit[0]  # .replace('/','') # / 없이 보드 변경
        fenTurn = fenSplit[1]  # 턴
        fenCastling = fenSplit[2]  # 캐슬링

        if fenTurn == 'b':  # 입력된 fen이 흑인경우
            for i in range(len(fenBoard)):
                if fenBoard[i].isupper() == True:  # 대문자이면 소문자로 변경
                    fenBoard[i].replace(fenBoard[i], fenBoard[i].lower())
                elif fenBoard[i].islower() == True:  # 소문자이면 대문자로 변경
                    fenBoard[i].replace(fenBoard[i], fenBoard[i].upper())

            fenSplit[0] = self.rotateBoard(fenBoard)  # 회전된 1단계 fen 기보
            fenSplit[1] = self.changeTurn(fenTurn)  # 턴을 수정
            fenSplit[2] = self.changeCastling(fenCastling).strip()
            fenSplit[3] = '-'  # 프로모션 부분은 제외
            rotateFen = ' '.join(fenSplit)

            return rotateFen

        else:  # 입력된 fen이 백인경우 그대로 리턴
            return fen
    def turnResult(self,fen,result):
        #fen이 바뀔때 결과 값도 바뀌게 되므로
        #기존 흑 과 백의 경우
        # rm = {'1-0': [1, 0, 0, 0], '0-1': [0, 1, 0, 0], '1/2-1/2': [0, 0, 1, 0],
        #       '*': [0, 0, 0, 1]}  # 게임의 끝, ( 백승 = 1, 흑승 = -1, 무승부, 0 )
        fenSplit = fen.split(' ')
        fenTurn = fenSplit[1]  # 턴
        if fenTurn =='w':
            return result
        if fenTurn == 'b':  # 입력된 fen이 흑인경우
            rm = {'1-0': '0-1', '0-1':'1-0', '1/2-1/2': '1/2-1/2','*': '*'}  # 게임의 끝, ( 백승 = 1, 흑승 = -1, 무승부, 0 )
            result = rm[result]
            return result

    def turnMove(self,fen,move):
        fenSplit = fen.split(' ')
        fenTurn = fenSplit[1]  # 턴
        if fenTurn == 'w':
            return move
        if fenTurn == 'b':  # 입력된 fen이 흑인경우
            move = self.ohe.symmetryMove2move(move)
            return move


    def makeWhiteFen(self,chessBoard):
        # chessBoard를  모두 백의 경우로 바꾸기위한 함수
        # board의 fen을 수정한다
        if chessBoard.turn == False:  # 현재 흑인 경우
            fen = chessBoard.fen()
            fenSplit = fen.split(' ')

            fenBoard = fenSplit[0]  # .replace('/','') # / 없이 보드 변경
            fenTurn = fenSplit[1]  # 턴
            fenCastling = fenSplit[2]  # 캐슬링
            for i in range(len(fenBoard)):
                if fenBoard[i].isupper() == True:  # 대문자이면 소문자로 변경
                    fenBoard[i].replace(fenBoard[i], fenBoard[i].lower())
                elif fenBoard[i].islower() == True:  # 소문자이면 대문자로 변경
                    fenBoard[i].replace(fenBoard[i], fenBoard[i].upper())

            fenSplit[0] = self.rotateBoard(fenBoard)  # 회전된 1단계 fen 기보
            fenSplit[1] = self.changeTurn(fenTurn)  # 턴을 수정
            fenSplit[2] = self.changeCastling(fenCastling).strip()
            fenSplit[3] = '-'
            fenSplit[4] = str(int(fenSplit[4]))
            fenSplit[5] = str(int(fenSplit[5]))
            resultFen = ' '.join(fenSplit)

            print("result fen : ", resultFen)
            makeBoard = chess.Board(resultFen)

            return makeBoard
        else:
            return chessBoard


    def rotateBoard(self,fenBoard):
        # 대소문자가 바뀐 보드를 대문자가 아래로 가게 보드를 회전
        listOfBoard = fenBoard.split('/')
        for i in range(8):  # 각 행을 거꾸로 뒤집는다
            listOfBoard[i] = listOfBoard[i].swapcase()
        listOfBoard.reverse()
        # print(listOfBoard)
        fenString = '/'.join(listOfBoard)  # 나눠진 fen을 다시 /로 합치는것

        return fenString


    def changeTurn(self,fenTurn):
        if fenTurn == 'b':
            return 'w'


    def changeCastling(self,fenCastling):
        # 입력은 4이하 문자열
        if fenCastling == '-':
            return fenCastling
        white = []
        black = []
        for i in range(len(fenCastling)):
            if fenCastling[i].isupper() == True:
                black.append(fenCastling[i].lower())
            elif fenCastling[i].islower() == True:
                white.append(fenCastling[i].upper())
        castling = white + black

        return ''.join(castling)