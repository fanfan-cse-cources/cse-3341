import java.util.*;

// Parser class contains all the non-terminal classes
class Parser {
	//scanner is stored here so it is avaiable to the parse method of all contained classes
	Scanner scanner;
	//program is the root of the parse tree
	Program program;
	//scopes is a data structure for the semantic checks performed after parsing
	Stack<ArrayList<String>> scopes;
	
	//Constructor for Parser. Initializes the scanner.
	Parser(Scanner s) {
		this.scanner = s;
	}
	
	//parse starts the recursive desccent parser
	void parse() {
		program = new Program();
		program.parse();
	}
	
	//semantic should be called after parsing to perform semantic checks on the parse tree
	//this is what find doubly-declared variables and variables not in scope
	void semantic() {
		scopes = new Stack<ArrayList<String>>();
		program.semantic();
	}
	
	//print will walk over the tree and print the program
	void print() {
		program.print();
	}
	
	//helper method for the semantic checks
	//returns true if the string x is the name of a variable that is in scope
	boolean nestedScopeCheck(String x) {
		boolean match = false;
		if (!scopes.empty()) {
			ArrayList<String> temp = scopes.pop();
			match = temp.contains(x);
			if (!match) {
				match = nestedScopeCheck(x);
			}
			scopes.push(temp);
		}
		return match;
	}
	
	//helper method for the semantic checks
	//returns true if the string x is the name of a variable that was declared in the current scope
	boolean currentScopeCheck(String x) {
		boolean match = false;
		if (!scopes.empty()) {
			match = scopes.peek().contains(x);
		}
		return match;
	}
	
	//helper method for handling error messages, used by the parse methods
	void expectedToken(Core expected) {
		if (scanner.currentToken() != expected) {
			System.out.println("ERROR: Expected " + expected + ", recieved " + scanner.currentToken());
			System.exit(0);
		}
	}
	
	/*
	* This is where the contained classes being
	* Each non-terminal of the grammar has a class
	* Each class has a parse, a semantic, and a print method
	*/
	
	class Program {
		DeclSeq ds;
		StmtSeq ss;
		
		void parse() {
			expectedToken(Core.PROGRAM);
			scanner.nextToken();
			ds = new DeclSeq();
			ds.parse();
			expectedToken(Core.BEGIN);
			scanner.nextToken();
			ss = new StmtSeq();
			ss.parse();
			expectedToken(Core.END);
			scanner.nextToken();
			expectedToken(Core.EOF);
		}
		
		void semantic() {
			scopes.push(new ArrayList<String>());
			ds.semantic();
			scopes.push(new ArrayList<String>());
			ss.semantic();
			scopes.pop();
		}
		
		void print() {
			System.out.println("program");
			ds.print(1);
			System.out.println("begin");
			ss.print(1);
			System.out.println("end");
		}
	}
	
	class DeclSeq {
		Decl decl;
		DeclSeq ds;
		
		void parse() {
			decl = new Decl();
			decl.parse();
			if (scanner.currentToken() != Core.BEGIN) {
				ds = new DeclSeq();
				ds.parse();
			}
		}
		
		void semantic() {
			decl.semantic();
			if (ds != null) {
				ds.semantic();
			}
		}
		
		void print(int indent) {
			decl.print(indent);
			if (ds != null) {
				ds.print(indent);
			}
		}
	}
	
	//Stmt is an interface so we can take advantage of some polymorphism in StmtSeq
	interface Stmt {
		void parse();
		void semantic();
		void print(int indent);
	}
	
	class StmtSeq {
		Stmt stmt;
		StmtSeq ss;
		
		void parse() {
			if (scanner.currentToken() == Core.ID) {
				stmt = new Assign();
			} else if (scanner.currentToken() == Core.INPUT) {
				stmt = new Input();
			} else if (scanner.currentToken() == Core.OUTPUT) {
				stmt = new Output();
			}  else if (scanner.currentToken() == Core.IF) {
				stmt = new If();
			} else if (scanner.currentToken() == Core.WHILE) {
				stmt = new Loop();
			}  else if (scanner.currentToken() == Core.INT) {
				stmt = new Decl();
			} else {
				System.out.println("ERROR: Bad start to statement: " + scanner.currentToken());
				System.exit(0);
			}
			stmt.parse();
			if ((scanner.currentToken() != Core.END) 
				&& (scanner.currentToken() != Core.ENDIF)
				&& (scanner.currentToken() != Core.ENDWHILE)
				&& (scanner.currentToken() != Core.ELSE)) {
				ss = new StmtSeq();
				ss.parse();
			}
		}
		
		void semantic() {
			stmt.semantic();
			if (ss != null) {
				ss.semantic();
			}
		}
		
		void print(int indent) {
			stmt.print(indent);
			if (ss != null) {
				ss.print(indent);
			}
		}
	}
	
	class Decl implements Stmt {
		IdList list;
		
		public void parse() {
			expectedToken(Core.INT);
			scanner.nextToken();
			list = new IdList();
			list.parse();
			expectedToken(Core.SEMICOLON);
			scanner.nextToken();
		}
		
