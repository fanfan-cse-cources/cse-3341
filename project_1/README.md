# Readme

## List of Files

```
├── Core.py             Enum for keywords
├── README.txt
├── Test_Correct        Test cases, expected to running without errors
│   ├── ...
├── Test_Default        Test cases, expected to running without errors (From Piazza)
│   ├── ...
├── Test_Error          Test cases, expected to running with errors
│   ├── ...
├── Tokenizer.py        Preprocessor, Tokenizer for single word
└── main.py             Runner
```

## Run the program

```
$ python3 main.py <path_to_file>

```

## Design

- main.py: Entry point of the program, it will keep consuming tokens from source file until reaches the end of file.
- Tokenizer.py: Tokenizer will replace every symbol as token in words, then process it as token
- Core.py: Enum for keywords, corresponding with numbers

### Core.py

```
1: Core.PROGRAM
2: Core.BEGIN
3: Core.END
4: Core.INT
5: Core.IF
6: Core.THEN
7: Core.ELSE
8: Core.WHILE
9: Core.LOOP
10: Core.READ
11: Core.WRITE
12: Core.SEMICOLON
13: Core.COMMA
14: Core.ASSIGN
15: Core.NEGATION
16: Core.SLPAREN
17: Core.SRPAREN
18: Core.AND
19: Core.OR
20: Core.LPAREN
21: Core.RPAREN
22: Core.ADD
23: Core.SUB
24: Core.MULT
25: Core.NOTEQUAL
26: Core.EQUAL
27: Core.LESS
28: Core.GREATER
29: Core.LESSEQUAL
30: Core.GREATEREQUAL
31: Core.CONST
32: Core.ID
33: Core.EOF
```
