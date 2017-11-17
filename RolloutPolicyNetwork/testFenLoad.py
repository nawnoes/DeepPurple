from FenLoad import FenLoad as FL
import time
filename = './FenData/whiteFen-1.txt'
#입력한 데이터가 불러오는데 얼마나 걸리는지 확인하는것
fl = FL()
start = time.time()
tmp = fl.getBatchSizeData(filename,10000)
end =start -time.time()
print(end)