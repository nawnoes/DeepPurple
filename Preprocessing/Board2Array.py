import numpy as np
import chess

class Board2Array:

    def board2array(self, chessBoard):
        #chessBoard를 Model에 넣기 전에 원하는 input을 만들기 위한 함수

        chessStr = self.get_chessStr(chessBoard)
        boardArray = []
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
        boardArray.append(self.slidingPiece(chessBoard, 'Q'))
        boardArray.append(self.slidingPiece(chessBoard, 'q'))
        boardArray.append(self.slidingPiece(chessBoard, 'R'))
        boardArray.append(self.slidingPiece(chessBoard, 'r'))
        boardArray.append(self.slidingPiece(chessBoard, 'B'))
        boardArray.append(self.slidingPiece(chessBoard, 'b'))
        boardArray.append(self.pin(chessBoard, chess.WHITE))
        boardArray.append(self.pin(chessBoard, chess.BLACK))
        boardArray.append(self.attacked(chessBoard, chess.WHITE))# 흰색 말이 이동할 수 있는 곳
        boardArray.append(self.attacked(chessBoard, chess.BLACK))# 검은색 말이 이동할 수 있는 곳
        boardArray.append(self.check(chessBoard,chessStr, chess.WHITE))
        boardArray.append(self.check(chessBoard,chessStr, chess.BLACK))
        boardArray.append(self.castling(chessBoard,chess.WHITE))
        boardArray.append(self.castling(chessBoard, chess.BLACK))
        boardArray.append(self.turn(chessBoard, chess.WHITE))
        boardArray.append(self.turn(chessBoard, chess.BLACK))

        boardArray = np.array(boardArray)
        boardArray =boardArray.transpose(1,2,0) # 행렬을 입력에 맞게 변환
        boardArray = np.ndarray.tolist(boardArray) # numpy 배열을 list로 변환

        return boardArray
    #feature만들기
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
    def slidingPiece(self,chessBoard , piece):
        feature = [[0] * 8 for i in range(8)]
        pieceIndex = []
        chessStr = self.get_slashChessStr(chessBoard)
        chessStr = chessStr.split('/')
        chessStr.reverse()
        chessStr=''.join(chessStr)
        for i in range(64):
            if chessStr[i] == piece:
                pieceIndex.append(i)

        # print(pieceIndex)
        for index in pieceIndex:
            str=chessBoard.attacks(index).__str__()
            str = str.replace('\n', ' ')
            str = str.replace(' ', '')

            m=0 #이때 m의 순서는 chess.SQUARES가 아니다
            for i in range(8):
                for j in range(8):
                    if str[m] == '1' :
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
    def check(self,chessBoard, chessStr, chessTurn):
        #주어진 턴의 킹의 상태가 check인지
        feature = [[0] * 8 for i in range(8)]
        k = 0
        for i in range(8):
            for j in range(8): # 이때 chessStr의 인덱스 k가 chess.SQUARES 의 순서가 아니므로 위에서 부터 접근
                if chessTurn== chess.BLACK and chessBoard.is_check() and chessStr[k] == 'k':
                    feature[i][j] = 1
                if chessTurn== chess.WHITE and chessBoard.is_check() and chessStr[k] == 'K':
                    feature[i][j] = 1
                k += 1
        # for i in range(8):
        #     print(feature[i])
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


