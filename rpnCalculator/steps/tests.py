import behave

import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import calc
import calc_cli

@behave.given('I have a calculator')
def step_impl(context):
    context.calc = calc.ReversePolishNotatioParser()

@behave.given('I evaluate ""')
@behave.given('I evaluate "{query}"')
def step_impl(context, query=''):
    context.exp = context.calc.parse(query)

@behave.then('I expect seeing {result}')
def step_impl(context, result):
    if str(result)=='an error':
        assert not context.exp.wellFormed()
    else:
        assert context.exp.interpret() == float(result)

@behave.given('I am using the CLI')
def step_impl(context):
    context.i = calc_cli.FakeInput()
    context.o = calc_cli.FakeOutput()
    context.run = lambda: calc_cli.view(context.i,context.o)

@behave.when('I entered "" on the CLI')
@behave.when('I entered "{inp}" on the CLI')
def step_impl(context,inp=''):
    context.i.append(inp)

@behave.when('I let it run')
def step_impl(context):
    context.run()
    context.line = 0

@behave.then('I expect reading \'\'')
@behave.then('I expect reading ""')
@behave.then('I expect reading "{msg}"')
@behave.then('I expect reading \'{msg}\'')
def step_impl(context,msg=''):
    assert context.o.get().splitlines()[context.line] == msg
    context.line+=1

@behave.then('I expect reading no more line')
def step_impl(context):
    assert len(context.o.get().splitlines()) >= context.line
