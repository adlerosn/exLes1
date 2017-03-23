def avg(lst:list):
    return sum(lst)/len(lst)

class Observable(object):
    def __init__(self):
        self.__observers = list()
        super().__init__()
        
    def registerObserver(self, observer):
        self.__observers.append(observer)
        
    def notifyObservers(self):
        [observer.notify(self) for observer in self.__observers]

class Observer(object):
    def __init__(self, observable):
        observable.registerObserver(self)
        super().__init__()
        
    def notify(self, observable):
        pass

class Sensor(Observable):
    _lastMeasurement = 0;
    
    def __init__(self):
        super().__init__()
        
    def setMock(self, ficticiousMeasure):
        self._lastMeasurement = ficticiousMeasure
        self.notifyObservers()
        
    def getMeasurement(self):
        return self._lastMeasurement

class TemperatureSensor(Sensor):
    def __init__(self):
        super().__init__()

class PeopleSensor(Sensor):
    def __init__(self):
        super().__init__()

class SensorReducer(Observer, Sensor):
    reduceFunction = None
    _observables = None
    _reduced = None
    
    def __init__(self, sensor, reduceableFunction):
        self._observables = dict()
        self.reduceFunction = reduceableFunction
        super().__init__(sensor)
        
    def addSensor(self, sensor):
        super().__init__(sensor)
        
    def notify(self, sensor):
        self._observables[id(sensor)] = sensor.getMeasurement()
        self._reduced = self.reduceFunction(list(self._observables.values()))
        self.notifyObservers()
        
    def getMeasurement(self):
        return self._reduced

class LastNotificationSensorObserver(Observer):
    _lastMeasurement = 0;
    def __init__(self, sensor):
        super().__init__(sensor)
    def notify(self, sensor):
        self._lastMeasurement = sensor.getMeasurement()
    def getMeasurement(self):
        return self._lastMeasurement

class nullObservable(Observable):
    pass

class Arcondicionado(Observer, Observable):
    temperaturaIdeal = 25
    grauPorPessoa = 1
    temperatura = None
    pessoas = None
    temperaturaParaRegulagemInterna = 25
    
    def __init__(self,sensoresTemperatura,sensoresPessoas):
        self.temperatura = SensorReducer(sensoresTemperatura[0],avg)
        for sensorTemperatura in sensoresTemperatura[1:]:
            self.temperatura.addSensor(sensorTemperatura)
        self.temperatura.registerObserver(self)
        
        self.pessoas = SensorReducer(sensoresPessoas[0],avg)
        for sensorPessoas in sensoresPessoas[1:]:
            self.pessoas.addSensor(sensorPessoas)
        self.pessoas.registerObserver(self)
        
        super().__init__(nullObservable())
        
    def notify(self, observable):
        temperaturaAtual = self.temperatura.getMeasurement()
        lotacaoAtual = self.pessoas.getMeasurement()
        try:
            self.temperaturaParaRegulagemInterna = (
                (
                    self.temperaturaIdeal
                    -
                    (
                        temperaturaAtual
                        +
                        (
                            lotacaoAtual
                            *
                            self.grauPorPessoa
                        )
                    )
                )
                +
                self.temperaturaIdeal
            )
            self.notifyObservers()
        except:
            pass
        
        return super().notify(observable)
        
    def getMeasurement(self):
        return self.temperaturaParaRegulagemInterna
