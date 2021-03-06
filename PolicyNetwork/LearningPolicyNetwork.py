
import os
import tensorflow as tf
from FenLoad import FenLoad as FL
from Board2Array import Board2Array as B2A
from OneHotEncoding import OneHotEncode as OHE
import chess

KingBase = ['KingBase']

testPgn =None
pgnIndex, pgnInput, pgnOutput, pgnResult =None, None, None, None
learning_rate=0.001 #0.00025
training_epochs = 3
batchSize = 10000
TEN_Million = 80000000
ITERATION = int(TEN_Million / batchSize)
VALID = 3000 # 2000개 검증 데이터로 사용
TRAIN = batchSize - VALID # batchSize-2000개 학습 데이터로 사용


fl = FL()
ohe = OHE()
b2a = B2A()
board = chess.Board()



path = "./PNCheckpoint/path"
# sess = tf.Session()
mode ="All Data mode "
name =None





with tf.variable_scope("PN"):
    X = tf.placeholder(tf.float32, [None, 8, 8, 36], name="X")  # 체스에서 8X8X10 이미지를 받기 위해 64
    Y = tf.placeholder(tf.float32, [None, 4096], name="Y")

    W1 = tf.get_variable("W1", shape=[5, 5, 36, 128], initializer=tf.contrib.layers.xavier_initializer())
    B1 = tf.get_variable("B1", initializer=tf.random_normal([128], stddev=0.01))
    L1 = tf.nn.relu(tf.nn.conv2d(X, W1, strides=[1, 1, 1, 1], padding='SAME') + B1)

    W2 = tf.get_variable("W2", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
    B2 = tf.get_variable("B2", initializer=tf.random_normal([128], stddev=0.01))
    L2 = tf.nn.relu(tf.nn.conv2d(L1, W2, strides=[1, 1, 1, 1], padding='SAME') + B2)

    W3 = tf.get_variable("W3", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
    B3 = tf.get_variable("B3", initializer=tf.random_normal([128], stddev=0.01))
    L3 = tf.nn.relu(tf.nn.conv2d(L2, W3, strides=[1, 1, 1, 1], padding='SAME') + B3)

    W4 = tf.get_variable("W4", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
    B4 = tf.get_variable("B4", initializer=tf.random_normal([128], stddev=0.01))
    L4 = tf.nn.relu(tf.nn.conv2d(L3, W4, strides=[1, 1, 1, 1], padding='SAME') + B4)

    W5 = tf.get_variable("W5", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
    B5 = tf.get_variable("B5", initializer=tf.random_normal([128], stddev=0.01))
    L5 = tf.nn.relu(tf.nn.conv2d(L4, W5, strides=[1, 1, 1, 1], padding='SAME') + B5)

    W6 = tf.get_variable("W6", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
    B6 = tf.get_variable("B6", initializer=tf.random_normal([128], stddev=0.01))
    L6 = tf.nn.relu(tf.nn.conv2d(L5, W6, strides=[1, 1, 1, 1], padding='SAME') + B6)

    W7 = tf.get_variable("W7", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
    B7 = tf.get_variable("B7", initializer=tf.random_normal([128], stddev=0.01))
    L7 = tf.nn.relu(tf.nn.conv2d(L6, W7, strides=[1, 1, 1, 1], padding='SAME') + B7)

    W8 = tf.get_variable("W8", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
    B8 = tf.get_variable("B8", initializer=tf.random_normal([128], stddev=0.01))
    L8 = tf.nn.relu(tf.nn.conv2d(L7, W8, strides=[1, 1, 1, 1], padding='SAME') + B8)

    W9 = tf.get_variable("W9", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
    B9 = tf.get_variable("B9", initializer=tf.random_normal([128], stddev=0.01))
    L9 = tf.nn.relu(tf.nn.conv2d(L8, W9, strides=[1, 1, 1, 1], padding='SAME') + B9)

    W10 = tf.get_variable("W10", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
    B10 = tf.get_variable("B10", initializer=tf.random_normal([128], stddev=0.01))
    L10 = tf.nn.relu(tf.nn.conv2d(L9, W10, strides=[1, 1, 1, 1], padding='SAME') + B10)

    W11 = tf.get_variable("W11", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
    B11 = tf.get_variable("B11", initializer=tf.random_normal([128], stddev=0.01))
    L11 = tf.nn.relu(tf.nn.conv2d(L10, W11, strides=[1, 1, 1, 1], padding='SAME') + B11)

    W12 = tf.get_variable("W12", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
    B12 = tf.get_variable("B12", initializer=tf.random_normal([128], stddev=0.01))
    L12 = tf.nn.relu(tf.nn.conv2d(L11, W12, strides=[1, 1, 1, 1], padding='SAME') + B12)

    W13 = tf.get_variable("W13", shape=[1, 1, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
    B13 = tf.get_variable("B13", initializer=tf.random_normal([128], stddev=0.01))
    L13 = tf.nn.relu(tf.nn.conv2d(L12, W13, strides=[1, 1, 1, 1], padding='SAME') + B13)

    FlatLayer = tf.reshape(L13, [-1, 8 * 8 * 128])
    Flat_W = tf.get_variable("Flat_W", shape=[8 * 8 * 128, 4096], initializer=tf.contrib.layers.xavier_initializer())
    Flat_B = tf.get_variable("Flat_B", initializer=tf.random_normal([4096], stddev=0.01))

    hypothesis = tf.matmul(FlatLayer, Flat_W) + Flat_B

    tf.summary.histogram("hypothesis", hypothesis)

    # define cost/Loss & optimizer
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=hypothesis, labels=Y))

    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

    #Accuracy
    correct_prediction = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))*100

    tf.summary.scalar("Cost",cost)
    accuracy_summary=tf.summary.scalar("Accuracy", accuracy)

    #Summary
    summary = tf.summary.merge_all()

    # GPU 사용 옵션
    config = tf.ConfigProto( allow_soft_placement=True)
    config.gpu_options.allow_growth = True
    config.gpu_options.per_process_gpu_memory_fraction = 0.95
    config.gpu_options.allocator_type = "BFC"
    sess = tf.Session(config=config)


    # Saver 선언
    saver = tf.train.Saver()
    sess.run(tf.global_variables_initializer())

    # train my model
    print("Learning start. It tackes sometime.")

    #Create summary writer
    summary_dir = "./PNLogs"
    writer = tf.summary.FileWriter(summary_dir + '/train')
    testWriter = tf.summary.FileWriter(summary_dir + '/Valid')
    writer.add_graph(sess.graph)
    global_step = 0

    ckpt = tf.train.get_checkpoint_state(os.path.dirname('./PNCheckpoint/'))
    if ckpt and ckpt.model_checkpoint_path:
        print(ckpt.model_checkpoint_path)
        saver.restore(sess, ckpt.model_checkpoint_path)
        print("\n체크포인트 파일 재사용 = ",ckpt.model_checkpoint_path)
        global_step = int(ckpt.model_checkpoint_path.rsplit('-',1)[1])
        print("global step = ",global_step)
    else:
        print("\n체크포인트 파일 새로 생성")

    for epoch in range(training_epochs):

        e_avg_cost = 0
        filename = './FenData/allFen.txt'

        with open('LearnCount.txt', 'r') as f:
            COUNT = int(f.readline())

        with open('iterList2.txt', 'r') as f:
            # 학습을 이어서 하기 위해 iter 횟수를 확인
            # iterList = f.readlines()
            i = int(f.readline())

        trainingFile = open(filename, 'r')

        batchsizeInput = []
        batchsizeOutput = []
        # batchsizeResult = []


        k = 0

        for m, line in enumerate(trainingFile):  # 학습한 이후 부터 다시 시작
            if COUNT <= m and m < COUNT + batchSize:
                if k % 1000 == 0:
                    print("\r", k, end="", flush=True)
                k += 1
                fenInform = line

                if fenInform == None:
                    print("\n파일 끝 도착: ", m, "\n")
                    break
                    # return batchsizeInput, batchsizeOutput

                fenInform = fenInform[:-1]
                fenInform = fenInform.split(":")  # ':'으로 나눈다. [0] 입력 fen, [1] 명령어, [2] 게임 결과

                # 파일에서 받은 fen을 보드에 입력
                board.set_fen(fenInform[0])

                # 입력 데이터 전처리
                batchsizeInput.append(b2a.board2array(board))
                batchsizeOutput.append(fl.convertOutput(fenInform[1]))
                # batchsizeResult.append(fl.convertResult(fenInform[2])) #가치망 사용할 때 입력 받음

                if m == (COUNT + batchSize-1): #배치사이즈 만큼 다 차면 학습을 시작

                    i += 1

                    print("\nNo.", i, " Training")
                    try:
                        pgnInput, pgnOutput = batchsizeInput ,batchsizeOutput
                        batch_xs, batch_ys = pgnInput[0:TRAIN], pgnOutput[0:TRAIN]
                        validInput, validOutput = pgnInput[TRAIN:], pgnOutput[TRAIN:]  # 2000개 검증데이터
                        trainInput, trainOutput = pgnInput[TRAIN - 3000:TRAIN], pgnOutput[TRAIN - 3000:TRAIN]  # 2000개 학습 데이터
                        feed_dict = {X: batch_xs, Y: batch_ys}

                        s, c, _, = sess.run([summary, cost, optimizer], feed_dict=feed_dict)
                        e_avg_cost += c / ITERATION
                        print("\n", global_step + batchSize, 'data learning / ', 'CNN Training :', '%04d' % (i + 1),
                              '   cost = ', c)
                    except:
                        print("학습 Error 다음 Iteration으로 continue")

                    global_step += batchSize
                    COUNT += batchSize

                    try:
                        # 정확도 판별
                        with tf.variable_scope("Validation"):
                            print('\nValidation Accuracy:', sess.run(accuracy, feed_dict={X: validInput, Y: validOutput}), "%")
                        with tf.variable_scope("Training"):
                            accu_sum, acc = sess.run([accuracy_summary, accuracy], feed_dict={X: trainInput, Y: trainOutput})
                            print('Train Accuracy:', acc, "%")
                    except:
                        print("accuracy 계산 Error")

                    try:
                        saver.save(sess, path, global_step=global_step)
                        writer.add_summary(s, global_step=global_step)
                        testWriter.add_summary(accu_sum, global_step=global_step)
                    except:
                        print("\nSaver or Summary 에러 \n")

                    # 학습이 끝나면 학습한 데이터의 숫자를 기록한다.
                    with open('LearnCount.txt', 'w') as f:
                        f.write(str(COUNT))
                    with open('iterList2.txt', 'w') as f:  # 'a'로 이어서 저장
                        # 학습을 반복한 횟수 i 저장
                        # f.write(str(i) + "\n")
                        f.write(str(i))
                    # 메모리를 줄이기 위한 소멸자 호출
                    del (pgnInput)
                    del (pgnOutput)
                    batchsizeInput.clear()
                    batchsizeOutput.clear()
                    # del(results)
                    k=0
                    print("-----------------------------------")

        trainingFile.close()
        print('                              %04d 번째 epoch' % (epoch + 1) + '  avg_cost = {:9}'.format(e_avg_cost))
        f.close()
        # 새 epoch를 돌리기 위해
        with open('LearnCount.txt', 'w') as f:
            f.write("0")
        with open('iterList2.txt', 'w') as f:
            f.write("0")
print('Learning Finished!')
