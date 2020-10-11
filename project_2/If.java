
public class If {
    private Cond c;
    private StmtSeq ss;
    private StmtSeq ss1;

    If() {
        c = null;
        ss = null;
        ss1 = null;
    }

    public void parse(Scanner S) {
        String current = this.getClass().getName();
        S.checkKeyword(Core.IF, current);
        S.nextToken();

        c = new Cond();
        c.parse(S);
        S.checkKeyword(Core.THEN, current);
        S.nextToken();

        ss = new StmtSeq();
        ss.parse(S);

        if (S.currentToken() == Core.ELSE) {
            S.nextToken();
            ss1 = new StmtSeq();
            ss1.parse(S);
        }

        S.checkKeyword(Core.ENDIF, current);
        S.nextToken(); // SEMICOL

        S.checkKeyword(Core.SEMICOLON, current);
        S.nextToken();
    }

    public void print() {
        System.out.print("  if ");
        c.print();
        System.out.println(" then");
        System.out.print("  ");
        ss.print();

        if (ss1 != null) {
            System.out.println("  else");
            System.out.print("  ");
            ss1.print();
        }

        System.out.println("  endif;");
    }
}
