Feature: GPS louco

Scenario Outline: Usando essa joça que não faz sentido
Given there is a database with cities
And the database knows that "Cariacica" is in <-20.3072429,-40.5397882>
And the database knows that "Vitoria" is in <-20.2821881,-40.3211898>
And the database knows that "Serra" is in <-20.1625771,-40.3315196>
And the database knows that "Colatina" is in <-19.516744,-40.687371>
And the database knows that "Pedro Canário" is in <-18.2963839,-39.9592541>
And I have a FoobarCar
When the car knows I'm in "<currentPlace>"
And I search "<query>"
Then I get "<outputPlace>"

Examples:
| currentPlace | query | outputPlace |
| Cariacica | Vitoria, Serra, Colatina e Pedro Canário norte | Pedro Canário |
| Cariacica | Vitoria, Serra, Colatina e Pedro Canário sul | Cariacica |
| Cariacica | Vitoria, Serra, Colatina e Pedro Canário oeste | Colatina |
| Cariacica | Vitoria, Serra, Colatina e Pedro Canário leste | Pedro Canário |

Scenario: Não usando essa joça que não faz sentido
Given there is a database with cities
And I have a FoobarCar
When I search "pipoca"
Then I get nothing
