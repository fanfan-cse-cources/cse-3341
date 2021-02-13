from enum import Enum

Core = Enum('Core',
  'PROGRAM,\
  BEGIN,\
  END,\
  INT,\
  IF,\
  THEN,\
  ELSE,\
  WHILE,\
  LOOP,\
  READ,\
  WRITE,\
  SEMICOLON,\
  COMMA,\
  ASSIGN,\
  NEGATION,\
  SLPAREN,\
  SRPAREN,\
  AND,\
  OR,\
  LPAREN,\
  RPAREN,\
  ADD,\
  SUB,\
  MULT,\
  NOTEQUAL,\
  EQUAL,\
  LESS,\
  GREATER,\
  LESSEQUAL,\
  GREATEREQUAL,\
  CONST,\
  ID,\
  EOF'
)
