from Board2Array_31Feature import Board2Array as B2A
import chess
import copy
from Symmtry_OneHotEncoding import OneHotEncode as OHE
import os

b2a= B2A()

f = open('fen.txt','r')
lines = f.readlines()
for i in lines:
    print(i)
    board = chess.Board(i)
    print(board)
    b = b2a.makeWhiteFen(board)
    print('\n makeWhiteFen\n',b)
    print("b.fen : ", b.fen())