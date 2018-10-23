class TransportModel:
    # 基本变量定义
    name = ""
    sources = []  # 产地产量
    sourceNames = []
    sales = []  # 销地销量
    saleNames = []
    prices = []  # 价格
    numberOfSources = 0
    numberOfSales = 0
    transProject = []
    totalProdtion = 0
    totalSale = 0
    leftProduction = 0

    def initModel(self, dataLines):
        # 维度
        self.numberOfSources = len(dataLines) - 2  # 产地 = 行数 - 1
        self.numberOfSales = len(dataLines[0].split()) - 2  # 销地 = 列数 - 2
        # 开始识别
        for i in range(len(dataLines)):
            line = dataLines[i]
            cols = line.split()
            if i == 0:  # 识别销地
                for j in range(len(cols)):
                    if j > 0:
                        if j < self.numberOfSales + 1:   # 销地名称
                            self.saleNames.append(cols[j])
                    else:
                        name = cols[j]  # 名字--问题的名称
            else:
                if i < self.numberOfSources + 1:
                    # 开始识别价格
                    v = []
                    for j in range(len(cols)):
                        if j == 0:
                            self.sourceNames.append(cols[j])
                        else:
                            if j < self.numberOfSales + 1:   # 价格
                                v.append(float(cols[j]))
                            else:
                                self.sources.append(float(cols[j]))
                    self.prices.append(v)
                else:
                    for j in range(len(cols)):
                        if (j>0 and j < self.numberOfSales + 1):
                            self.sales.append(float(cols[j]))

        print("共有%d产地：" % (self.numberOfSources), self.sourceNames)
        print("产量：", self.sources)
        print("共有%d销地：" % (self.numberOfSales), self.saleNames)
        print("销量：", self.sales)
        print("运价表：")
        print(self.prices)
        self.totalProdtion = sum(self.sources)
        self.totalSale = sum(self.sales)
        self.leftProduction = self.totalProdtion
        return

    def showTransProject(self):
        for e in self.transProject:
            print(e)

    def initTransportProject(self):

        # 初始化一个空的调运方案
        def initEmptyTransportProject(self):
            for i in range(0, self.numberOfSources):
                pe = []
                for j in range(0, self.numberOfSales):
                    p = {}
                    p["value"] = 0.0
                    p["isBase"] = False
                    pe.append(p)
                self.transProject.append(pe)
            print("空调运方案：")
            self.showTransProject()
            return

        # 西北角法
        def northwestCornerIteration(self):
            print("西北角法初始调运方案：")
            # 从西北角开始

            rowIndex = 0
            colIndex = 0
            tempProduction = self.sources.copy()
            tempSalesVolume = self.sales.copy()
            while ((self.leftProduction > 0) and (rowIndex < self.numberOfSources) and (colIndex < self.numberOfSales)):
                row = False
                col = False
                # 查找调运量 - -与横纵坐标相关
                transValue = min(tempProduction[rowIndex], tempSalesVolume[colIndex])
                # 填写调运方案
                self.transProject[rowIndex][colIndex]["value"] = transValue
                self.transProject[rowIndex][colIndex]["isBase"] = True
                # 登记完成的行列
                tempProduction[rowIndex] -= transValue
                tempSalesVolume[colIndex] -= transValue

                if (tempProduction[rowIndex] == 0):
                    row = True
                    rowIndex += 1
                if (tempSalesVolume[colIndex] == 0):
                    col = True
                    colIndex += 1
                # 如果同时行列都满足，添加一个零(同列)
                if (row and col):
                    if ((rowIndex < self.numberOfSources) and (colIndex < self.numberOfSales)):
                        self.transProject[rowIndex][colIndex - 1]["value"] = 0
                        self.transProject[rowIndex][colIndex - 1]["isBase"] = True
                # 更新剩余产量
                self.leftProduction -= transValue
            return

        #最小元素法
        def miniElementIteration(self):

            print("最小元素法初始调运方案：")
            finishedSource = []
            finishedTarget = []
            leftProduction = self.totalProduct

            tempProduction = self.sources.copy()
            tempSales = self.sales.copy()
            # 查找最小元素
            plist = []
            for i in range(self.numberOfSources):
                for j in range(self.numberOfSales):
                    p = {}
                    if (not ((i in finishedSource) or (j in finishedTarget))):
                        p["i"] = i
                        p["j"] = j
                        p["value"] = self.prices[i][j]
            miniE = min(plist, key=lambda e: e["value"])
            print("最小元素：", miniE)

            # 查找调运量 - -与横纵坐标相关
            i = miniE["i"]
            j = miniE["j"]
            transValue = min(tempProduction[i], tempSales[j])

            // 填写调运方案
            transProject[miniE.i][miniE.j] = transValue
            transProjectFlag[miniE.i][miniE.j] = true
            calculateTotalCost()

            // 登记完成的行列
            if (transValue == tempProduction[miniE.i]) {
            finishedSource.add(miniE.i)
            }
            tempProduction[miniE.i] -= transValue

            if (transValue == tempSalesVolume[miniE.j]) {
            finishedTarget.add(miniE.j)
            }
            tempSalesVolume[miniE.j] -= transValue

            if (tempProduction[miniE.i] == tempSalesVolume[miniE.j]) {
            // 同时划去一行 & 一列
            println("同时满足：${stepIndex}  ${miniE}")
            }

            // 更新剩余产量
            leftProduction -= transValue

            return

        initMethod = {
            '1': northwestCornerIteration,
            '2': miniElementIteration
        }

        initEmptyTransportProject(self)
        methodIndex = input("请选择初始化方法(1--西北角, 2--最小元素法)：")
        if (methodIndex==''):
            methodIndex = '2'
        initMethod[methodIndex](self)
        self.showTransProject()

        return

    def calculatePotential(self):
        return

    def calculateCheckNumber(self):
        return

    def adjustTransportProject(self):
        return

    def findCloseLoop(self):
        return

    def showResult(self):
        return


