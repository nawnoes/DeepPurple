import ForFenMake_LoadData as LD
from Symmtry_OneHotEncoding import OneHotEncode as OHE

ohe = OHE()
rd = LD.pgn_reader('./test.pgn')
input, onehotOutput , result = rd.get_allData()
print()
print(input[0])

for i in range(len(input)):
    print(ohe.onehotToMove4096(onehotOutput[i]))
    print(ohe.uciMoveToOnehot(ohe.onehotToMove4096(onehotOutput[i])) == onehotOutput[i])
    print("----------------")
