Feature: ar condicionado

Scenario Outline: média dos sensores
Given sensor 1 marks <s1>
And sensor 2 marks <s2>
And sensor 3 marks <s3>
Then sensors' final value should be <sf>

Examples:
| s1 | s2 | s3 | sf |
| 12 | 14 | 16 | 14 |

Scenario Outline: temperatura do ar
Given external temperature is <et>
And there are <ppl> people in room
Then air conditioning system temperature should mark <tsm>

Examples:
| et | ppl | tsm |
| 20 |   8 |  22 |
| 18 |  10 |  22 |
