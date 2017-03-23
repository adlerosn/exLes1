import behave

import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import imposto

@behave.given('I make ${income} monthly')
def step_impl(context, income:float):
    context.tx = imposto.TaxCalculator(income)

@behave.then('I pay ${tax} on taxes')
def step_impl(context, tax:float):
    assert context.tx.calculateTax() == float(tax)
