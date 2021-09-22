#!/usr/bin/env python3
from Tokenizer import Tokenizer
from Core import Core
import sys

class Interpreter:
    # define tokenizer when initalized
    def __init__(self, t):
        self.tokenizer = t

    # parse program recursively
    def parse(self):
        self.valueDict = {}
        self.program = Program()
        self.program.parse(self)

    # check validation
    def validate(self):
        self.validateValueDict = {}
        self.program.validate(self)

    # print program recursively
    def print(self):
        self.program.print()

    # execute program recursively
    def execute(self):
        self.program.execute(self)

    def assignValue(self, x, value):
        if x in self.valueDict:
            self.valueDict[x] = value
        else:
            print("ERROR: Identifier " + x + " does not exist.")
            sys.exit()

    #helper method for handling error messages, used by the parse methods
    def expectSingle(self, expected):
        if self.tokenizer.getToken() != expected:
            print("ERROR: Expecting " + expected.name + ", received " + self.tokenizer.getToken().name + ".")
            sys.exit()

class Program:

    def parse(self, parser):
        parser.expectSingle(Core.PROGRAM)
        parser.tokenizer.skipToken()

        self.ds = DeclSeq()
        self.ds.parse(parser)

        parser.expectSingle(Core.BEGIN)
        parser.tokenizer.skipToken()

        self.ss = StmtSeq()
        self.ss.parse(parser)

        parser.expectSingle(Core.END)
        parser.tokenizer.skipToken()
        parser.expectSingle(Core.EOF)

    def validate(self, parser):
        self.ds.validate(parser)
        self.ss.validate(parser)

    def execute(self, parser):
        # print("DEBUG: Program executed")
        self.ds.execute(parser)
        self.ss.execute(parser)

    def print(self):
        print("program")
        self.ds.print(1)
        print("begin")
        self.ss.print(1)
        print("end")

class DeclSeq:

    def parse(self, parser):
        self.decl = Decl()
        self.decl.parse(parser)
        if not parser.tokenizer.getToken() == Core.BEGIN:
            self.ds = DeclSeq()
            self.ds.parse(parser)

    def validate(self, parser):
        self.decl.validate(parser)
        if hasattr(self, "ds"):
            self.ds.validate(parser)

    def execute(self, parser):
        # print("DEBUG: DeclSeq executed")
        self.decl.execute(parser)
        if hasattr(self, "ds"):
            self.ds.execute(parser)

    def print(self, indent):
        self.decl.print(indent)
        if hasattr(self, "ds"):
            self.ds.print(indent)

class StmtSeq:

    # differentiate statements and create attribute for each cases
    def parse(self, parser):
        if parser.tokenizer.getToken() == Core.ID:
            self.stmt = Assign()
        elif parser.tokenizer.getToken() == Core.READ:
            self.stmt = Input()
        elif parser.tokenizer.getToken() == Core.WRITE:
            self.stmt = Output()
        elif parser.tokenizer.getToken() == Core.IF:
            self.stmt = If()
        elif parser.tokenizer.getToken() == Core.REPEAT:
            self.stmt = Repeat()
        elif parser.tokenizer.getToken() == Core.WHILE:
            self.stmt = Loop()
        else:
            print("ERROR: Expecting ID, READ, WRITE, IF, WHILE, received " + parser.tokenizer.getToken().name + ".\n")
            sys.exit()
        # parse statement
        self.stmt.parse(parser)
        if (not parser.tokenizer.getToken() == Core.END
            and not parser.tokenizer.getToken() == Core.ELSE
            and not parser.tokenizer.getToken() == Core.UNTIL):
            self.ss = StmtSeq()
            self.ss.parse(parser)

    def validate(self, parser):
        self.stmt.validate(parser)
        if hasattr(self, "ss"):
            self.ss.validate(parser)

    def execute(self, parser):
        # print("DEBUG: Stmt executed")
        self.stmt.execute(parser)
        if hasattr(self, "ss"):
            # print("DEBUG: StmtSeq executed")
            self.ss.execute(parser)

    def print(self, indent):
        self.stmt.print(indent)
        if hasattr(self, "ss"):
            self.ss.print(indent)

class Decl:

    def parse(self, parser):
        parser.expectSingle(Core.INT)
        parser.tokenizer.skipToken()

        self.list = IdList()
        self.list.parse(parser)

        parser.expectSingle(Core.SEMICOLON)
        parser.tokenizer.skipToken()

    def validate(self, parser):
        self.list.validate(parser)

    def execute(self, parser):
        # print("DEBUG: Decl executed")
        self.list.execute(parser)

    def print(self, indent):
        for x in range(indent):
            print("  ", end="")
        print("int ", end="")
        self.list.print()
        print(";")

