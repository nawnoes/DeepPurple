import Tree as TR

class MontecarloTreeSearch:
    def __init__(self, searchRepeatNum, searchDepth, expendPoint):
        self.tree = TR.Tree()
        self.searchDepth = searchDepth
        self.expendPoint = expendPoint
        self.searchRepeatNum = searchRepeatNum
    def MCTS(self):
        for i in range(self.searchRepeatNum):
            print("\r%d" % i , end="")
            self.search()
        bestMove = self.selectBiggestChildrenValue()
        return bestMove

    def search(self):
        depth = 2
        while True:
            selectionResult = self.selection(depth)
            depth +=1
            if selectionResult ==0 or selectionResult ==2:
                # 0 gameover, 1 more, 2 simulation
                break
        if selectionResult != 0:
            #selection 에서 게임이 끝나지 않은 경우.
            #확장과 시뮬레이션 진행
            result = self.expansion()

            if not result:
                result = self.rolloutSimulation()
    def selection(self, depth):
        if depth == self.searchDepth:
            return 0
        if self.tree.get_GameOver():
            return 0
        else: #게임이 끝나지 않았다면
            if self.searchDepth>depth:
                if not self.tree.currentNode.get_Flag():
                    #정책망을 통해 자식 노드 생성
                    self.tree.make_policyNextChildren()
                #다음 노드로
                try:
                    self.tree.go_next()
                except:
                    return 0
                return 1
            else: #깊이기준을 초과 했다면 정해진 depth 초과
                if self.tree.currentNode.get_Flag():
                    #자식이 있다면 자식노드로 이동
                    self.tree.go_next()
                    return 1
                else: #게임 끝나지 않았는데 자식도 없다(???)
                    return 2

    def evaluation(self):

    def expansion(self):
        if self.tree.currentNode.should_expand(self.expendPoint):
            self.tree.make_policyNextChildren()
            self.tree.go_next()
            if self.tree.board_stack.get_GameOver():
                return self.tree.board_stack.get_Result() #게임의 결과 반환
            else: #게임이 끝나지 않으면 다시 확장
                return self.expansion()
        else: #모든 확장을 끝낸다면 False 반환
            return False
    def backpropagation(self,gameResult):
        if self.tree.currentNode.is_root():
            return 0
        else:
            self.tree.currentNode.renew_result(gameResult)
            self.tree.go_parrent()
            return self.backpropagation(gameResult)
    def selectBiggestChildrenValue(self):
    def rolloutSimulation(self):