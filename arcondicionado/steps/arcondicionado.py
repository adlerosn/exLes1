from behave import *

import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import refrigeracao

@given(u'sensor 1 marks 12')
def step_impl(context):
    context.s1 = refrigeracao.Sensor()
    context.s1.setMock(12)

@given(u'sensor 2 marks 14')
def step_impl(context):
    context.s2 = refrigeracao.Sensor()
    context.s2.setMock(14)

@given(u'sensor 3 marks 16')
def step_impl(context):
    context.s3 = refrigeracao.Sensor()
    context.s3.setMock(16)

@then(u'sensors\' final value should be 14')
def step_impl(context):
    sr = refrigeracao.SensorReducer(context.s1,refrigeracao.avg)
    sr.addSensor(context.s2)
    sr.addSensor(context.s3)
    
    context.s1.notifyObservers()
    context.s2.notifyObservers()
    context.s3.notifyObservers()    
    
    assert sr.getMeasurement() == 14

@given(u'external temperature is 20')
def step_impl(context):
    context.ts = refrigeracao.TemperatureSensor()
    context.ts.setMock(20)

@given(u'there are 8 people in room')
def step_impl(context):
    context.ps = refrigeracao.PeopleSensor()
    context.ps.setMock(8)

@then(u'air conditioning system temperature should mark 22')
def step_impl(context):
    arcond = refrigeracao.Arcondicionado([context.ts],[context.ps])
    
    fakeListener = refrigeracao.LastNotificationSensorObserver(arcond)
    
    context.ps.notifyObservers()
    context.ts.notifyObservers()
    
    assert fakeListener.getMeasurement() == 22

@given(u'external temperature is 18')
def step_impl(context):
    context.ts = refrigeracao.TemperatureSensor()
    context.ts.setMock(18)

@given(u'there are 10 people in room')
def step_impl(context):
    context.ps = refrigeracao.PeopleSensor()
    context.ps.setMock(10)