class IdList:

    def parse(self, parser):
        self.id = Id()
        self.id.parse(parser)

        # processing comma
        if parser.tokenizer.getToken() == Core.COMMA:
            parser.tokenizer.skipToken()
            self.list = IdList()
            self.list.parse(parser)

    def validate(self, parser):
        self.id.doubleDecleared(parser)
        if hasattr(self, "list"):
            self.list.validate(parser)

    def execute(self, parser):
        self.id.executeDecl(parser)
        if hasattr(self, "list"):
            self.list.execute(parser)

    def executeInput(self, parser):
        self.id.setValue(parser)
        if hasattr(self, "list"):
            self.list.executeInput(parser)

    def executeOutput(self, parser):
        # print("DEBUG: executeOutput output")
        print(self.id.getValue(parser))
        if hasattr(self, "list"):
            self.list.executeOutput(parser)

    def print(self):
        self.id.print()
        if hasattr(self, "list"):
            print(",", end="")
            self.list.print()

class Id:

    def parse(self, parser):
        parser.expectSingle(Core.ID)
        self.identifier = parser.tokenizer.idName()
        parser.tokenizer.skipToken()

    def validate(self, parser):
        # check id is in valueDic or not
        parser.validateValueDict[self.identifier] = None

    def addToDict(self, parser):
        parser.valueDict[self.identifier] = None

    # check for doubly declared variables
    def doubleDecleared(self, parser):
        # print(self.identifier)
        # print(self.identifier in parser.valueDict)
        if self.identifier in parser.valueDict:
            print("ERROR: Doubly declared variable: " + self.identifier + ".\n")
            sys.exit()

    def executeDecl(self, parser):
        # print("DEBUG: Id-executeDecl executed")
        parser.valueDict[self.identifier] = None

    def setValue(self, parser):
        if self.identifier in parser.valueDict:
            # get value from stdin
            val = input("Value for {}: ".format(self.identifier))
            parser.valueDict[self.identifier] = int(val)
        else:
            print("ERROR: Identifier " + self.identifier + " does not exist.")
            sys.exit()

    def getValue(self, parser):
        if self.identifier in parser.valueDict:
            return parser.valueDict[self.identifier]
        else:
            print("ERROR: Identifier " + self.identifier + " does not exist.")
            sys.exit()

    def print(self):
        print(self.identifier, end="")

class Assign:

    def parse(self, parser):
        self.id = Id()
        self.id.parse(parser)

        parser.expectSingle(Core.ASSIGN)
        parser.tokenizer.skipToken()

        self.exp = Exp()
        self.exp.parse(parser)

        parser.expectSingle(Core.SEMICOLON)
        parser.tokenizer.skipToken()

    def validate(self, parser):
        if hasattr(self, 'exp'):
            self.exp.validate(parser)

    def execute(self, parser):
        # print("DEBUG: Assign executed")
        parser.assignValue(self.id.identifier, self.exp.execute(parser))

    def print(self, indent):
        for x in range(indent):
            print("  ", end="")
        self.id.print()
        print("=", end="")
        self.exp.print()
        print(";")

class Input:

    def parse(self, parser):
        parser.tokenizer.skipToken()

        self.list = IdList()
        self.list.parse(parser)

        parser.expectSingle(Core.SEMICOLON)
        parser.tokenizer.skipToken()

    def validate(self, parser):
        self.list.validate(parser)

    def execute(self, parser):
        self.list.executeInput(parser)

    def print(self, indent):
        for x in range(indent):
            print("  ", end="")
        print("read ", end="")
        self.list.print()
        print(";")

class Output:

    def parse(self, parser):
        parser.tokenizer.skipToken()

        self.list = IdList()
        self.list.parse(parser)

        parser.expectSingle(Core.SEMICOLON)
        parser.tokenizer.skipToken()

    def validate(self, parser):
        self.list.validate(parser)

    def execute(self, parser):
        # print("DEBUG: Output executed")
        self.list.executeOutput(parser)

    def print(self, indent):
        for x in range(indent):
            print("  ", end="")
        print("write ", end="")
        self.list.print()
        print(";")

