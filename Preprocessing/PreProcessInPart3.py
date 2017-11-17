import pickle
import LoadData_Part3 as LD
from OneHotEncoding import OneHotEncode as OHE
import time

ohe = OHE()
rd = LD.pgn_reader('./test.pgn')
# input,  moveOutput, onehotOutput , result \
start = time.time()
tmp = rd.get_allData()
end = time.time() - start


print(end)
with open('input.txt','wb') as f:
       pickle.dump(tmp,f)

# with open('output.txt', 'wb') as f:
#     pickle.dump(onehotOutput, f)
# with open('input.txt','rb') as f:
#     inputdata=pickle.load(f)
#
# print(inputdata)