
public class Assign {
    private Expr e;
    private Decl d;
    private String n;

    Assign() {
        e = null;
        d = new Decl();
        n = null;
    }

    public void parse(Scanner S) {

        String current = this.getClass().getName();

        S.checkKeyword(Core.ID, current);
        n = S.getID();
        S.nextToken();

        S.checkKeyword(Core.ASSIGN, current);
        S.nextToken();
        e = new Expr();

        int[] val = e.parse(S);

        if (val[0] == 1) {
            d.getVarMap().put(n, val[1]);
        }

        S.checkKeyword(Core.SEMICOLON, current);
        S.nextToken();
    }

    public void print() {
        System.out.print("  " + n + "=");
        e.print();
        System.out.println(";");
    }
}
