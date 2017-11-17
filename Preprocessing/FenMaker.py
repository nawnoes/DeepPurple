#fen 기보를 만들기 위한 파일

import ForFenMake_LoadData as LD
from FindFile import FindFile as ff
import time

#fen으로 생성할 pgn 파일 Load

start = time.time()
getFen = ff()
fileList = getFen.getDiretoryList('./KingBase/')# 끝에 '/'붙여야한다

for fileName in fileList:
    if getFen.is_UsedName('UsedFile.txt',fileName):
        continue
    rd = LD.pgn_reader(fileName)
    rd.fenMake()
    fortime = time.time() -start
    print(fortime)
# index, input, output, r = rd.get_alldata()

end = time.time() -start

print(end)