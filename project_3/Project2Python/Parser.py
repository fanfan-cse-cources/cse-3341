from Scanner import Scanner
from Core import Core
import sys

# Parser class contains all the persistent data structures we will need, and some helper functions
class Parser:
	#scanner is stored here so it is avaiable to the parse method of all contained classes
	#program is the root of the parse tree
	#scopes is a data structure for the semantic checks performed after parsing
	
	#Constructor for Parser. Initializes the scanner.
	def __init__(self, s):
		self.scanner = s
	
	#parse starts the recursive desccent parser
	def parse(self):
		self.program = Program()
		self.program.parse(self)
	
	#semantic should be called after parsing to perform semantic checks on the parse tree
	#this is what find doubly-declared variables and variables not in scope
	def semantic(self):
		self.scopes = [[]]
		self.program.semantic(self)
	
	#print will walk over the tree and print the program
	def print(self):
		self.program.print()
	
	#helper method for the semantic checks
	#returns true if the string x is the name of a variable that is in scope
	def nestedScopeCheck(self, x):
		match = False
		if not len(self.scopes) == 0:
			temp = self.scopes.pop()
			match = x in temp
			if not match:
				match = self.nestedScopeCheck(x)
			self.scopes.append(temp)
		return match
	
	#helper method for the semantic checks
	#returns true if the string x is the name of a variable that was declared in the current scope
	def currentScopeCheck(self, x):
		match = False
		if not len(self.scopes) ==0:
			match = x in self.scopes[-1]
		return match
	
	#helper method for handling error messages, used by the parse methods
	def expectedToken(self, expected):
		if self.scanner.currentToken() != expected:
			print("ERROR: Expected " + expected.name + ", recieved " + self.scanner.currentToken().name + "\n", end='')
			sys.exit()
	
#
# This is where the non-terminal classes being
# Each non-terminal of the grammar has a class except for <stmt>
# Each class has a parse, a semantic, and a print method
#
	
class Program:
	
	def parse(self, parser):
		parser.expectedToken(Core.PROGRAM)
		parser.scanner.nextToken()
		self.ds = DeclSeq()
		self.ds.parse(parser)
		parser.expectedToken(Core.BEGIN)
		parser.scanner.nextToken()
		self.ss = StmtSeq()
		self.ss.parse(parser)
		parser.expectedToken(Core.END)
		parser.scanner.nextToken()
		parser.expectedToken(Core.EOF)
	
	def semantic(self, parser):
		parser.scopes.append([])
		self.ds.semantic(parser)
		parser.scopes.append([])
		self.ss.semantic(parser)
		parser.scopes.pop()
	
	def print(self):
		print("program\n", end='')
		self.ds.print(1)
		print("begin\n", end='')
		self.ss.print(1)
		print("end\n", end='')

class DeclSeq:
	
	def parse(self, parser):
		self.decl = Decl()
		self.decl.parse(parser)
		if not parser.scanner.currentToken() == Core.BEGIN:
			self.ds = DeclSeq()
			self.ds.parse(parser)
	
	def semantic(self, parser):
		self.decl.semantic(parser)
		if hasattr(self, 'ds'):
			self.ds.semantic(parser)
	
	def print(self, indent):
		self.decl.print(indent)
		if hasattr(self, 'ds'):
			self.ds.print(indent)

class StmtSeq:

	def parse(self, parser):
		if parser.scanner.currentToken() == Core.ID:
			self.stmt = Assign()
		elif parser.scanner.currentToken() == Core.INPUT:
			self.stmt = Input()
		elif parser.scanner.currentToken() == Core.OUTPUT:
			self.stmt = Output()
		elif parser.scanner.currentToken() == Core.IF:
			self.stmt = If()
		elif parser.scanner.currentToken() == Core.WHILE:
			self.stmt = Loop()
		elif parser.scanner.currentToken() == Core.INT:
			self.stmt = Decl()
		else:
			print("ERROR: Bad start to statement: " + parser.scanner.currentToken().name + "\n", end='')
			System.exit(0)
		self.stmt.parse(parser)
		if (not parser.scanner.currentToken() == Core.END
			and not parser.scanner.currentToken() == Core.ENDIF
			and not parser.scanner.currentToken() == Core.ENDWHILE
			and not parser.scanner.currentToken() == Core.ELSE):
			self.ss = StmtSeq()
			self.ss.parse(parser)
	
	def semantic(self, parser):
		self.stmt.semantic(parser)
		if hasattr(self, 'ss'):
			self.ss.semantic(parser)
	
	def print(self, indent):
		self.stmt.print(indent)
		if hasattr(self, 'ss'):
			self.ss.print(indent)

