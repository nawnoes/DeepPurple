import math
import random

Cpuct = 3
class Node:


    def __init__(self, parent = None, command=None, policy_Score = 0, value_Score = 0): # 부모로 부터 파생 될때, 부모노드의 정보와 커맨드를 부여받음
        self.command = command  # 명령어
        self.color = None # 현재 노드의 색깔 True면 흰색, False 검은색
        self.visit = 0  # 방문횟수
        self.policy_Score = policy_Score # 정책망
        self.value_Score = value_Score  # 정책망
        self.win = 0  # 승
        self.draw = 0  # 무
        self.lose = 0  # 패
        self.child = []  # 자식 노드
        self.parent = parent  # 부모노드
        self.bear_Flag = False


    def set_Child(self,child):
        self.child = child
    def set_Color(self,color):
        self.color = color

    def get_Command(self):
        return self.command
    def get_Parent(self):
        return self.parent
    def get_Child(self):
        return self.child
    def get_Color(self):
        return self.color
    def get_Win(self):
        return self.win
    def get_Draw(self):
        return self.draw
    def get_Lose(self):
        return self.lose
    def get_Flag(self):
        return self.bear_Flag

    def on_Flag(self):
        self.bear_Flag = True
    def off_Flag(self):
        self.bear_Flag = False

    def add_Win(self, win):
        self.win += win
    def add_Draw(self,draw):
        self.draw += draw
    def add_Lose(self, lose):
        self.lose += lose
    def add_Visit(self,visit):
        self.visit += visit
    def add_ChildNode(self, node):
        self.child.append(node)

    def calc_selectingScore(self):
        #win/games + C_puct * policy_Score * ( root( sigma(other child visit) / ( 1 + my visit ) )
        score =  self.calc_Q() + self.calc_u()
        return score
    def calc_Q(self):
        return 0.5*(self.win)/( 1 + self.win+self.draw+self.lose) + 0.5*self.value_Score
    def calc_u(self):
        return Cpuct * self.policy_Score * math.sqrt(self.sum_otherVisit()+1) / (1 + self.visit)


    def sum_otherVisit(self):
        sumAll = self.parent.sum_childVisit()
        return sumAll - self.visit

    def sum_childVisit(self):
        lenth = len(self.child)
        sum = 0
        for i in range(lenth):
            sum += self.child[i].visit
        return sum

    def get_bestChild(self):
        #child에서 가장 selectingScore가 최대인 후보를 선택
        lenth = len(self.child)
        index = 0
        max = 0
        candidates = []
        for i in range(lenth):
            if max < self.child[i].calc_selectingScore():
                #점수가 최대값일때 index를 가진다
                max = self.child[i].calc_selectingScore()
                index = i
                candidates.clear()
                candidates.append(i)

            elif max == self.child[i].calc_selectingScore():
                #선택된 값이 최대값과 같다면 후보로 추가
                candidates.append(i)

        if len(candidates) == 1:
            #반복문이 끝났을때 index는 최대값을 가진다
            #print(max)
            return self.child[index] # 최대값 반환
        else : #선택된 것이 없다면 랜덤으로 자식 선택
            try:
                choice = random.choice(candidates)
            except:
                #print(lenth)
                self.child[index]
            #print(max)
            return self.child[choice]


    def should_expand(self, point):
        if self.visit == point:
            return True
        else:
            return False

    def sumChildPolicyScore(self):
        sum = 0
        for child in self.child:
            sum += child.policy_Score
        return sum

    def get_policyDistribution(self):
        scores = []
        sum = self.sumChildPolicyScore()

        for child in self.child:
            score = child.policy_Score /sum
            scores.append(score)

        return scores


    def renew_result(self, result):
        result = self.trans_result(result)

        if result == 1:  # 백승
            if not self.color:
                self.add_Win(1)
            else:
                self.add_Lose(1)
            return

        elif result == 0:  # 무승부
            self.add_Draw(1)
            return

        elif result == -1:  # 흑승
            if not self.color:
                self.add_Lose(1)

            else:
                self.add_Win(1)
            return
        else:
            print("result is not formal")

    def For_root_choice(self):
        lenth = len(self.child)
        max = -1
        index = 0

        for i in range(lenth):
            if max < self.child[i].visit:
                max = self.child[i].visit
                #print(max)
                index = i
        return index

    def is_root(self):
        if self.parent:
            return False
        else:
            return True

    def print_childInfo(self):
        lenth = len(self.child)
        print("child")
        for i in range(lenth):
            print(i,"> win:", self.child[i].win, "loss:", self.child[i].lose, "draw:", self.child[i].draw, "command:", self.child[i].command, self.child[i].visit)
            print(self.child[i].calc_selectingScore())
            print("ps : ",self.child[i].policy_Score)
            print("q : ",self.child[i].calc_Q())
            print("u : ",self.child[i].calc_u())
            print("move : ", self.child[i].get_Command())

    def trans_result(self, result):
        rm = {'1-0': 1, '0-1': -1, '1/2-1/2': 0}  # 게임의 끝, ( 백승 = 1, 흑승 = -1, 무승부, 0 )

        return rm[result]

    #
    # def get_bestPolicyScoreChildIndex(self):
    #     scores = self.get_policyDistribution()
    #     max = -1000
    #     index = -1
    #     for i in range(len(scores)):
    #         if max > scores[i]:
    #             max = scores[i]
    #             index = i
    #     return index

    # def get_AllChild(self):  # 모든 자식 노드를 반환
    #     if self.bear_Flag == False:
    #         return -1
    #     elif len(self.child) == 0:
    #         return 0
    #     else:
    #         return self.child
    #
    # def visited(self):
    #     self.visit += 1

