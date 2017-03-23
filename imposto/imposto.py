class TaxStrategy(object):
    def __init__(self):
        super().__init__()
    def calculate(self,income:float)->float:
        return income*self.getAliquot()
    def getAliquot(self)->float:
        raise NotImplemented('Abstract method')

class TaxStrategyT0(TaxStrategy):
    def getAliquot(self)->float:
        return 0

class TaxStrategyT1(TaxStrategy):
    def getAliquot(self)->float:
        return 0.075

class TaxStrategyT2(TaxStrategy):
    def getAliquot(self)->float:
        return 0.15

class TaxStrategyT3(TaxStrategy):
    def getAliquot(self)->float:
        return 0.225

class TaxStrategyT4(TaxStrategy):
    def getAliquot(self)->float:
        return 0.275

class TaxCalculator(object):
    taxStrategy = None
    income = None
    def __init__(self, income:float):
        income = float(income)
        super().__init__()
        self.income = income
        self.autoselectStrategy()
    def autoselectStrategy(self):
        if   self.income <= 1710.78:
            self.taxStrategy = TaxStrategyT0()
        elif self.income <= 2563.91:
            self.taxStrategy = TaxStrategyT1()
        elif self.income <= 3418.59:
            self.taxStrategy = TaxStrategyT2()
        elif self.income <= 4271.59:
            self.taxStrategy = TaxStrategyT3()
        else:
            self.taxStrategy = TaxStrategyT4()
        return
    def calculateTax(self)->float:
        return self.taxStrategy.calculate(self.income)
