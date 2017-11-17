import pickle
import ForFenMake_LoadData as LD
from Symmtry_OneHotEncoding import OneHotEncode as OHE

ohe = OHE()
rd = LD.pgn_reader('./test.pgn')
# input,  moveOutput, onehotOutput , result \
tmp = rd.get_allData()

with open('input.txt','wb') as f:
       pickle.dump(tmp,f)

# with open('output.txt', 'wb') as f:
#     pickle.dump(onehotOutput, f)
with open('input.txt','rb') as f:
    inputdata=pickle.load(f)

print(inputdata)