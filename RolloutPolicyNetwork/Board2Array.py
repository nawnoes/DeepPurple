'''
5/20일 알파고모델에 사용된 입력 변환 모듈
-체크 부분 수정
-슬라이딩 피스 의문점 , 그러나 chess 라이브러리 자체 기능

'''

import numpy as np
import chess

class Board2Array:
    def board2arrayForRollout(self, chessBoard):
        #chessBoard를 Model에 넣기 전에 원하는 input을 만들기 위한 함수

        chessStr = self.get_chessStr(chessBoard)
        boardArray = []
        boardArray.append(self.square())
        boardArray.append(self.white(chessBoard,chessStr))
        boardArray.append(self.black(chessBoard, chessStr))
        boardArray.append(self.piece(chessBoard, chessStr, '.'))
        boardArray.append(self.piece(chessBoard, chessStr, 'K'))
        boardArray.append(self.piece(chessBoard, chessStr, 'k'))
        boardArray.append(self.piece(chessBoard, chessStr, 'Q'))
        boardArray.append(self.piece(chessBoard, chessStr, 'q'))
        boardArray.append(self.piece(chessBoard, chessStr, 'R'))
        boardArray.append(self.piece(chessBoard, chessStr, 'r'))
        boardArray.append(self.piece(chessBoard, chessStr, 'N'))
        boardArray.append(self.piece(chessBoard, chessStr, 'n'))
        boardArray.append(self.piece(chessBoard, chessStr, 'B'))
        boardArray.append(self.piece(chessBoard, chessStr, 'b'))
        boardArray.append(self.piece(chessBoard, chessStr, 'P'))
        boardArray.append(self.piece(chessBoard, chessStr, 'p'))\

        boardArray = np.array(boardArray)
        boardArray =boardArray.transpose(1,2,0) # 행렬을 입력에 맞게 변환
        boardArray = np.ndarray.tolist(boardArray) # numpy 배열을 list로 변환

        return boardArray #, boardArray2

    def board2array(self, chessBoard):
        #chessBoard를 Model에 넣기 전에 원하는 input을 만들기 위한 함수

        chessStr = self.get_chessStr(chessBoard)
        boardArray = []
        boardArray.append(self.square())
        boardArray.append(self.white(chessBoard,chessStr))
        boardArray.append(self.black(chessBoard, chessStr))
        boardArray.append(self.piece(chessBoard, chessStr, '.'))
        boardArray.append(self.piece(chessBoard, chessStr, 'K'))
        boardArray.append(self.piece(chessBoard, chessStr, 'k'))
        boardArray.append(self.piece(chessBoard, chessStr, 'Q'))
        boardArray.append(self.piece(chessBoard, chessStr, 'q'))
        boardArray.append(self.piece(chessBoard, chessStr, 'R'))
        boardArray.append(self.piece(chessBoard, chessStr, 'r'))
        boardArray.append(self.piece(chessBoard, chessStr, 'N'))
        boardArray.append(self.piece(chessBoard, chessStr, 'n'))
        boardArray.append(self.piece(chessBoard, chessStr, 'B'))
        boardArray.append(self.piece(chessBoard, chessStr, 'b'))
        boardArray.append(self.piece(chessBoard, chessStr, 'P'))
        boardArray.append(self.piece(chessBoard, chessStr, 'p'))
        boardArray.append(self.slidingPiece(chessBoard,chessStr, 'Q'))
        boardArray.append(self.slidingPiece(chessBoard,chessStr, 'q'))
        boardArray.append(self.slidingPiece(chessBoard,chessStr, 'R'))
        boardArray.append(self.slidingPiece(chessBoard,chessStr, 'r'))
        boardArray.append(self.slidingPiece(chessBoard,chessStr, 'B'))
        boardArray.append(self.slidingPiece(chessBoard,chessStr, 'b'))
        boardArray.append(self.slidingPiece(chessBoard,chessStr, 'N'))
        boardArray.append(self.slidingPiece(chessBoard,chessStr, 'n'))
        boardArray.append(self.slidingPiece(chessBoard,chessStr, 'P'))
        boardArray.append(self.slidingPiece(chessBoard,chessStr, 'p'))
        boardArray.append(self.pin(chessBoard, chess.WHITE))
        boardArray.append(self.pin(chessBoard, chess.BLACK))
        boardArray.append(self.attacked(chessBoard, chess.WHITE))# 흰색 말이 이동할 수 있는 곳
        boardArray.append(self.attacked(chessBoard, chess.BLACK))# 검은색 말이 이동할 수 있는 곳
        boardArray.append(self.check(chessBoard,chessStr)) #chess.WHITE
        boardArray.append(self.check(chessBoard,chessStr)) #chess.BLACK
        boardArray.append(self.castling(chessBoard,chess.WHITE))
        boardArray.append(self.castling(chessBoard, chess.BLACK))
        boardArray.append(self.turn(chessBoard, chess.WHITE))
        boardArray.append(self.turn(chessBoard, chess.BLACK))

        boardArray = np.array(boardArray)
        boardArray =boardArray.transpose(1,2,0) # 행렬을 입력에 맞게 변환
        boardArray = np.ndarray.tolist(boardArray) # numpy 배열을 list로 변환

        return boardArray #, boardArray2
    #feature만들기
    def square(self):
        #칸 고유의 특성을 1로 설정
        #아마 제로패딩시 사용될거라 추측
        feature = [[1] * 8 for i in range(8)]
        return feature

    def white(self,chessBoard , chessStr):
        feature= [[0] * 8 for i in range(8)]
        k=0
        for i in range(8):
            for j in range(8):
                if chessStr[k].isupper() == True: # 대문자로 흰색이면
                    feature[i][j] = 1
                k +=1
        # print(feature)
        return feature
    def black(self,chessBoard , chessStr):
        feature= [[0] * 8 for i in range(8)]
        k=0
        for i in range(8):
            for j in range(8):
                if chessStr[k].islower() == True: # 대문자로 흰색이면
                    feature[i][j] = 1
                k +=1
        # print(feature)
        return feature
    def piece(self,chessBoard , chessStr, piece):
        feature= [[0] * 8 for i in range(8)]
        k=0
        for i in range(8):
            for j in range(8):
                if chessStr[k] == piece: # 대문자로 흰색이면
                    feature[i][j] = 1
                k +=1
        # print(feature)
        return feature

    def slidingPiece(self, chessBoard, chessStr, piece):
        #5월20일에 수정됨
        feature = [[0] * 8 for i in range(8)]
        pieceIndex = []
        l = 0
        for i in range(8):
            for j in range(8):
                if chessStr[l] == piece:
                    pieceIndex.append((8 * (7 - i) + j))
                l += 1

        # print(pieceIndex)
        for index in pieceIndex:
            str = chessBoard.attacks(index).__str__()
            str = str.replace('\n', ' ')
            str = str.replace(' ', '')
            m = 0  # 이때 m의 순서는 chess.SQUARES가 아니다
            for i in range(8):
                for j in range(8):
                    if str[m] == '1':
                        feature[i][j] = 1
                    m += 1
        # for i in range(8):
        #     print(feature[i])
        return feature
    def pin(self,chessBoard, chessTurn):
        feature = [[0] * 8 for i in range(8)]
        k = 0 #이때 k는 chess.SQUARES 순서
        for i in range(8):
            for j in range(8):
                if chessBoard.is_pinned(chessTurn,k):
                    #현재 주어진 color(턴)에 square가 pin 상태라면
                    feature[7-i][j] = 1
                k += 1
        # for i in range(8):
        #     print(feature[i])
        return feature
    def attacked(self,chessBoard, chessTurn):
        # color에 의해 square가 공격받을 수 있는지
        feature = [[0] * 8 for i in range(8)]
        k = 0 #이때 k 값은 chess.SQUARES의 의 순서라 아래에서 부터 접근
        for i in range(8):
            for j in range(8):
                if chessBoard.is_attacked_by(chessTurn, k):
                    feature[7 - i][j] = 1
                k += 1
        # for i in range(8):
        #     print(feature[i])
        return feature
    def check(self,chessBoard, chessStr):
        #주어진 턴의 킹의 상태가 check인지
        feature = [[0] * 8 for i in range(8)]
        k = 0
        flag =False
        for i in range(8):
            for j in range(8): # 이때 chessStr의 인덱스 k가 chess.SQUARES 의 순서가 아니므로 위에서 부터 접근
                if chessBoard.turn== chess.BLACK and chessBoard.is_check() and chessStr[k] == 'k':
                    feature[i][j] = 1
                    flag =True
                if chessBoard.turn== chess.WHITE and chessBoard.is_check() and chessStr[k] == 'K':
                    feature[i][j] = 1
                    flag = True
                k += 1
                if flag:
                    break
            if flag:
                break

        return feature
    def turn(self,chessBoard, chessTurn):
        #턴이 일치하면 전체가 1, 일치하지 않으면 0 반환
        feature = [[0] * 8 for i in range(8)]
        for i in range(8):
            for j in range(8):
                if chessTurn == chessBoard.turn:
                    feature[i][j] = 1
        return feature
    def castling(self,chessBoard, chessTurn):
        #주어진 턴에서 캐슬링 경우가 있는지
        feature = [[0] * 8 for i in range(8)]

        if chessBoard.has_kingside_castling_rights(chessTurn) and chessTurn:
            #현재 체스 턴이 백. 백의 킹사이드 캐슬링
            feature[7][4] = feature[7][7] = 1
        if chessBoard.has_kingside_castling_rights(chessTurn) and not chessTurn:
            #현재 체스 턴이 흑. 흑의 킹사이드 캐슬링
            feature[0][4] = feature[0][7] = 1
        if chessBoard.has_queenside_castling_rights(chessTurn) and  chessTurn:
            #현재 체스 턴이 흑. 흑의 킹사이드 캐슬링
            feature[7][0] = feature[7][3] = 1
        if chessBoard.has_queenside_castling_rights(chessTurn) and not chessTurn:
            #현재 체스 턴이 흑. 흑의 킹사이드 캐슬링
            feature[0][0] = feature[0][3] = 1

        # for i in range(8):
        #     print(feature[i])
        # print()
        return feature
    def get_chessStr(elf,chessBoard):

        chessStr = chessBoard.__str__()
        chessStr = chessStr.replace('\n', ' ')
        chessStr = chessStr.replace(' ', '')

        return chessStr
    def get_slashChessStr(self,chessBoard):

        chessStr = chessBoard.__str__()
        chessStr = chessStr.replace('\n', '/')
        chessStr = chessStr.replace(' ', '')

        return chessStr



