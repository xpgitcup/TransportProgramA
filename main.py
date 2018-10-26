from TransportModel import TransportModel

#filename = "p.79.例1.dat"
filename = "2018-2019-1-2.dat"
try:
    with open(filename) as sourceFile:
        dataLines = sourceFile.readlines()
        print(dataLines)
    model = TransportModel()
    model.initModel(dataLines)
    model.initTransportProject()
    model.displayTransProject()
    model.showResult()
    model.optimization()
    model.showResult()
    print("计算完成...")
except IOError:
    print("文件不存在...")
print("Bye...")
