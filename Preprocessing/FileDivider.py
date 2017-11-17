from FindFile import FindFile as ff


f = ff()
fileList = ff().getDiretoryList('./KingBase/')# 끝에 '/'붙여야한다

for playerName in fileList:
    # try:
    f.dividePgnFile(playerName)
    # except:
    #     continue