		public void semantic() {
			list.semantic();
		}
		
		public void print(int indent) {
			for (int i=0; i<indent; i++) {
				System.out.print("  ");
			}
			System.out.print("int ");
			list.print();
			System.out.println(";");
		}
	}
	
	class IdList {
		Id id;
		IdList list;
		
		void parse() {
			id = new Id();
			id.parse();
			if (scanner.currentToken() == Core.COMMA) {
				scanner.nextToken();
				list = new IdList();
				list.parse();
			} 
		}
		
		void semantic() {
			id.doublyDeclared();
			id.addToScope();
			if (list != null) {
				list.semantic();
			}
		}
		
		void print() {
			id.print();
			if (list != null) {
				System.out.print(",");
				list.print();
			}
		}
	}
	
	class Id {
		String identifier;
		
		void parse() {
			expectedToken(Core.ID);
			identifier = scanner.getID();
			scanner.nextToken();
		}
		
		void semantic() {
			if (!nestedScopeCheck(identifier)) {
				System.out.println("ERROR: No matching declaration found: " + identifier);
				System.exit(0);
			}
		}
		
		//Called by Decl.semantic to add the variable to the scopes data structure
		void addToScope() {
			scopes.peek().add(identifier);
		}
		
		//Called by Decl.semantic to check for doubly declared variables
		void doublyDeclared() {
			if (currentScopeCheck(identifier)) {
				System.out.println("ERROR: Doubly declared variable detected: " + identifier);
				System.exit(0);
			}
		}
		
		void print() {
			System.out.print(identifier);
		}
	}
	
	class Assign implements Stmt {
		Id id;
		Expr expr;
		
		public void parse() {
			id = new Id();
			id.parse();
			expectedToken(Core.ASSIGN);
			scanner.nextToken();
			expr = new Expr();
			expr.parse();
			expectedToken(Core.SEMICOLON);
			scanner.nextToken();
		}
		
		public void semantic() {
			id.semantic();
			expr.semantic();
		}
		
		public void print(int indent) {
			for (int i=0; i<indent; i++) {
				System.out.print("  ");
			}
			id.print();
			System.out.print("=");
			expr.print();
			System.out.println(";");
		}
	}
	
	class Input implements Stmt {
		Id id;
		
		public void parse() {
			scanner.nextToken();
			id = new Id();
			id.parse();
			expectedToken(Core.SEMICOLON);
			scanner.nextToken();
		}
		
		public void semantic() {
			id.semantic();
		}
		
		public void print(int indent) {
			for (int i=0; i<indent; i++) {
				System.out.print("  ");
			}
			System.out.print("input ");
			id.print();
			System.out.println(";");
		}
	}
	
	class Output implements Stmt {
		Expr expr;
		
		public void parse() {
			scanner.nextToken();
			expr = new Expr();
			expr.parse();
			expectedToken(Core.SEMICOLON);
			scanner.nextToken();
		}
		
		public void semantic() {
			expr.semantic();
		}
		
		public void print(int indent) {
			for (int i=0; i<indent; i++) {
				System.out.print("  ");
			}
			System.out.print("output ");
			expr.print();
			System.out.println(";");
		}
	}
	
	class If implements Stmt {
		Cond cond;
		StmtSeq ss1;
		StmtSeq ss2;
		
		public void parse() {
			scanner.nextToken();
			cond = new Cond();;
			cond.parse();
			expectedToken(Core.THEN);
			scanner.nextToken();
			ss1 = new StmtSeq();
			ss1.parse();
			if (scanner.currentToken() == Core.ELSE) {
				scanner.nextToken();
				ss2 = new StmtSeq();
				ss2.parse();
			}
			expectedToken(Core.ENDIF);
			scanner.nextToken();
			expectedToken(Core.SEMICOLON);
			scanner.nextToken();
		}
		
		public void semantic() {
			cond.semantic();
			scopes.push(new ArrayList<String>());
			ss1.semantic();
			scopes.pop();
			if (ss2 != null) {
				scopes.push(new ArrayList<String>());
				ss2.semantic();
				scopes.pop();
			}
		}
		
		public void print(int indent) {
			for (int i=0; i<indent; i++) {
				System.out.print("  ");
			}
			System.out.print("if ");
			cond.print();
			System.out.println(" then");
			ss1.print(indent+1);
			if (ss2 != null) {
				for (int i=0; i<indent; i++) {
					System.out.print("  ");
				}
				System.out.println("else");
				ss2.print(indent+1);
			}
			for (int i=0; i<indent; i++) {
				System.out.print("  ");
			}
			System.out.print("endif");
			System.out.println(";");
		}
	}
	
	class Loop implements Stmt {
		Cond cond;
		StmtSeq ss;
		
