class Prog{
	DeclSeq ds;
	StmtSeq ss;

	parse() {
		if (currentToken() != Core.PROGRAM) {
			// Print error message and stop parsing
		}
		nextToken();
		ds = new DeclSeq();
		ds.parse();
		if (currentToken() != Core.BEGIN) {
			// Print error message and stop parsing
		}
		nextToken();
		ss = new StmtSeq();
		ss.parse();
		if (currentToken() != Core.END) {
			// Print error message and stop parsing
		}
		nextToken();
		if (currentToken() != Core.EOF) {
			// Print error message and stop parsing
		}
	}

	print() {
		System.out.println("program");
		ds.print();
		System.out.println("begin");
		ss.print();
		System.out.println("end");
	}
}