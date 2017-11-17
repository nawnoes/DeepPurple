from Board2Array_31Feature import Board2Array as B2A
import chess
import copy
from Symmtry_OneHotEncoding import OneHotEncode as OHE
import os

b2a= B2A()

f = open('fen.txt','r')
lines = f.readlines()
for i in lines:
    board = chess.Board(i)
    print(board)
    b , b2= b2a.board2array(board)
    print()
# b2a.attacked(board,chess.WHITE)
# print('------------white-----------------')
# b2a.attacked(board,chess.BLACK)
# print('------------black-----------------')
# # b2a.slidingPiece(board,'r')

