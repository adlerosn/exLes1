import calc

class Input:
    def get(self):
        return None

class UserInput(Input):
    def get(self):
        return input()

class FakeInput(Input):
    _waiting = None
    def __init__(self):
        super().__init__()
        self._waiting = list()
    def append(self,line):
        self._waiting.append(line)
    def get(self):
        line = self._waiting[0]
        del self._waiting[0]
        return line

class Output:
    def println(self,text):
        pass

class UserOutput(Output):
    def println(self,text):
        print(text)

class FakeOutput(Output):
    _waiting = None
    def __init__(self):
        super().__init__()
        self._waiting = ''
    def println(self,text):
        self._waiting+= text+'\n'
    def get(self):
        return self._waiting

class CalculationController:
    calculatorModel = None
    def __init__(self):
        super().__init__()
        self.calculatorModel = calc.ReversePolishNotatioParser()
    def actionCalculate(self,query):
        expression = self.calculatorModel.parse(query)
        if expression.wellFormed():
            try:
                return str(expression.interpret())
            except Exception as e:
                return 'Error: '+str(e.__class__.__name__)
        else:
            return 'Error: Malformed expression'

def view(InputHandler:Input,OutputHandler:Output):
    calculator = CalculationController()
    while True:
        OutputHandler.println('Type an expression to be evaluated or "exit" to quit')
        query = InputHandler.get()
        if query == 'exit': break
        OutputHandler.println(calculator.actionCalculate(query))

if __name__ == '__main__' :
    view(UserInput(),UserOutput())
