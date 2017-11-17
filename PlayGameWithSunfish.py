from Sunfish import sunfish
from GetMovesAndScores import GetMovesAndScores as GMAS
import chess

def main():
    gmas = GMAS()
    chessBoard = chess.Board()

    pos = sunfish.Position(sunfish.initial, 0, (True,True), (True,True), 0, 0)
    searcher = sunfish.Searcher()
    while True:
        sunfish.print_pos(pos)

        if pos.score <= -sunfish.MATE_LOWER:
            print("You lost")
            break

        # We query the user until she enters a (pseudo) legal move.
        move = None
        while move not in pos.gen_moves():
            # match = sunfish.re.match('([a-h][1-8])'*2, input('Your move: '))
            # if match:
                move = gmas.get_bestMove(chessBoard)# sunfish.parse(match.group(1)), sunfish.parse(match.group(2))
                chessBoard.push_uci(move)
                move = sunfish.parse(move[:2]), sunfish.parse(move[2:])
            # else:
            #     Inform the user when invalid input (e.g. "help") is entered
                # print("Please enter a move like g8f6")
        pos = pos.move(move)

        # After our move we rotate the board and print it again.
        # This allows us to see the effect of our move.
        sunfish.print_pos(pos.rotate())

        if pos.score <= -sunfish.MATE_LOWER:
            print("You won")
            break

        # Fire up the engine to look for a move.
        move, score = searcher.search(pos, secs=2)

        if score == sunfish.MATE_UPPER:
            print("Checkmate!")

        # The black player moves from a rotated position, so we have to
        # 'back rotate' the move before printing it.
        myMove = sunfish.render(119 - move[0]) + sunfish.render(119 - move[1])
        print("My move:", myMove)
        chessBoard.push_uci(myMove)
        pos = pos.move(move)


if __name__ == '__main__':
    main()