from Symmtry_OneHotEncoding import OneHotEncode as OHE

ohe = OHE()

movList = ohe.getSymPosition()
for m in movList:
    mov = ohe.symmetryMove2move(m)
    symmov = ohe.move2symmetryMove(mov)
    print("sym: ", m , "//  ", mov, "// ", symmov," ", ohe.uciMoveToOnehot(mov)==ohe.moveToSymmetryOnehot(symmov))
    # onhot = ohe.moveToSymmetryOnehot(m)
    # # print(onhot)
    # mov=ohe.onehotToSymmetryMove4096(onhot)
    # onhot2 = ohe.moveToSymmetryOnehot(mov)
    # print("명령어 : ", mov ," //Symmetry를  일반 명령으로 : ", ohe.onehotToMove4096(onhot), "  일반명령을 Symmetry으로 : ", ohe.onehotToSymmetryMove4096(onhot2)," ",onhot == onhot2)