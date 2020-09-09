from Core import Core
import re

class Scanner:
  # Constructor should open the file and find the first token
  def __init__(self, filename):

    # set current position, and end flag to 0
    self.pos = 0
    self.end = 0

    # read file
    with open(filename, "r" ) as f:
      content = f.read()
      rep = {
              ";": " semicolon ", 
              "(": " lparen ",
              ")": " rparen ",
              ",": " comma ",
              "==": " equal ",
              "<=": " lessequal ",
              "=": " assign ",
              "!": " negation ",
              "<": " less ",
              "+": " add ",
              "-": " sub ",
              "*": " mult "
            }
    
    # replace symbol as string, then create a list of all user inputs
    for item in rep:
      content = content.replace(item, rep[item])

    self.list = content.split()

    # create a list of keywords as lower case string
    self.keywords = []
    for item in Core:
      self.keywords.append(item.name.lower())

  # nextToken should advance the scanner to the next token
  def nextToken(self):
    self.pos += 1

    return 0

  # currentToken should return the current token
  def currentToken(self):
    val = -1

    # when the reach the keyword of end
    if self.pos < len(self.list) and self.list[self.pos] == "end":
      self.end = 1
      val = Core["END"]
    # check current string in the list is a keyword or not
    elif self.pos < len(self.list) and self.list[self.pos] in self.keywords and self.end == 0:
      val = Core[self.list[self.pos].upper()]
    # check current string in the list is a number or not
    elif self.pos < len(self.list) and self.list[self.pos].isnumeric():
      # check the number is larger than 1023 or not
      if int(self.list[self.pos]) < 1024:
        val = Core["CONST"]
      else:
        val = Core["EOF"]
        print("Error: Invalid Input")
    # check current string in the list is an ID or not
    elif self.pos < len(self.list) and re.match("[a-zA-Z]+\d*[a-zA-Z]*\d*", self.list[self.pos]) and self.end == 0:
      val = Core["ID"]
    # check current string in the list combined the number and words,
    # if yes, separate them
    elif self.pos < len(self.list) and re.match("([0-9]+)(\w+)", self.list[self.pos]) and self.end == 0:
      val = Core["CONST"]

      temp = re.compile("([0-9]+)(\w+)")
      res = temp.match(self.list[self.pos]).groups() 

      self.list.remove(self.pos)
      self.list[self.pos + 1: self.pos + 1] = res
    # if there is nothing to match and reach the end of the list
    elif val == -1 and self.pos == len(self.list):
      val = Core["EOF"]
    # otherwise throw expection
    else:
      val = Core["EOF"]
      print("Error: Invalid Input")
      
    return val

  # If the current token is ID, return the string value of the identifier
	# Otherwise, return value does not matter
  def getID(self):
    return self.list[self.pos]

  # If the current token is CONST, return the numerical value of the constant
	# Otherwise, return value does not matter
  def getCONST(self):
    return int(self.list[self.pos])