Feature: Calculator with Reverse Polish Notation

Scenario Outline: Using the calculator via code
Given I have a calculator
And I evaluate "<expression>"
Then I expect seeing <result>

Examples:
| expression  | result   |
| 0           | 0        |
| 1 1 +       | 2        |
| 1 1 -       | 0        |
| 1 1 *       | 1        |
| 1 1 /       | 1        |
| 1 1 +       | 2        |
| 1 1 1 + +   | 3        |
| 1 1 + 1 +   | 3        |
|             | an error |
| 1 +         | an error |
| 1 1 + 1 + * | an error |
| + 1         | 1        |
| 0.  1 +     | 1.0      |
| 0.1 1 +     | 1.1      |
|  .1 1 +     | 1.1      |

Scenario: Using the calculator via CLI
Given I am using the CLI
When I entered "" on the CLI
And I entered "1 1 +" on the CLI
And I entered "1 1 + *" on the CLI
And I entered "1 0 /" on the CLI
And I entered "exit" on the CLI
And I let it run
Then I expect reading 'Type an expression to be evaluated or "exit" to quit'
And I expect reading "Error: Malformed expression"
And I expect reading 'Type an expression to be evaluated or "exit" to quit'
And I expect reading "2.0"
And I expect reading 'Type an expression to be evaluated or "exit" to quit'
And I expect reading "Error: Malformed expression"
And I expect reading 'Type an expression to be evaluated or "exit" to quit'
And I expect reading "Error: ZeroDivisionError"
And I expect reading 'Type an expression to be evaluated or "exit" to quit'
And I expect reading no more line
