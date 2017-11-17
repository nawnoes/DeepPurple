import random

class MovesMaker: #legal_Moves에서 명령어로 배열로 받기 위한 클래스

    def __init__(self):
        self.legal_Moves_List = []


    def make(self, str):
        start = str.find("(") # ( 이 시작하는 위치 반환
        mid = str[start+1:-2] # ( 의 다음 위치 부터 마지막 -2 까지 반환
        self.legal_Moves_List = mid.split(", ") #','만으로 자르면 문자열 앞에 공백 발생

        return self.legal_Moves_List

    def get_RandomMove(self):
        #legal_Moves_List에서 MCTS에서 사용할
        #임의의 명령어를 랜덤으로 받기 위한 함수

        if self.legal_Moves_List != None: #게임 종료시에는 legal_Moves가 없음.
            # 0부터 legal_Moves_List-1 사이의 숫자 반환
            index = random.randrange(0,len(self.legal_Moves_List))
            return self.legal_Moves_List.pop(index)
        # make후에 legal_Mmoves_List가 가리키는게 없다면 가능한 노드가 없는것
        return None