		public void parse() {
			scanner.nextToken();
			cond = new Cond();;
			cond.parse();
			expectedToken(Core.BEGIN);
			scanner.nextToken();
			ss = new StmtSeq();
			ss.parse();
			expectedToken(Core.ENDWHILE);
			scanner.nextToken();
			expectedToken(Core.SEMICOLON);
			scanner.nextToken();
		}
		
		public void semantic() {
			cond.semantic();
			scopes.push(new ArrayList<String>());
			ss.semantic();
			scopes.pop();
		}
		
		public void print(int indent) {
			for (int i=0; i<indent; i++) {
				System.out.print("  ");
			}
			System.out.print("while ");
			cond.print();
			System.out.println(" begin");
			ss.print(indent+1);
			for (int i=0; i<indent; i++) {
				System.out.print("  ");
			}
			System.out.print("endwhile");
			System.out.println(";");
		}
	}
	
	class Cond {
		Cmpr cmpr;
		Cond cond;
		
		void parse() {
			if (scanner.currentToken() == Core.NEGATION){
				scanner.nextToken();
				expectedToken(Core.LPAREN);
				scanner.nextToken();
				cond = new Cond();
				cond.parse();
				expectedToken(Core.RPAREN);
				scanner.nextToken();
			} else {
				cmpr = new Cmpr();
				cmpr.parse();
				if (scanner.currentToken() == Core.OR) {
					scanner.nextToken();
					cond = new Cond();
					cond.parse();
				}
			}
		}
		
		void semantic() {
			if (cmpr == null) {
				cond.semantic();
			} else {
				cmpr.semantic();
				if (cond != null) {
					cond.semantic();
				}
			}
		}
		
		void print() {
			if (cmpr == null) {
				System.out.print("!(");
				cond.print();
				System.out.print(")");
			} else {
				cmpr.print();
				if (cond != null) {
					System.out.print(" or ");
					cond.print();
				}
			}
		}
	}
	
	class Cmpr {
		Expr expr1;
		Expr expr2;
		int option;
		
		void parse() {
			expr1 = new Expr();
			expr1.parse();
			if (scanner.currentToken() == Core.EQUAL) {
				option = 0;
			} else if (scanner.currentToken() == Core.LESS) {
				option = 1;
			} else if (scanner.currentToken() == Core.LESSEQUAL) {
				option = 2;
			} else {
				System.out.println("ERROR: Expected EQUAL, LESS, or LESSEQUAL, recieved " + scanner.currentToken());
				System.exit(0);
			}
			scanner.nextToken();
			expr2 = new Expr();
			expr2.parse();
		}
		
		void semantic() {
			expr1.semantic();
			expr2.semantic();
		}
		
		void print() {
			expr1.print();
			switch(option) {
				case 0:
					System.out.print("==");
					break;
				case 1:
					System.out.print("<");
					break;
				case 2:
					System.out.print("<=");
					break;
			}
			expr2.print();
		}
	}
	
	class Expr {
		Term term;
		Expr expr;
		int option;
		
		void parse() {
			term  = new Term();
			term.parse();
			if (scanner.currentToken() == Core.ADD) {
				option = 1;
			} else if (scanner.currentToken() == Core.SUB) {
				option = 2;
			}
			if (option != 0) {
				scanner.nextToken();
				expr = new Expr();
				expr.parse();
			}						
		}
		
		void semantic() {
			term.semantic();
			if (expr != null) {
				expr.semantic();
			}
		}
		
		void print() {
			term.print();
			if (option == 1) {
				System.out.print("+");
				expr.print();
			} else if (option == 2) {
				System.out.print("-");
				expr.print();
			}
		}
	}
	
	class Term {
		Factor factor;
		Term term;
		
		void parse() {
			factor = new Factor();
			factor.parse();
			if (scanner.currentToken() == Core.MULT) {
				scanner.nextToken();
				term = new Term();
				term.parse();
			}				
		}
		
		void semantic() {
			factor.semantic();
			if (term != null) {
				term.semantic();
			}
		}
		
		void print() {
			factor.print();
			if (term != null) {
				System.out.print("*");
				term.print();
			}
		}
	}
	
	class Factor {
		Id id;
		int constant;
		Expr expr;
		
		void parse() {
			if (scanner.currentToken() == Core.ID) {
				id = new Id();
				id.parse();
			} else if (scanner.currentToken() == Core.CONST) {
				constant = scanner.getCONST();
				scanner.nextToken();
			} else if (scanner.currentToken() == Core.LPAREN) {
				scanner.nextToken();
				expr = new Expr();
				expr.parse();
				expectedToken(Core.RPAREN);
				scanner.nextToken();
			} else {
				System.out.println("ERROR: Expected ID, CONST, or LPAREN, recieved " + scanner.currentToken());
				System.exit(0);
			}
		}
		
		void semantic() {
			if (id != null) {
				id.semantic();
			} else if (expr != null) {
				expr.semantic();
			}
		}
		
		void print() {
			if (id != null) {
				id.print();
			} else if (expr != null) {
				System.out.print("(");
				expr.print();
				System.out.print(")");
			} else {
				System.out.print(constant);
			}
		}
	}

}