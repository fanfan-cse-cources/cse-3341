#!/usr/bin/env python3
from Interpreter import Interpreter
from Tokenizer import Tokenizer
from Core import Core
import sys

def main():
  # Initialize the tokenizer with the input file
  tokenizer = Tokenizer(sys.argv[1])
  interpreter = Interpreter(tokenizer)
  interpreter.parse()
  interpreter.validate()
  # interpreter.print()
  interpreter.execute()


if __name__ == "__main__":
    main()