class If:

    def parse(self, parser):
        parser.tokenizer.skipToken()
        self.cond = Cond()
        self.cond.parse(parser)

        parser.expectSingle(Core.THEN)
        parser.tokenizer.skipToken()

        self.ss1 = StmtSeq()
        self.ss1.parse(parser)
        if parser.tokenizer.getToken() == Core.ELSE:
            parser.tokenizer.skipToken()
            self.ss2 = StmtSeq()
            self.ss2.parse(parser)

        parser.expectSingle(Core.END)
        parser.tokenizer.skipToken()
        parser.expectSingle(Core.SEMICOLON)
        parser.tokenizer.skipToken()

    def validate(self, parser):
        self.cond.validate(parser)
        self.ss1.validate(parser)
        if hasattr(self, "ss2"):
            self.ss2.validate(parser)

    def execute(self, parser):
        # print("DEBUG: If executed")
        if self.cond.execute(parser):
            # print("DEBUG: If-ss1 executed")
            self.ss1.execute(parser)
        elif hasattr(self,"ss2"):
            # print("DEBUG: If-ss2 executed")
            self.ss2.execute(parser)

    def print(self, indent):
        for x in range(indent):
            print("  ", end="")
        print("if ", end="")
        self.cond.print()
        print(" then")
        self.ss1.print(indent + 1)
        if hasattr(self, "ss2"):
            for x in range(indent):
                print("  ", end="")
            print("else")
            self.ss2.print(indent + 1)
        for x in range(indent):
            print("  ", end="")
        print("end;")

class Repeat:

    def parse(self, parser):
        parser.expectSingle(Core.REPEAT)
        parser.tokenizer.skipToken()
        self.ss = StmtSeq()
        self.ss.parse(parser)

        parser.expectSingle(Core.UNTIL)
        parser.tokenizer.skipToken()

        self.cond = Cond()
        self.cond.parse(parser)

        parser.expectSingle(Core.SEMICOLON)
        parser.tokenizer.skipToken()

    def validate(self, parser):
        self.cond.validate(parser)
        self.ss.validate(parser)

    def execute(self, parser):
        self.ss.execute(parser)

        while self.cond.execute(parser) == False:
            self.ss.execute(parser)

    def print(self, indent):
        for x in range(indent):
            print("  ", end="")
        print("repeat ")
        self.ss.print(indent + 1)
        for x in range(indent):
            print("  ", end="")
        print("until ", end="")
        self.cond.print()
        print(";", end="")
        print()

class Loop:

    def parse(self, parser):
        parser.tokenizer.skipToken()
        self.cond = Cond()
        self.cond.parse(parser)

        parser.expectSingle(Core.LOOP)
        parser.tokenizer.skipToken()
        self.ss = StmtSeq()
        self.ss.parse(parser)

        parser.expectSingle(Core.END)
        parser.tokenizer.skipToken()
        parser.expectSingle(Core.SEMICOLON)
        parser.tokenizer.skipToken()

    def validate(self, parser):
        self.cond.validate(parser)
        self.ss.validate(parser)

    def execute(self, parser):
        # execute StmtSeq until it condition does not met
        while self.cond.execute(parser):
            self.ss.execute(parser)

    def print(self, indent):
        for x in range(indent):
            print("  ", end="")
        print("while ", end="")
        self.cond.print()
        print()
        self.ss.print(indent + 1)
        for x in range(indent):
            print("  ", end="")
        print("end;")

class Cond:

    def parse(self, parser):
        # parse for mutiple condition
        if parser.tokenizer.getToken() == Core.NEGATION:
            parser.tokenizer.skipToken()
            self.cond = Cond()
            self.cond.parse(parser)
        elif parser.tokenizer.getToken() == Core.SLPAREN:
            parser.tokenizer.skipToken()
            self.cond = Cond()
            self.cond.parse(parser)

            if parser.tokenizer.getToken() == Core.AND:
                parser.tokenizer.skipToken()
                self.land = "land"
                self.cond2 = Cond()
                self.cond2.parse(parser)
            elif parser.tokenizer.getToken() == Core.OR:
                parser.tokenizer.skipToken()
                self.lor = "lor"
                self.cond2 = Cond()
                self.cond2.parse(parser)
            parser.expectSingle(Core.SRPAREN)
            parser.tokenizer.skipToken()
        else:
            self.comp = Comp()
            self.comp.parse(parser)

    def validate(self, parser):
        # if there is another condition
        if hasattr(self, "cond2"):
            self.cond2.validate(parser)
        if not hasattr(self, "comp"):
            self.cond.validate(parser)
        else:
            self.comp.validate(parser)

    def execute(self, parser):
        # execute cond2 if exist
        if hasattr(self, "cond2"):
            # print("DEBUG: Cond2 executed")
            # compare between two condition then return
            if hasattr(self, "land"):
                return self.cond.execute(parser) and self.cond2.execute(parser)
            elif hasattr(self, "lor"):
                return self.cond.execute(parser) or self.cond2.execute(parser)
        elif not hasattr(self, "comp"):
            # print("DEBUG: not Cond executed")
            # if there is no comp attribute, it will return opposite of cond
            return not self.cond.execute(parser)
        else:
            # otherwise return comp
            return self.comp.execute(parser)

    def print(self):
        if hasattr(self, "cond2"):
            print("[", end="")
            self.cond.print()
            if hasattr(self, "lor"):
                print(" or ", end="")
                self.cond2.print()
            elif hasattr(self, "land"):
                print(" && ", end="")
                self.cond2.print()
            print("]", end="")
        elif not hasattr(self, "comp"):
            print("!", end="")
            self.cond.print()
        else:
            self.comp.print()

