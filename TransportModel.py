class TransportModel:
    # 基本变量定义
    name = ""
    sources = []  # 产地产量
    sourceNames = []
    sales = []  # 销地销量
    saleNames = []
    prices = []  # 价格
    pu = []
    pv = []
    numberOfSources = 0
    numberOfSales = 0
    transProject = []
    totalProduction = 0
    totalSale = 0
    minCheckNumber = {}
    circleLoop = []
    optFound = False  # 最优解标记

    def initModel(self, dataLines):
        # 维度
        self.numberOfSources = len(dataLines) - 2  # 产地 = 行数 - 1
        self.numberOfSales = len(dataLines[0].split()) - 2  # 销地 = 列数 - 2
        # 最优解标志
        self.optFound = False
        # 开始识别
        for i in range(len(dataLines)):
            line = dataLines[i]
            cols = line.split()
            if i == 0:  # 识别销地
                for j in range(len(cols)):
                    if j > 0:
                        if j < self.numberOfSales + 1:  # 销地名称
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
                            if j < self.numberOfSales + 1:  # 价格
                                v.append(float(cols[j]))
                            else:
                                self.sources.append(float(cols[j]))
                    self.prices.append(v)
                else:
                    for j in range(len(cols)):
                        if (j > 0 and j < self.numberOfSales + 1):
                            self.sales.append(float(cols[j]))

        print("共有%d产地：" % (self.numberOfSources), self.sourceNames)
        print("产量：", self.sources)
        print("共有%d销地：" % (self.numberOfSales), self.saleNames)
        print("销量：", self.sales)
        print("运价表：")
        print(self.prices)
        self.totalProduction = sum(self.sources)
        self.totalSale = sum(self.sales)
        self.leftProduction = self.totalProduction
        return

    def optimization(self):
        k = 0
        while not self.optFound:
            k += 1
            print("\n第%d次迭代..." % k)
            print("调运方案：")
            self.displayTransProject()
            print()
            self.calculatePotential()
            self.calculateCheckNumber()
            self.findMinCheckNumber()
            if not self.optFound:
                self.findCloseLoop()
                self.adjustTransportProject()
                self.showResult()
        return

    def displayTransProject(self):
        for e in self.transProject:
            tmp = "["
            for ee in e:
                tmp += " %5.1f" % (ee["value"])
            tmp += "]"
            print(tmp)
        return

    def showTransProject(self):
        for e in self.transProject:
            print(e)
        return

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

        # 最小元素法
        def miniElementIteration(self):

            print("最小元素法初始调运方案：")
            finishedSource = []
            finishedTarget = []
            tempProduction = self.sources.copy()
            tempSales = self.sales.copy()
            leftProduction = self.totalProduction

            while (leftProduction > 0):
                # 查找最小元素
                plist = []
                for i in range(self.numberOfSources):
                    for j in range(self.numberOfSales):
                        p = {}
                        if (not ((i in finishedSource) or (j in finishedTarget))):
                            p["i"] = i
                            p["j"] = j
                            p["value"] = self.prices[i][j]
                            plist.append(p)
                miniE = min(plist, key=lambda e: e["value"])
                print("最小元素：", miniE)

                # 查找调运量 - -与横纵坐标相关
                i = miniE["i"]
                j = miniE["j"]
                transValue = min(tempProduction[i], tempSales[j])

                # 填写调运方案
                self.transProject[i][j]["value"] = transValue
                self.transProject[i][j]["isBase"] = True

                leftProduction -= transValue
                tempProduction[i] -= transValue
                tempSales[j] -= transValue
                row = not (tempProduction[i] > 0)
                col = not (tempSales[j] > 0)

                # 登记完成的行列
                if (row):
                    finishedSource.append(i)
                if (col):
                    finishedTarget.append(j)

                # 同时划去一行 & 一列
                if ((row and col) and (leftProduction > 0)):
                    print("同时满足：%d,%d" % (i, j))
                    self.transProject[i][j - 1]["value"] = 0
                    self.transProject[i][j - 1]["isBase"] = True
            return

        initMethod = {
            '1': northwestCornerIteration,
            '2': miniElementIteration
        }

        initEmptyTransportProject(self)
        methodIndex = input("请选择初始化方法(1--西北角, 2--最小元素法)：")
        if (methodIndex == ''):
            methodIndex = '2'
        initMethod[methodIndex](self)
        self.showTransProject()

        return

    def calculatePotential(self):
        finishedU = [0]
        finishedV = []
        self.pu.clear()
        self.pv.clear()
        for i in range(self.numberOfSources):
            self.pu.append(0.0)
        for i in range(self.numberOfSales):
            self.pv.append(0.0)
        plist = []
        for i in range(self.numberOfSources):
            for j in range(self.numberOfSales):
                p = {}
                if (self.transProject[i][j]["isBase"]):
                    p["i"] = i
                    p["j"] = j
                    p["price"] = self.prices[i][j]
                    plist.append(p)
        plist.sort(key=lambda e: e["i"])
        print("基变量：", plist)
        kk = 0
        while ((len(finishedU) < self.numberOfSources) or (len(finishedV) < self.numberOfSales)):
            kk += 1
            for k in range(len(plist)):
                i = plist[k]["i"]
                j = plist[k]["j"]
                if (i in finishedU):
                    if not (j in finishedV):
                        self.pv[j] = self.prices[i][j] - self.pu[i]
                        finishedV.append(j)
                else:
                    if (j in finishedV):
                        self.pu[i] = self.prices[i][j] - self.pv[j]
                        finishedU.append(i)
            print("位势计算迭代%d步..." % kk)
            if (kk > 10):
                print("死循环了...")
                break
        print("位势：")
        print("U:", self.pu)
        print("V:", self.pv)
        return

    def calculateCheckNumber(self):
        for i in range(self.numberOfSources):
            for j in range(self.numberOfSales):
                if (not self.transProject[i][j]["isBase"]):
                    self.transProject[i][j]["check"] = self.prices[i][j] - self.pu[i] - self.pv[j]
        self.showTransProject()
        return

    def findMinCheckNumber(self):
        clist = []
        for i in range(self.numberOfSources):
            for j in range(self.numberOfSales):
                c = {}
                if (not self.transProject[i][j]["isBase"]):
                    c["i"] = i
                    c["j"] = j
                    c["v"] = self.transProject[i][j]["check"]
                    clist.append(c)
        mine = min(clist, key=lambda e: e["v"])
        print("最小检验数：", mine)
        self.minCheckNumber = mine
        self.optFound = (mine["v"] >= 0)
        if (self.optFound):
            print("获得最优解.")
        return

    def findCloseLoop(self):
        closeLoop = []
        front = 0
        rear = 0
        # 定义起始点
        startPoint = {}
        startPoint["i"] = self.minCheckNumber["i"]
        startPoint["j"] = self.minCheckNumber["j"]
        startPoint["pre"] = -1
        startPoint["flag"] = 1
        closeLoop.append(startPoint)
        # 开始搜索
        while (front <= rear):
            x = closeLoop[front]["i"]
            y = closeLoop[front]["j"]
            if (closeLoop[front]["flag"] == 1):
                i = x
                for j in range(self.numberOfSales):
                    if (self.transProject[i][j]["isBase"]):
                        rear += 1
                        p = {}
                        p["i"] = i
                        p["j"] = j
                        p["pre"] = front
                        p["flag"] = 0
                        closeLoop.append(p)
                        if (j == startPoint["j"]):
                            print("找到了:", closeLoop)
                            i = rear
                            self.getCircleLoop(closeLoop, i)
                            return
                        # -- 是否需要登记这一个基变量点？
            else:
                j = y
                for i in range(self.numberOfSources):
                    if (self.transProject[i][j]["isBase"]):
                        rear += 1
                        q = {}
                        q["i"] = i
                        q["j"] = j
                        q["pre"] = front
                        q["flag"] = 1
                        closeLoop.append(q)
                        # 需要登记吗？
            front += 1
        print("到头了:", closeLoop)
        return

    def getCircleLoop(self, closeLoop, i):
        self.circleLoop.clear()
        while (i != -1):
            self.circleLoop.append(closeLoop[i])
            i = closeLoop[i]["pre"]
        print("闭回路：", self.circleLoop)
        tmp = ""
        for e in self.circleLoop:
            if tmp == "":
                tmp += "(%d,%d)" % (e["i"], e["j"])
            else:
                tmp += "->(%d,%d)" % (e["i"], e["j"])
        print(tmp)
        return

    def adjustTransportProject(self):
        if self.optFound:
            return

        vlist = []
        for i in range(len(self.circleLoop)):
            x = self.circleLoop[i]["i"]
            y = self.circleLoop[i]["j"]
            # 最小调整量是关键--对角线上的两点，取最小。偶数点取最小
            if (self.transProject[x][y]["isBase"] and (i % 2 == 0)):
                vlist.append(self.transProject[x][y]["value"])
        minv = min(vlist)
        print("调整量是：%f" % minv)
        # 开始调整
        for i in range(len(self.circleLoop)):
            x = self.circleLoop[i]["i"]
            y = self.circleLoop[i]["j"]
            ov = self.transProject[x][y]["value"]
            if i % 2 == 0:
                self.transProject[x][y]["value"] = ov - minv
                if ov == minv:
                    self.transProject[x][y]["isBase"] = False
            else:
                self.transProject[x][y]["value"] = ov + minv
                self.transProject[x][y]["isBase"] = True
        print("调整结束：")
        self.showTransProject()
        self.displayTransProject()
        # 检验数清空
        for i in  range(self.numberOfSources):
            for j in range(self.numberOfSales):
                if (self.transProject[i][j].__contains__('check')):
                    self.transProject[i][j].pop('check')
        print("删除上次检验数的计算结果")
        #self.showTransProject()
        return

    def showResult(self):
        cost = 0
        for i in range(self.numberOfSources):
            for j in range(self.numberOfSales):
                if (self.transProject[i][j]["isBase"]):
                    cost += self.transProject[i][j]["value"] * self.prices[i][j]
        print("当前运费：", cost)
        return
