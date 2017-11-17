import chess
import ChessAI as AI

Intro = 0
Select = 10
Single = 1
Single_B =5
Two_player = 2
AIvsAI = 3
End = 7
Exit = 4

class ChessGame :
    def __init__(self):
        self.gameNum = 0
        self.ai = AI.ChessAI()
        self.player1 = None
        self.menuNum = 0
        self.autoSave = False # AIvsAI 모드 일때 기보 자동저장
        self.gameCount = 0 # AIvsAI 모드 일때 몇 게임을 진행하였는지 보여주기 위한 변수

        ########### 게임 결과정보 변수 ##############
        self.winner = None
        self.countNode = 0 # 게임이 몇개의 기보만에 끝이 났는지

    def start(self):
        while self.menuNum != Exit :
            if self.menuNum == Intro :
                self.intro()
            elif self.menuNum == Select :
                self.selectMode()
            elif self.menuNum == Single:
                self.single()
            elif self.menuNum == Two_player:
                self.two_player()
            elif self.menuNum == AIvsAI :
                self.aivsai()
            elif self.menuNum == End :
                self.endGame()
        self.exit()

    def intro(self):
        print('--------------ChessGame-------------')
        print('Welcome to Deep Purple Chess AI game!!!')
        self.menuNum = Select

    def selectMode(self):
        print("< mode menu >")
        print("1. single with AI")
        print("2. 2 Players")
        print("3. AI vs Ai For TrainMode")
        print("4. Exit")
        judge = False
        while not judge :
            self.menuNum = int(input('select : '))
            judge =  self.menuNum == Single or self.menuNum == Two_player or self.menuNum == AIvsAI or self.menuNum == Exit
            if not judge :
                print("선택이 올바르지 않습니다. 다시 선택하십시오.")

    def single(self):
        print("플레이할 색상을 선택하시오")
        print("1. White    2. Black")
        color = int(input("select : "))
        if color == 2 :
            self.menuNum = Single_B
        print("게임을 시작합니다")
        self.play()

    def two_player(self):
        print("게임을 시작합니다")
        self.play()

    def aivsai(self):
        print(self.gameCount,"번째 게임을 시작합니다")
        self.play()

    def endGame(self):
        print("게임종료")
        print("승자 : " ,end = "")
        if self.winner == '1-0' :
            print("흰색")
        elif self.winner == '0-1' :
            print("검정색")
        else :
            print("무승부")
        self.winner == None
        print("총 기보수 : " , self.countNode)
        self.countNode = 0
        print("1. 처음으로")
        print("2. 게임종료")
        tmp = input("select : ")
        if tmp == 1:
            self.menuNum = Select
        elif tmp == 2:
            self.menuNum = Exit

    def exit(self):
        print("게임을 종료합니다.")

    def play(self):
        board = chess.Board()
        count = 0
        while(True):
            print("a b c d e f g h")
            print("---------------")
            print(board,chr(13))
            print("---------------")
            print("a b c d e f g h")

            if (board.turn):
                print("흰색 차례")
                if self.menuNum == Single or self.menuNum == Two_player :
                    # player
                    choice = self.turnForPlayer(board)
                else :
                    # AI
                    choice = self.turnForAI(board)


            else :
                print("검은색 차례")
                if self.menuNum == Single or self.menuNum == AIvsAI :
                    # AI
                    choice = self.turnForAI(board)
                else :
                    # player
                    choice = self.turnForPlayer(board)

            if (choice == "0") :
                print("bye")
                self.menuNum = Exit
                break
            else :
                try:
                    board.push_san(choice)
                except :
                    choice = chess.Move.from_uci(choice)
                    board.push(choice)

                count += 1

            if board.is_game_over():
                self.countNode = count
                self.winner = board.result()
                self.menuNum = End
                break


    def turnForPlayer(self,Board):
        flag = True
        while flag:
            moves = Board.legal_moves.__str__()
            print("Legal moves : " , end = "")
            print(moves[37:-1])
            choice = input("choice:")
            if choice != "0":
                tmpBoard = Board.copy()
                try:
                    tmpBoard.push_san(choice)
                    flag = False
                except ValueError:
                    print("다시 선택해주세요")
            else :
                flag = False
        return choice

    def turnForAI(self,Board):
        choice=self.ai.ask(Board)
        print("AI의 선택 : ", choice)
        return choice


# 소스 구동
game = ChessGame()
game.start()
