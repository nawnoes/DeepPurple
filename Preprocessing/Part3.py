import pickle
import LoadData_Part3 as LD
from OneHotEncoding import OneHotEncode as OHE
import time

ohe = OHE()
rd = LD.pgn_reader('./test.pgn')
# input,  moveOutput, onehotOutput , result \
start = time.time()
tmp = rd.allData()
end = time.time() - start
print(end)