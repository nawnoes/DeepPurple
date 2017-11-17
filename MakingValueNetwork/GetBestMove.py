import chess
import numpy as np
import tensorflow as tf
import os
import copy

from Board2Array import Board2Array as B2A
from OneHotEncoding import OneHotEncode as OHE

class GetBestMove:
    def __init__(self):
        self.promotion = 0.5  # legalmoves중에서 몇 퍼센트까지 만들지 결정 비율
        self.penalty = 0.01  # Score계산에서
        self.madeMoves = []  # 선택된 Moves의 list
        self.madeMovesScores = []  # madeMoves의 점수들이 들어 있는 list
        self.flag = False
        self.sess = tf.Session()

        PN_Name = "PN/"

        with tf.variable_scope("PN"):
            self.X = tf.placeholder(tf.float32, [None, 8, 8, 36], name="X")  # 체스에서 8X8X10 이미지를 받기 위해 64
            self.Y = tf.placeholder(tf.float32, [None], name="Y")

            self.W1 = tf.get_variable("W1", shape=[5, 5, 36, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B1 = tf.get_variable("B1", initializer=tf.random_normal([128], stddev=0.01))
            self.L1 = tf.nn.relu(tf.nn.conv2d(self.X, self.W1, strides=[1, 1, 1, 1], padding='SAME') + self.B1)

            self.W2 = tf.get_variable("W2", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B2 = tf.get_variable("B2", initializer=tf.random_normal([128], stddev=0.01))
            self.L2 = tf.nn.relu(tf.nn.conv2d(self.L1, self.W2, strides=[1, 1, 1, 1], padding='SAME') + self.B2)

            self.W3 = tf.get_variable("W3", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B3 = tf.get_variable("B3", initializer=tf.random_normal([128], stddev=0.01))
            self.L3 = tf.nn.relu(tf.nn.conv2d(self.L2, self.W3, strides=[1, 1, 1, 1], padding='SAME') + self.B3)

            self.W4 = tf.get_variable("W4", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B4 = tf.get_variable("B4", initializer=tf.random_normal([128], stddev=0.01))
            self.L4 = tf.nn.relu(tf.nn.conv2d(self.L3, self.W4, strides=[1, 1, 1, 1], padding='SAME') + self.B4)

            self.W5 = tf.get_variable("W5", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B5 = tf.get_variable("B5", initializer=tf.random_normal([128], stddev=0.01))
            self.L5 = tf.nn.relu(tf.nn.conv2d(self.L4, self.W5, strides=[1, 1, 1, 1], padding='SAME') + self.B5)

            self.W6 = tf.get_variable("W6", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B6 = tf.get_variable("B6", initializer=tf.random_normal([128], stddev=0.01))
            self.L6 = tf.nn.relu(tf.nn.conv2d(self.L5, self.W6, strides=[1, 1, 1, 1], padding='SAME') + self.B6)

            self.W7 = tf.get_variable("W7", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B7 = tf.get_variable("B7", initializer=tf.random_normal([128], stddev=0.01))
            self.L7 = tf.nn.relu(tf.nn.conv2d(self.L6, self.W7, strides=[1, 1, 1, 1], padding='SAME') + self.B7)

            self.W8 = tf.get_variable("W8", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B8 = tf.get_variable("B8", initializer=tf.random_normal([128], stddev=0.01))
            self.L8 = tf.nn.relu(tf.nn.conv2d(self.L7, self.W8, strides=[1, 1, 1, 1], padding='SAME') + self.B8)

            self.W9 = tf.get_variable("W9", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B9 = tf.get_variable("B9", initializer=tf.random_normal([128], stddev=0.01))
            self.L9 = tf.nn.relu(tf.nn.conv2d(self.L8, self.W9, strides=[1, 1, 1, 1], padding='SAME') + self.B9)

            self.W10 = tf.get_variable("W10", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B10 = tf.get_variable("B10", initializer=tf.random_normal([128], stddev=0.01))
            self.L10 = tf.nn.relu(tf.nn.conv2d(self.L9, self.W10, strides=[1, 1, 1, 1], padding='SAME') + self.B10)

            self.W11 = tf.get_variable("W11", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B11 = tf.get_variable("B11", initializer=tf.random_normal([128], stddev=0.01))
            self.L11 = tf.nn.relu(tf.nn.conv2d(self.L10, self.W11, strides=[1, 1, 1, 1], padding='SAME') + self.B11)

            self.W12 = tf.get_variable("W12", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B12 = tf.get_variable("B12", initializer=tf.random_normal([128], stddev=0.01))
            self.L12 = tf.nn.relu(tf.nn.conv2d(self.L11, self.W12, strides=[1, 1, 1, 1], padding='SAME') + self.B12)

            self.W13 = tf.get_variable("W13", shape=[1, 1, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B13 = tf.get_variable("B13", initializer=tf.random_normal([128], stddev=0.01))
            self.L13 = tf.nn.relu(tf.nn.conv2d(self.L12, self.W13, strides=[1, 1, 1, 1], padding='SAME') + self.B13)

            self.FlatLayer = tf.reshape(self.L13, [-1, 8 * 8 * 128])
            self.Flat_W = tf.get_variable("Flat_W", shape=[8 * 8 * 128, 4096],
                                     initializer=tf.contrib.layers.xavier_initializer())
            self.Flat_B = tf.get_variable("Flat_B", initializer=tf.random_normal([4096], stddev=0.01))

            self.hypothesis = tf.matmul(self.FlatLayer, self.Flat_W) + self.Flat_B

            self.softmaxOfHypothesis = tf.nn.softmax(self.hypothesis)
            self.score = tf.nn.softmax(self.Y)

            self.sess.run(tf.global_variables_initializer())
        self.PN_Saves={
                         PN_Name + "W1": self.W1, PN_Name + "B1": self.B1,
                         PN_Name + "W2": self.W2, PN_Name + "B2": self.B2,
                         PN_Name + "W3": self.W3, PN_Name + "B3": self.B3,
                         PN_Name + "W4": self.W4, PN_Name + "B4": self.B4,
                         PN_Name + "W5": self.W5, PN_Name + "B5": self.B5,
                         PN_Name + "W6": self.W6, PN_Name + "B6": self.B6,
                         PN_Name + "W7": self.W7, PN_Name + "B7": self.B7,
                         PN_Name + "W8": self.W8, PN_Name + "B8": self.B8,
                         PN_Name + "W9": self.W9, PN_Name + "B9": self.B9,
                         PN_Name + "W10": self.W10, PN_Name + "B10": self.B10,
                         PN_Name + "W11": self.W11, PN_Name + "B11": self.B11,
                         PN_Name + "W12": self.W12, PN_Name + "B12": self.B12,
                         PN_Name + "W13": self.W13, PN_Name + "B13": self.B13,
                         PN_Name + "Flat_W": self.Flat_W, PN_Name + "Flat_B": self.Flat_B,
                         }
        saver = tf.train.Saver(self.PN_Saves)
        checkpoint= tf.train.get_checkpoint_state(os.path.dirname('C:/Users/Kim/Desktop/Project/New_DeepPurple/PolicyCheckpoint/'))
        # checkpoint = tf.train.get_checkpoint_state(os.path.dirname('./PNCheckpoint/'))
        print(checkpoint.model_checkpoint_path)
        if checkpoint and checkpoint.model_checkpoint_path:
            saver.restore(self.sess, checkpoint.model_checkpoint_path)
            print("\n체크포인트 파일 재사용 = ", checkpoint.model_checkpoint_path)
        else:
            print("\n체크포인트 파일 미사용 ")
    def getPolicyNetworkModel(self, cnnInput):
        getSoftmax = self.sess.run(self.softmaxOfHypothesis, feed_dict={self.X: cnnInput})
        return getSoftmax

    def getPolicyNetworkInput(self,chessBoard):
        CnnInput = []
        CnnInput.append(B2A().board2arrayForGetBestMove(chessBoard))
        return CnnInput

    def getBestMove(self,chessBoard):

        cnnInput = self.getPolicyNetworkInput(chessBoard)
        softmax = self.getPolicyNetworkModel(cnnInput)
        softmax = np.array(softmax[0])

        indexOfArgmaxedSoftmax = (-softmax).argsort()

        onehotencoding = OHE()
        score = []
        move = []

        i=0
        #선택된 자식수
        child=0

        numOfLegalMoves = len(chessBoard.legal_moves)
        numOfChild = 1 # 만들어질 자식 수

        if numOfLegalMoves < numOfChild:
            numOfChild = numOfLegalMoves

        for j in range(4096):
            try:
                tmpMove = onehotencoding.indexToMove4096(indexOfArgmaxedSoftmax[i])
                strMove = copy.deepcopy(tmpMove)
                tmpMove = chess.Move.from_uci(tmpMove) # 주석처리: 선피쉬랑 붙기 위해 String 자체를 사용
            except:
                print(i)
                print(numOfChild)
                print(numOfLegalMoves)
            try:
                if tmpMove in chessBoard.legal_moves:
                    move=strMove # tmpMove가 legal이면 추가
                    score = softmax[indexOfArgmaxedSoftmax[i]]
                    # print(i+1,"번째 선택된 점수 : ",score, " move: ",move)
                    child += 1
            except:
                continue
            # print(i + 1, "번째 선택된 점수 : ", softmax[indexOfArgmaxedSoftmax[i]], " move: ", tmpMove)
            i += 1
            if child >= numOfChild:  # 만드려고 하는 자식 갯수보다 많으면 반환
                break
        #(???) 왜 다시 소프트맥스를 하는 거지
        # score = self.sess.run(self.score, feed_dict={self.Y: score})

        return move, score


