
# Automatic detection of push-down field refactoring in Java programs with ANTLR4
<a href="https://refactoring.guru/push-down-field">Push down field</a> in one of the refactorings related to inheritance that is mentioned by Martin Fowler, in his book, <i>Refactoring: Improving the Design of Existing Code</i>. it is applied when a field was planned to be used in a class and his children, but in reality, only some of its subclasses used it. to refactor, it is better to move the unused field in parent class to its subclasses that use it.
This tool is developed to automatically determine possible opportunities of this refactoring in java projects.

## Dependancies
- python 3.8
- ANTLR4

## Run
Use the following command to run the tool on your java project:
`python3 main.py --path='PATH-TO-YOUR-JAVA-PROJECT'`

