from Core import Core
import re

class Tokenizer:
  # Constructor should open the file and find the first token
  def __init__(self, filename):
    # set current position, and end flag to 0
    self.pos = 0

    # read file
    with open(filename, "r" ) as f:
      content = f.read()
      # lookup table for symbols
      rep = {
              "!=": " notequal ",
              "==": " equal ",
              "<=": " lessequal ",
              ">=": " greaterequal ",
              "&&": " and ",
              "||": " or ",
              ";": " semicolon ",
              ",": " comma ",
              "=": " assign ",
              "!": " negation ",
              "[": " slparen ",
              "]": " srparen ",
              "(": " lparen ",
              ")": " rparen ",
              "+": " add ",
              "-": " sub ",
              "*": " mult ",
              "<": " less ",
              ">": " greater ",
            }

    # replace symbol as string, then create a list of all user inputs
    for item in rep:
      content = content.replace(item, rep[item])

    self.list = content.split()

    # create a list of keywords as lower case string
    self.keywords = []
    for item in Core:
      self.keywords.append(item.name.lower())


  # skipToken should advance the scanner to the next token
  def skipToken(self):
    self.pos += 1

    return 0


  # getToken should return the current token
  def getToken(self):
    ls = self.list
    currentPos = self.pos
    val = -1

    # check current string in the list is a keyword or not
    if currentPos < len(ls) and ls[currentPos] in self.keywords:
      val = Core[ls[currentPos].upper()]
    # check current string in the list is a number or not
    elif currentPos < len(ls) and ls[currentPos].isnumeric():
      # check pervious token is INT or not,
      # it is illegal to define a CONST as id
      if Core[(ls[currentPos - 1]).upper()] == Core.INT:
        val = Core["EOF"]
        print("Error: Invalid Input, illegal ID name")
      # check the number is larger than 8 digit or not
      elif int(ls[currentPos]) < 99999999:
        val = Core["CONST"]
      else:
        val = Core["EOF"]
        print("Error: Invalid Input, INT value cannot exceed 99999999")
    # check current string in the list is an ID or not
    elif currentPos < len(ls):
      if len(ls[currentPos]) <= 8:

        # if there is a match with regular expression
        match = ''
        if re.match("[A-Z]+[\d]*", ls[currentPos]):
          match = re.match("[A-Z]+[\d]*", ls[currentPos])[0]

        # test the match is fully comply with our expression
        if match == ls[currentPos]:
          val = Core["ID"]
        else:
          val = Core["EOF"]
          print("Error: Invalid Input, illegal ID name")
      else:
        val = Core["EOF"]
        print("Error: Invalid Input, ID name cannot exceed 8 characters")
    # if there is nothing to match and reach the end of the list
    elif val == -1 and currentPos == len(ls):
      val = Core["EOF"]
    # otherwise throw expection
    else:
      val = Core["EOF"]
      print("Error: Invalid Input")

    return val


  # if the current token is ID, return the string value of the identifier
	# otherwise, return value does not matter
  def idName(self):
    return self.list[self.pos]


  # if the current token is CONST, return the numerical value of the constant
	# otherwise, return value does not matter
  def intVal(self):
    return int(self.list[self.pos])
