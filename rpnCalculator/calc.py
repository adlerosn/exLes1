import re

def isFloat(val):
    try:
        float(val)
        return True
    except:
        return False

class Expression:
    def interpret(self):
        return None
    def tokensConsumed(self):
        return 1
    def wellFormed(self):
        return True

class MalformedExpression(Expression):
    def interpret(self):
        raise RuntimeError('Malformed expression got interpreted')
    def tokensConsumed(self):
        return 0
    def wellFormed(self):
        return False

class BiOperandExpression(Expression):
    le = None
    re = None
    def __init__(self,lft,rgt):
        super().__init__()
        self.le = lft
        self.re = rgt
    def tokensConsumed(self):
        return 1+self.le.tokensConsumed()+self.re.tokensConsumed()
    def wellFormed(self):
        return self.le.wellFormed() and self.re.wellFormed()

class PlusExpression(BiOperandExpression):
    def interpret(self):
        return self.le.interpret() + self.re.interpret()

class MinusExpression(BiOperandExpression):
    def interpret(self):
        return self.le.interpret() - self.re.interpret()

class TimesExpression(BiOperandExpression):
    def interpret(self):
        return self.le.interpret() * self.re.interpret()

class DivExpression(BiOperandExpression):
    def interpret(self):
        return self.le.interpret() / self.re.interpret()

class ValueExpression(Expression):
    val = None
    def __init__(self,val):
        super().__init__()
        self.val = float(val)
    def interpret(self):
        return self.val

class TransformChain:
    def __init__(self,nextTransformer = None):
        super().__init__()
        self.nextTransformer = nextTransformer
    nextTransformer = None
    def process(self,element):
        if self._handles(element):
            return self._handle(element)
        elif not self.nextTransformer is None:
            return self.nextTransformer.process(element)
        else:
            return element
    def _handles(self,element):
        return False
    def _handle(self,element):
        return element

class ValueTransformer(TransformChain):
    def _handles(self,element):
        return isFloat(element)
    def _handle(self,element):
        return ValueExpression(element)

class PlusTransformer(TransformChain):
    def _handles(self,element):
        return element == '+'
    def _handle(self,element):
        return PlusExpression

class MinusTransformer(TransformChain):
    def _handles(self,element):
        return element == '-'
    def _handle(self,element):
        return MinusExpression

class TimesTransformer(TransformChain):
    def _handles(self,element):
        return element == '*'
    def _handle(self,element):
        return TimesExpression

class DivTransformer(TransformChain):
    def _handles(self,element):
        return element == '/'
    def _handle(self,element):
        return DivExpression

class ReversePolishNotatioParser:
    _transformerChain = None

    def __init__(self):
        super().__init__()
        self.__init_tranform_chain()

    def __init_tranform_chain(self):
        self._transformerChain = (
            ValueTransformer(
                PlusTransformer(
                    MinusTransformer(
                        TimesTransformer(
                            DivTransformer(
                                None
                            )
                        )
                    )
                )
            )
        )

    def _tokenize(self,query):
        return re.findall(r'(\d+\.\d+|\.\d+|\d+|\+|\-|\*|\/)',query)

    def parse(self, query:str):
        tokens = [
            self._transformerChain.process(token)
            for token in self._tokenize(query)
        ]
        try:
            return self._buildExpression(list(reversed(tokens)))
        except:
            return MalformedExpression()

    def _buildExpression(self,tokens):
        if len(tokens)>=1:
            if isinstance(tokens[0],Expression):
                return tokens[0]
            elif len(tokens)>1:
                rgt = self._buildExpression(tokens[1:])
                lft = self._buildExpression(tokens[1+rgt.tokensConsumed():])
                if (
                    isinstance(rgt,MalformedExpression)
                    or
                    isinstance(lft,MalformedExpression)
                ):
                    return MalformedExpression()
                return tokens[0](lft,rgt)
        return MalformedExpression()
