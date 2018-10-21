class TransportModel:
    # 基本变量定义
    name = ""
    sources = []  # 产地产量
    sourceNames = []
    sales = []  # 销地销量
    saleNames = []
    prices = []  # 价格
    numberOfSource = 0
    numberOfSale = 0

    def initModel(self, dataLines):
        # 维度
        self.numberOfSource = len(dataLines) - 2  # 产地 = 行数 - 1
        self.numberOfSale = len(dataLines[0].split()) - 2  # 销地 = 列数 - 2
        # 开始识别
        for i in range(len(dataLines)):
            line = dataLines[i]
            cols = line.split()
            if i == 0:  # 识别销地
                for j in range(len(cols)):
                    if j > 0:
                        if j < self.numberOfSale + 1:   # 销地名称
                            self.saleNames.append(cols[j])
                    else:
                        name = cols[j]  # 名字--问题的名称
            else:
                if i < self.numberOfSource + 1:
                    # 开始识别价格
                    v = []
                    for j in range(len(cols)):
                        if j == 0:
                            self.sourceNames.append(cols[j])
                        else:
                            if j < self.numberOfSale + 1:   # 价格
                                v.append(float(cols[j]))
                            else:
                                self.sources.append(float(cols[j]))
                    self.prices.append(v)
                else:
                    for j in range(len(cols)):
                        if (j>0 and j < self.numberOfSale + 1):
                            self.sales.append(float(cols[j]))

        print("共有%d产地：" % (self.numberOfSource), self.sourceNames)
        print("产量：", self.sources)
        print("共有%d销地：" % (self.numberOfSale), self.saleNames)
        print("销量：", self.sales)
        print("运价表：")
        print(self.prices)
        return

    def initTransportProject(self):

        # 西北角法
        def northwestCornerIteration(self):
            print("西北角法初始调运方案：")
            return

        #最小元素法
        def miniElementIteration(self):
            print("最小元素法初始调运方案：")

            return

        initMethod = {
            '1': northwestCornerIteration,
            '2': miniElementIteration
        }

        methodIndex = input("请选择初始化方法(1--西北角, 2--最小元素法)：")
        if (methodIndex==''):
            methodIndex = '2'
        initMethod[methodIndex](self)

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