class Decl:
	
	def parse(self, parser):
		parser.expectedToken(Core.INT)
		parser.scanner.nextToken()
		self.list = IdList()
		self.list.parse(parser)
		parser.expectedToken(Core.SEMICOLON)
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		self.list.semantic(parser)
	
	def print(self, indent):
		for x in range(indent):
			print("  ", end='')
		print("int ", end='')
		self.list.print()
		print(";\n", end='')

class IdList:
	
	def parse(self, parser):
		self.id = Id()
		self.id.parse(parser)
		if parser.scanner.currentToken() == Core.COMMA:
			parser.scanner.nextToken()
			self.list = IdList()
			self.list.parse(parser)
	
	def semantic(self, parser):
		self.id.doublyDeclared(parser)
		self.id.addToScope(parser)
		if hasattr(self, 'list'):
			self.list.semantic(parser)
	
	def print(self):
		self.id.print()
		if hasattr(self, 'list'):
			print(",", end='')
			self.list.print()

class Id:
	
	def parse(self, parser):
		parser.expectedToken(Core.ID)
		self.identifier = parser.scanner.getID()
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		if not parser.nestedScopeCheck(self.identifier):
			print("ERROR: No matching declaration found: " + self.identifier + "\n", end='')
			sys.exit()
	
	#Called by Decl.semantic to add the variable to the scopes data structure
	def addToScope(self, parser):
		parser.scopes[-1].append(self.identifier)
	
	#Called by Decl.semantic to check for doubly declared variables
	def doublyDeclared(self, parser):
		if parser.currentScopeCheck(self.identifier):
			print("ERROR: Doubly declared variable detected: " + self.identifier + "\n", end='')
			sys.exit()
	
	def print(self):
		print(self.identifier, end='')

class Assign:
	
	def parse(self, parser):
		self.id = Id()
		self.id.parse(parser)
		parser.expectedToken(Core.ASSIGN)
		parser.scanner.nextToken()
		self.expr = Expr()
		self.expr.parse(parser)
		parser.expectedToken(Core.SEMICOLON)
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		self.id.semantic(parser)
		self.expr.semantic(parser)
	
	def print(self, indent):
		for x in range(indent):
			print("  ", end='')
		self.id.print()
		print("=", end='')
		self.expr.print()
		print(";\n", end='')

class Input:
	
	def parse(self, parser):
		parser.scanner.nextToken()
		self.id = Id()
		self.id.parse(parser)
		parser.expectedToken(Core.SEMICOLON)
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		self.id.semantic(parser)
	
	def print(self, indent):
		for x in range(indent):
			print("  ", end='')
		print("input ", end='')
		self.id.print()
		print(";\n", end='')

class Output:
	
	def parse(self, parser):
		parser.scanner.nextToken()
		self.expr = Expr()
		self.expr.parse(parser)
		parser.expectedToken(Core.SEMICOLON)
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		self.expr.semantic(parser)
	
	def print(self, indent):
		for x in range(indent):
			print("  ", end='')
		print("output ", end='')
		self.expr.print()
		print(";\n", end='')

class If:
	
	def parse(self, parser):
		parser.scanner.nextToken()
		self.cond = Cond()
		self.cond.parse(parser)
		parser.expectedToken(Core.THEN)
		parser.scanner.nextToken()
		self.ss1 = StmtSeq()
		self.ss1.parse(parser)
		if parser.scanner.currentToken() == Core.ELSE:
			parser.scanner.nextToken()
			self.ss2 = StmtSeq()
			self.ss2.parse(parser)
		parser.expectedToken(Core.ENDIF)
		parser.scanner.nextToken()
		parser.expectedToken(Core.SEMICOLON)
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		self.cond.semantic(parser)
		parser.scopes.append([])
		self.ss1.semantic(parser)
		parser.scopes.pop()
		if hasattr(self, 'ss2'):
			parser.scopes.append([])
			self.ss2.semantic(parser)
			parser.scopes.pop()
	
	def print(self, indent):
		for x in range(indent):
			print("  ", end='')
		print("if ", end='')
		self.cond.print()
		print(" then\n", end='')
		self.ss1.print(indent+1)
		if hasattr(self, 'ss2'):
			for x in range(indent):
				print("  ", end='')
			print("else\n", end='')
			self.ss2.print(indent+1)
		for x in range(indent):
			print("  ", end='')
		print("endif;\n", end='')

class Loop:
	
	def parse(self, parser):
		parser.scanner.nextToken()
		self.cond = Cond()
		self.cond.parse(parser)
		parser.expectedToken(Core.BEGIN)
		parser.scanner.nextToken()
		self.ss = StmtSeq()
		self.ss.parse(parser)
		parser.expectedToken(Core.ENDWHILE)
		parser.scanner.nextToken()
		parser.expectedToken(Core.SEMICOLON)
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		self.cond.semantic(parser)
		parser.scopes.append([])
		self.ss.semantic(parser)
		parser.scopes.pop()
	
	def print(self, indent):
		for x in range(indent):
			print("  ", end='')
		print("while ", end='')
		self.cond.print()
		print(" begin\n", end='')
		self.ss.print(indent+1)
		for x in range(indent):
			print("  ", end='')
		print("endwhile;\n", end='')