class Comp:

    def parse(self, parser):
        if parser.tokenizer.getToken() == Core.LPAREN:
            parser.tokenizer.skipToken()

            self.operator = Operator()
            self.operator.parse(parser)

            self.compop = CompOP()
            self.compop.parse(parser)

            self.operator2 = Operator()
            self.operator2.parse(parser)

            parser.expectSingle(Core.RPAREN)
            parser.tokenizer.skipToken()
        else:
            print("ERROR: Expecting LPAREN, received " + parser.tokenizer.getToken().name + ".\n")
            sys.exit()


    def validate(self, parser):
        self.operator.validate(parser)
        self.compop.validate(parser)
        self.operator2.validate(parser)

    def execute(self, parser):
        # print("DEBUG: Comp executed")
        if self.compop.execute(parser) == Core.NOTEQUAL:
            return self.operator.execute(parser) != self.operator2.execute(parser)
        elif self.compop.execute(parser) == Core.EQUAL:
            # print("DEBUG: Comp-equal executed")
            return self.operator.execute(parser) == self.operator2.execute(parser)
        elif self.compop.execute(parser) == Core.LESS:
            return self.operator.execute(parser) < self.operator2.execute(parser)
        elif self.compop.execute(parser) == Core.GREATER:
            return self.operator.execute(parser) > self.operator2.execute(parser)
        elif self.compop.execute(parser) == Core.LESSEQUAL:
            return self.operator.execute(parser) <= self.operator2.execute(parser)
        elif self.compop.execute(parser) == Core.GREATEREQUAL:
            return self.operator.execute(parser) >= self.operator2.execute(parser)

    def print(self):
        print("(", end="")
        self.operator.print()
        self.compop.print()
        self.operator2.print()
        print(")", end="")

class Exp:

    def parse(self, parser):
        self.option = 0
        self.factor = Factor()
        self.factor.parse(parser)
        if parser.tokenizer.getToken() == Core.ADD:
            self.option = Core.ADD
        elif parser.tokenizer.getToken() == Core.SUB:
            self.option = Core.SUB
        if not self.option == 0:
            # parse expression when token there is not Core.ADD or Core.SUB
            parser.tokenizer.skipToken()
            self.exp = Exp()
            self.exp.parse(parser)

    def validate(self, parser):
        self.factor.validate(parser)
        if hasattr(self, "exp"):
            self.exp.validate(parser)

    def execute(self, parser):
        # calculate addition/minus
        if self.option == 0:
            return self.factor.execute(parser)
        if self.option == Core.ADD:
            return self.factor.execute(parser) + self.exp.execute(parser)
        if self.option == Core.SUB:
            return self.factor.execute(parser) - self.exp.execute(parser)

    def print(self):
        self.factor.print()
        if self.option == Core.ADD:
            print("+", end="")
            self.exp.print()
        elif self.option == Core.SUB:
            print("-", end="")
            self.exp.print()

class Factor:

    def parse(self, parser):
        self.operator = Operator()
        self.operator.parse(parser)
        if parser.tokenizer.getToken() == Core.MULT:
            parser.tokenizer.skipToken()
            self.factor = Factor()
            self.factor.parse(parser)

    def validate(self, parser):
        self.operator.validate(parser)
        if hasattr(self, "factor"):
            self.factor.validate(parser)

    def execute(self, parser):
        # calculate constant/muplication
        retVal = self.operator.execute(parser)
        if hasattr(self, "factor"):
            retVal *= self.factor.execute(parser)
        return retVal

    def print(self):
        self.operator.print()
        if hasattr(self, "factor"):
            print("*", end="")
            self.factor.print()

