Feature: income tax calculator

Scenario Outline: calculating taxes to be paid
Given I make $<income> monthly
Then I pay $<tax> on taxes

Examples:
| income | tax  |
| 1500   | 0    |
| 2000   | 150  |
| 3000   | 450  |
| 4000   | 900  |
| 5000   | 1375 |