class Cond:
	
	def parse(self, parser):
		if parser.scanner.currentToken() == Core.NEGATION:
			parser.scanner.nextToken()
			parser.expectedToken(Core.LPAREN)
			parser.scanner.nextToken()
			self.cond = Cond()
			self.cond.parse(parser)
			parser.expectedToken(Core.RPAREN)
			parser.scanner.nextToken()
		else:
			self.cmpr = Cmpr()
			self.cmpr.parse(parser)
			if parser.scanner.currentToken() == Core.OR:
				self.scanner.nextToken()
				self.cond = Cond()
				self.cond.parse(parser)
	
	def semantic(self, parser):
		if not hasattr(self, 'cmpr'):
			self.cond.semantic(parser)
		else:
			self.cmpr.semantic(parser)
			if hasattr(self, 'cond'):
				self.cond.semantic(parser)
	
	def print(self):
		if not hasattr(self, 'cmpr'):
			print("!(", end='')
			self.cond.print()
			print(")", end='')
		else:
			self.cmpr.print()
			if hasattr(self, 'cond'):
				print(" or ", end='')
				self.cond.print()

class Cmpr:
	
	def parse(self, parser):
		self.expr1 = Expr()
		self.expr1.parse(parser)
		if parser.scanner.currentToken() == Core.EQUAL:
			self.option = 0
		elif parser.scanner.currentToken() == Core.LESS:
			self.option = 1
		elif parser.scanner.currentToken() == Core.LESSEQUAL:
			self.option = 2
		else:
			print("ERROR: Expected EQUAL, LESS, or LESSEQUAL, recieved " + parser.scanner.currentToken().name + "\n", end='')
			sys.exit()
		parser.scanner.nextToken()
		self.expr2 = Expr()
		self.expr2.parse(parser)
	
	def semantic(self, parser):
		self.expr1.semantic(parser)
		self.expr2.semantic(parser)
	
	def print(self):
		self.expr1.print()
		if self.option == 0:
			print("==", end='')
		elif self.option == 1:
			print("<", end='')
		elif self.option == 2:
			print("<=", end='')
		self.expr2.print()

class Expr:
	
	def parse(self, parser):
		self.option = 0
		self.term = Term()
		self.term.parse(parser)
		if parser.scanner.currentToken() == Core.ADD:
			self.option = 1
		elif parser.scanner.currentToken() == Core.SUB:
			self.option = 2
		if not self.option == 0:
			parser.scanner.nextToken()
			self.expr = Expr()
			self.expr.parse(parser)
	
	def semantic(self, parser):
		self.term.semantic(parser)
		if hasattr(self, 'expr'):
			self.expr.semantic(parser)
	
	def print(self):
		self.term.print()
		if self.option == 1:
			print("+", end='')
			self.expr.print()
		elif self.option == 2:
			print("-", end='')
			self.expr.print()

class Term:
	
	def parse(self, parser):
		self.factor = Factor()
		self.factor.parse(parser)
		if parser.scanner.currentToken() == Core.MULT:
			parser.scanner.nextToken()
			self.term = Term()
			self.term.parse(parser)
	
	def semantic(self, parser):
		self.factor.semantic(parser)
		if hasattr(self, 'term'):
			self.term.semantic(parser)
	
	def print(self):
		self.factor.print()
		if hasattr(self, 'term'):
			print("*", end='')
			self.term.print()

class Factor:

	def parse(self, parser):
		if parser.scanner.currentToken() == Core.ID:
			self.id = Id()
			self.id.parse(parser)
		elif parser.scanner.currentToken() == Core.CONST:
			self.constant = parser.scanner.getCONST()
			parser.scanner.nextToken()
		elif parser.scanner.currentToken() == Core.LPAREN:
			parser.scanner.nextToken()
			self.expr = Expr()
			self.expr.parse(parser)
			parser.expectedToken(Core.RPAREN)
			parser.scanner.nextToken()
		else:
			print("ERROR: Expected ID, CONST, or LPAREN, recieved " + parser.scanner.currentToken().name + "\n", end='')
			sys.exit()
	
	def semantic(self, parser):
		if hasattr(self, 'id'):
			self.id.semantic(parser)
		elif hasattr(self, 'expr'):
			self.expr.semantic(parser)
	
	def print(self):
		if hasattr(self, 'id'):
			self.id.print()
		elif hasattr(self, 'expr'):
			print("(", end='')
			self.expr.print()
			print(")", end='')
		else:
			print(self.constant, end='')