class Operator:

    def parse(self, parser):
        if parser.tokenizer.getToken() == Core.ID:
            self.id = Id()
            self.id.parse(parser)
        elif parser.tokenizer.getToken() == Core.CONST:
            self.constant = parser.tokenizer.intVal()
            parser.tokenizer.skipToken()
        elif parser.tokenizer.getToken() == Core.LPAREN:
            parser.tokenizer.skipToken()

            self.exp = Exp()
            self.exp.parse(parser)

            parser.expectSingle(Core.RPAREN)
            parser.tokenizer.skipToken()
        else:
            print("ERROR: Expecteing ID, CONST, or LPAREN, received " + parser.tokenizer.getToken().name + ".\n")
            sys.exit()

    def validate(self, parser):
        if hasattr(self, "id"):
            self.id.validate(parser)
        elif hasattr(self, "exp"):
            self.exp.validate(parser)

    def execute(self, parser):
        retVal = 0
        if hasattr(self, "id"):
            retVal = self.id.getValue(parser)
            if retVal == None:
                print("Error: Accessing uninitalized variabl " + self.id.identifier + ".")
                sys.exit()
        elif hasattr(self, "exp"):
            retVal = self.exp.execute(parser)
        else:
            retVal = self.constant
        return retVal

    def print(self):
        if hasattr(self, "id"):
            self.id.print()
        elif hasattr(self, "exp"):
            print("(", end="")
            self.exp.print()
            print(")", end="")
        else:
            print(self.constant, end="")

class CompOP:

    def parse(self, parser):
        # set attribute for CompOP token
        if parser.tokenizer.getToken() == Core.NOTEQUAL:
            self.notequal = Core.NOTEQUAL

            parser.tokenizer.skipToken()
        elif parser.tokenizer.getToken() == Core.EQUAL:
            self.equal = Core.EQUAL

            parser.tokenizer.skipToken()
        elif parser.tokenizer.getToken() == Core.LESS:
            self.less = Core.LESS

            parser.tokenizer.skipToken()
        elif parser.tokenizer.getToken() == Core.GREATER:
            self.greater = Core.GREATER

            parser.tokenizer.skipToken()
        elif parser.tokenizer.getToken() == Core.LESSEQUAL:
            self.lessequal = Core.LESSEQUAL

            parser.tokenizer.skipToken()
        elif parser.tokenizer.getToken() == Core.GREATEREQUAL:
            self.greaterequal = Core.GREATEREQUAL

            parser.tokenizer.skipToken()
        else:
            print("ERROR: Expecting NOTEQUAL, EQUAL, LESS, GREATER, LESSEQUAL, GREATEREQUAL, received " + parser.tokenizer.getToken().name + ".\n")
            sys.exit()

    def validate(self, parser):
        # it is not a valid CompOP token, if there is no attribute from the list
        compop = ["notequal", "equal", "less", "greater", "lessequal", "greaterequal"]
        flag = False
        for x in compop:
            if hasattr(self, x):
                flag = True
        if flag == False:
            print("ERROR: Expecting CompOP, received " + parser.tokenizer.getToken().name + ".\n")
            sys.exit()

    def execute(self, parser):
        # return a CompOP token to execute call
        token = None
        # print("DEBUG: CompOP executed")
        if hasattr(self, "notequal"):
            token = Core.NOTEQUAL
        elif hasattr(self, "equal"):
            # print("DEBUG: Comp-equal executed")
            token = Core.EQUAL
        elif hasattr(self, "less"):
            token = Core.LESS
        elif hasattr(self, "greater"):
            token = Core.GREATER
        elif hasattr(self, "lessequal"):
            token = Core.LESSEQUAL
        elif hasattr(self, "greaterequal"):
            token = Core.GREATEREQUAL
        return token

    def print(self):
        if hasattr(self, "notequal"):
            print("!=", end="")
        elif hasattr(self, "equal"):
            print("==", end="")
        elif hasattr(self, "less"):
            print("<", end="")
        elif hasattr(self, "greater"):
            print(">", end="")
        elif hasattr(self, "lessequal"):
            print("<=", end="")
        elif hasattr(self, "greaterequal"):
            print(">=", end="")
