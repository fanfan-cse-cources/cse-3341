- Yifan Yao

- Assign.java,Assign function
- Cmpr.java,Compare function
- Cond.java,Process of condition
- Core.java,Enum
- Decl.java,Process of declaration
- DeclSeq.java,Process of sequence of declaration
- Expr.java,Process of expression
- Factor.java,Process of factor
- IDList.java,Process of list of id
- If.java,Process of if
- In.java,Process of input
- Loop.java,Process of while loop
- Main.java,Main method
- Oper.java,Process of operations
- Out.java,Process of output
- Prog.java,Process of program
- Scanner.java,Scanner
- Stmt.java,Process of statement
- StmtSeq.java,Process of statement sequence
- Term.java,Process of terms
- README.txt,this file

- No special feature implemented.

- Each will have it's own class and calling each other recursively to creating a
 parsing tree. By passing the scanner to the class, they can easily identify which
 step need to do next, process by itself or calling parse method from lower level
 class. Since we have already known the language, we will be able to calling
 recursively.

- The program cannot output value of variables correctly, or parsing with certain
 token.
