# Simple Compiler
This is a simple compiler for a programming language that supports various token types, including identifiers, keywords, integers, floating-point numbers, and symbols. The compiler performs tokenization (lexical analysis) of the source code and syntactic analysis according to a specific grammar.

## Tokenization
Tokenization is the process of breaking down the source code into individual tokens, where each token represents a meaningful unit of the code. The compiler uses Finite State Automata (FSAs) for each token type to recognize and classify tokens. The token types supported by this compiler are:

## Data Types:
1. **IDENTIFIER**: Represents user-defined identifiers.
1. **KEYWORD**: Represents keywords in the language.
1. **INTEGER**: Represents integer values.
1. **FLOAT**: Represents floating-point values.
1. **SYMBOL**: Represents symbols like operators and punctuation.

## Token Hierarchy: 
The compiler follows a token hierarchy to prioritize token recognition. If there are tokens that match the same patterns for keywords, identifiers, or numbers, the compiler prioritizes the matching based on this hierarchy. For example, if a token can be both an identifier and a keyword, it will be recognized as a keyword.

## Syntactic Analysis
After tokenization, the compiler performs syntactic analysis according to a specific grammar. The grammar rules are defined in the code as follows:

## CNF - Chomsky normal form of the grammar
```python
rules = {
    ("S", "y"),("G", "y"),("X", "y"),("I", "if"),("E", "else"),("O", "s"),("Z", "y"),
    ("S", "IA"),("S", "ZZ"),("Z", "IA"),("Z", "ZZ"),("A", "GZ"),("A", "GB"),("G", "XC"),("C", "OX"),("X", "XC"),("B", "ZF"),("F", "EZ"),
}
```
The grammar includes non-terminal symbols (S, G, X, I, E, O, Z, A, C, B, F) and terminal symbols (if, else, symbols), along with production rules. The goal is to check if the source code adheres to these production rules and has a valid syntax.

## How to Use:
To use this compiler, follow these steps:

1. Ensure you have Python installed on your system.
1. Copy and paste the provided code into a Python script (e.g., compiler.py).

## Run the script:

The script will tokenize the source code and then perform syntactic analysis. If there are any syntax errors, they will be displayed as error messages.

If there are no syntax errors, the script will display the token type and token value for each token in the source code.

## Assumptions made:

Not many assumptions are made. Have tried to handle all cases
- Real numbers do not include negative numbers (to handle operators)
- as many errors considered using brute-force
- Error printed as "Syntax Error: <message> "
