import os


class FindFile:

    def __init__(self):
        self.count = 0

    def getDiretoryList(self,path):
        #path 상에 있는 모든 .pgn형식의 파일 리스트를 반환
        fileList=[]
        for i in os.listdir(path): #해당 경로의 파일리스트를 받는 방법
            if ".pgn" in i:
                print(path+i)
                fileList.append(path+i)
        return fileList

    def is_emptyFile(self,path):
        #path 상에 있는 diretory의 내부가 비어있는지 확인
        fileList =[]
        for i in os.listdir(path):  # 해당 경로의 파일리스트를 받는 방법
            fileList.append(path + i)

        if len(fileList) == 0 : #리스트의 길이가 0 인경우 directory는 비어 있으므로 True
            return True
        else:
            return False

    def dividePgnFile(self,filePath):
        #path에 있는 기보 파일의 크기가 크므로 100kb 이하로 만들어 주기 위해
        #100kb는 대략 100000byte
        file = open(filePath, "r")#파이썬은 ANSI 방식으로 된 파일만 읽을 수 있다.
        # file = open(filePath,"r", "utf-8")#UTF-8로 작성된 파일을 읽기 위한 방법
        fileLinesList = file.readlines() # 파일의 모든 내용을 한 줄씩 List로 받는 함수
        currentFilePath = None
        flag =True


        for i in range(len(fileLinesList)):
            if flag == True:
                currentFilePath = filePath[:-4] + '-%d'%self.count + filePath[-4:]
                tmpFile = open(currentFilePath,"a")
                self.count +=1
                flag = False
            if "[Event" in fileLinesList[i] and os.path.getsize(currentFilePath) >90000.: #기보의 시작이 [event로 시작 하므로
                flag = True
                tmpFile.close()#이전 파일을 닫음
                currentFilePath = filePath[:-4] + '-%d'%self.count + filePath[-4:] #새로 열 파일의 경로를 생성
                self.count +=1
                tmpFile = open(currentFilePath,"a")
                tmpFile.write(fileLinesList[i])
                flag = False
            else:
                tmpFile.write(fileLinesList[i])
        file.close()
        os.remove(filePath) #경로의 파일을 삭제하는 함수

    def is_UsedName(self,path,name):
        file = open(path, "r")
        linesList = file.readlines()  # 파일의 모든 내용을 한 줄씩 List로 받는 함수

        for contents in linesList:
            if name in contents:
                return True # 현재 파일에 들어 있으므로 학습된것
        return False #학습되지 않았으므로 False return
    def is_LastLearnedFile(self,path,name):
        file = open(path, "r")
        linesList = file.readlines()  # 파일의 모든 내용을 한 줄씩 List로 받는 함수

        for contents in linesList:
            if name in contents:
                return True # 현재 파일에 들어 있으므로 학습된것
        return False #학습되지 않았으므로 False return
