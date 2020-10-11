from Parser import Parser
from Scanner import Scanner
from Core import Core
import sys

def main():
  # Initialize the scanner with the input file
  S = Scanner(sys.argv[1])
  p = Parser(S)
  p.parse()
  p.semantic()
  p.print()


if __name__ == "__main__":
    main()