class Prog {
    DeclSeq ds;
    StmtSeq ss;

    void parse(Scanner S) {
        String current = this.getClass().getName();
        S.checkKeyword(Core.PROGRAM, current);

        S.nextToken(); // token after program
        ds = new DeclSeq();
        ds.parse(S);

        S.checkKeyword(Core.BEGIN, current);

        S.nextToken(); // token after begin
        ss = new StmtSeq();
        ss.parse(S);

        S.checkKeyword(Core.END, current);

        S.nextToken();

        S.checkKeyword(Core.EOF, current);
    }

    void print() {
        System.out.println("program");
        ds.print();
        System.out.println("begin");
        ss.print();
        System.out.println("end");
    }
}
