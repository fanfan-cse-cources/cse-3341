
public class Loop {
    private StmtSeq ss;
    private Cond c;

    Loop() {
        ss = null;
        c = null;
    }

    public void parse(Scanner S) {
        String current = this.getClass().getName();
        S.checkKeyword(Core.WHILE, current);
        S.nextToken();
        c = new Cond();
        c.parse(S);

        S.checkKeyword(Core.BEGIN, current);
        S.nextToken();

        ss = new StmtSeq();
        ss.parse(S);

        S.checkKeyword(Core.ENDWHILE, current);
        S.nextToken();

        S.checkKeyword(Core.SEMICOLON, current);
        S.nextToken();
    }

    public void print() {
        System.out.print("  while ");
        c.print();
        System.out.println(" begin ");
        ss.print();
        System.out.println(" endwhile;");
    }

}
