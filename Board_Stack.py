import chess


class Board_Stack():
    def __init__(self, Board): #boardString은 Tree 생성할때 전달 받는 String
        self.chessBoard = Board.copy()

    def stack_push(self, command): #boardStack에 체스판 쌓기
        move = chess.Move.from_uci(command)
        self.chessBoard.push(move) #입력 받은 명령어를 chessBoard에 갱신

    def stack_pop(self): #boardStack의 선입선출
        return self.chessBoard.pop() #가장 최근 들어간 명령어를 pop

    def display_Board(self): #boardStack에 입력된 명령어까지 체스판으로 출력
        print(self.chessBoard)

    def get_ChessBoard(self):
        return self.chessBoard

    def get_GameOver(self):
        return self.chessBoard.is_game_over()

    def get_Result(self):
        return self.chessBoard.result()

    def get_Color(self):
        return self.chessBoard.turn


