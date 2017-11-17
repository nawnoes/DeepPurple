import Tree as TR

class Monte:
    def __init__(self, repeat_num = 3, select_depth = 5, simulation_num = 1,expend_point = 5):
        self.tree = TR.Tree()  # 트리 생성
        self.expand_point = expend_point  # 확장 기준값
        self.select_depth = select_depth  # 선택을 종료할 깊이
        self.repeat_num = repeat_num  # 반복 수행할 횟수
        self.simulation_num = simulation_num

    def set_state(self,Board):
        self.tree.reset_board(Board)

    def predict(self):
        for i in range(self.repeat_num):
            print("\r%d" % i , end="")
            self.search()

        # choice
        choice = self.choice()
        print("")
        return choice

    def search(self):
        depth = 2
        select_Flag = True

        while select_Flag:
        # selection
            result_selection = self.selection(depth)  # selection에서 게임이 끝이 났으면 0, 끝이 안났으면 1
            print(self.tree.get_currentBoard().is_stalemate())
            flag = True
            depth += 1
            if result_selection == 0 or result_selection == 2 : # 0 gameover 1 more 2 simulation
                select_Flag = False

        if result_selection != 0:  # 선택에서 게임이 끝나지 않앗으면 확장과 시뮬레이션
            # expantion
            result = self.expantion()

            if not result:
                # simulation
                result = self.simulation()
        else:
            result = self.tree.get_Result()

        # backpropagation
        self.backpropagation(result)

    def selection(self, depth):
        if depth == 5:
            return 0
        #print("selection")
        if self.tree.get_GameOver():  # 보드가 게임이 끝난 상태라면 ( 흰승 : 1, 검은승 : -1, 무: 0
            return 0

        else:  # 보드가 게임이 끝나지 않았다면

            if self.select_depth > depth: # select해야할 깊이라면
                if not self.tree.currentNode.get_Flag():  # 자식노드 체크
                    # 자식 노드 생성
                    self.tree.make_policyNextChildren()
                # 다음 노드로
                try :
                    self.tree.go_next()
                except:
                    return 0
                return 1

            else:  # 깊이 기준을 초과하였다면 정해진 depth 초과
                if self.tree.currentNode.get_Flag(): # 자식이 있으면 자식으로
                    self.tree.go_next()
                    return 1

                else:  # 자식이 없다면 이제 끝
                    return 2

    def expantion(self):

        if self.tree.currentNode.should_expand(self.expand_point):
            self.tree.make_policyNextChildren()
            self.tree.go_next()
            if self.tree.board_stack.get_GameOver() :
                return self.tree.board_stack.get_Result() #게임의 결과 반환
            else :#게임이 끝나지 않으면 다시 확장
                return self.expantion()
        else: #모든 확장을 끝낸다면 False 반환
            return False

    def simulation(self):

        tmpBoard = self.tree.get_currentBoard().copy()
        simul_count = 0

        while not tmpBoard.is_game_over():
            simul_count += 1
            tmpBoard = self.tree.make_policyNextRandomChildBoard(tmpBoard)

        result = tmpBoard.result()

        return result

    def backpropagation(self, result):
        if self.tree.currentNode.is_root():
            return 0
        else:
            self.tree.currentNode.renew_result(result)
            self.tree.go_parrent()
            return self.backpropagation(result)

    def choice(self):
        root = self.tree.get_RootNode()
        index = root.For_root_choice()
        self.tree.root_Node.print_childInfo()
        return root.child[index].command
