class Main {
    public static void main(String[] args) {
        // Initialize the scanner with the input file
        Scanner S = new Scanner(args[0]);

        Prog prog = new Prog();

        if (S.currentToken() == Core.PROGRAM) {
            prog.parse(S);
            prog.print();
        }

    }
}
