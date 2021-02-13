from Tokenizer import Tokenizer
from Core import Core
import sys


def main():
  # initialize the scanner with the input file
  S = Tokenizer(sys.argv[1])

  # print the token stream
  while (S.getToken() != Core.EOF):
    # print the current token, with any extra data needed
    print(S.getToken().value, end=' ')
    # debug(S)
    # advance to the next token
    S.skipToken();
  print(Core.EOF.value)


def debug(S):
    # print token name and value for token ID/CONST
    print(S.getToken().name, end=' ')
    if (S.getToken() == Core.ID):
      value = S.idName()
      print("[" + value + "]", end='');
    elif (S.getToken() == Core.CONST):
      value = S.intVal()
      print("[" + str(value) + "]", end='');
    print();


if __name__ == "__main__":
    main()
