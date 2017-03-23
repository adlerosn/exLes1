import behave

import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import navegacao

@behave.given('there is a database with cities')
def step_impl(context):
    context.cities = None

@behave.given('the database knows that "{city}" is in <{lat},{long}>')
def step_impl(context,city,lat,long):
    context.cities = navegacao.City(float(lat),float(long),city,context.cities)

@behave.given(u'I have a FoobarCar')
def step_impl(context):
    context.foobarcar = navegacao.FoobarCarSystem(context.cities)

@behave.when(u'the car knows I\'m in "{city}"')
def step_impl(context,city):
    context.foobarcar.updateCurrentLocation(context.cities.match(city))

@behave.when(u'I search "{query}"')
def step_impl(context,query):
    context.city = context.foobarcar.search(query)

@behave.then(u'I get "{city}"')
def step_impl(context,city):
    assert context.city.getName() == city

@behave.then(u'I get nothing')
def step_impl(context):
    assert context.city is None