'''
턴을 바꾸기 위해 사용했던 함수들
    def makeWhiteFen(self, chessBoard):
        #chessBoard를  모두 백의 경우로 바꾸기위한 함수
        # board의 fen을 수정한다
        if chessBoard.turn == False: # 현재 흑인 경우
            fen = chessBoard.fen()
            fenSplit = fen.split(' ')

            fenBoard = fenSplit[0] #.replace('/','') # / 없이 보드 변경
            fenTurn = fenSplit[1] #턴
            fenCastling = fenSplit [2] # 캐슬링
            for i in range(len(fenBoard)):
                if fenBoard[i].isupper() ==True: #대문자이면 소문자로 변경
                    fenBoard[i].replace(fenBoard[i], fenBoard[i].lower())
                elif fenBoard[i].islower() ==True: #소문자이면 대문자로 변경
                    fenBoard[i].replace(fenBoard[i], fenBoard[i].upper())

            fenSplit[0] = self.rotateBoard(fenBoard) # 회전된 1단계 fen 기보
            fenSplit[1] = self.changeTurn(fenTurn) # 턴을 수정
            fenSplit[2] = self.changeCastling(fenCastling).strip()
            fenSplit[4] = str(int(fenSplit[4])+1)
            fenSplit[5] = str(int(fenSplit[5])-1)
            resultFen = ' '.join(fenSplit)
            print("result fen : ", resultFen)

            makeBoard = chess.Board(resultFen)
            makeBoard.set_castling_fen(fenSplit[2])

            return makeBoard
        else:
            return chessBoard
    def rotateBoard(self,fenBoard):
        #대소문자가 바뀐 보드를 대문자가 아래로 가게 보드를 회전
        listOfBoard = fenBoard.split('/')
        for i in range(8): #각 행을 거꾸로 뒤집는다
            listOfBoard[i]=listOfBoard[i].swapcase()
            listOfBoard[i] = listOfBoard[i][::-1]
        listOfBoard.reverse()
        fenString = '/'.join(listOfBoard) # 나눠진 fen을 다시 /로 합치는것

        return fenString
    def changeTurn(self,fenTurn):
        if fenTurn == 'b':
            return 'w'
    def changeCastling(self,fenCastling):
        #입력은 4이하 문자열
        if fenCastling =='-':
            return fenCastling
        white=[]
        black = []
        for i in range(len(fenCastling)):
            if fenCastling[i].isupper()== True:
                black.append(fenCastling[i].lower())
            elif fenCastling[i].islower()== True:
                white.append(fenCastling[i].upper())
        castling = white+black

        return ''.join(castling)
    def board2array3(self, chessBoard):
        if chessBoard.turn:
            turn = 1
        else:
            turn = 0
        str = chessBoard.__str__()
        str = str.replace('\n', ' ')
        str = str.replace(' ', '')
        boardArray = []
        for i in range(len(str)):
            boardArray.append(-1)

        # ---------백-------\--------흑-----------빈칸
        # 0  1  2  3  4  5  6  7  8  9  10  11  12
        # 킹 퀸 말  숍 폰 룩 킹  퀸 말 숍  폰  룩  빈칸
        for i in range(len(str)):
            if turn == 1:
                color = chess.WHITE
            else:
                color = chess.BLACK

            row = 8 - i // 8
            col = 8 - i % 8
            xy = row * 8 - col

            attack = chessBoard.is_attacked_by(turn, xy)
            if attack:
                my_attack_value = 1
            else:
                my_attack_value = 0

            attack = chessBoard.is_attacked_by(not turn, xy)

            if attack:
                you_attack_value = 1
            else:
                you_attack_value = 0

            if str[i] == 'K':
                boardArray[i] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            elif str[i] == 'Q':
                boardArray[i] = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            elif str[i] == 'N':
                boardArray[i] = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            elif str[i] == 'B':
                boardArray[i] = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            elif str[i] == 'P':
                boardArray[i] = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
            elif str[i] == 'R':
                boardArray[i] = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
            elif str[i] == 'k':
                boardArray[i] = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
            elif str[i] == 'q':
                boardArray[i] = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
            elif str[i] == 'n':
                boardArray[i] = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
            elif str[i] == 'b':
                boardArray[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
            elif str[i] == 'p':
                boardArray[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
            elif str[i] == 'r':
                boardArray[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
            elif str[i] == '.':
                boardArray[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

            boardArray[i].append(my_attack_value)  # 공격
            boardArray[i].append(you_attack_value)  # 피공격
            boardArray[i].append(turn) #턴

        return boardArray
'''