class Main {
	public static void main(String[] args) {
		// Initialize the scanner with the input file
		Scanner S = new Scanner(args[0]);

		Parser parser = new Parser(S);
		
		parser.parse();
		
		parser.semantic();
		
		parser.print();
	}
}