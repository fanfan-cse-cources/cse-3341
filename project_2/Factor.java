
public class Factor {

    private Factor f;
    private Expr e;
    private Core t;
    private Decl d;
    private String v;

    Factor() {
        f = null;
        e = null;
        t = null;
        d = new Decl();
        v = null;
    }

    public int[] parse(Scanner S) {
        String current = this.getClass().getName();
        int[] val = { 0, 0
        };

        if (S.currentToken() == Core.CONST) {
            t = Core.CONST;
            val[0] = 1;
            val[1] = S.getCONST();
            v = Integer.toString(S.getCONST());
            S.nextToken();
        } else if (S.currentToken() == Core.ID) {
            t = Core.ID;
            v = S.getID();

            if (!d.getVarMap().containsKey(v) && !S.inSet(v)) {
                System.err.println("Error: Cannot assign value to undeclared variable: \"" + v + "\".");
            }

            if (d.getVarMap().get(v) == null) {
                System.err.println("Error: \"" + v + "\" did not assigned with any value.");
            } else {
                val[0] = 1;
                val[1] = d.getVarMap().get(v);
            }

            S.nextToken();
        } else if (S.currentToken() == Core.SUB) {
            t = Core.SUB;
            S.nextToken();
            f = new Factor();
            f.parse(S);
        } else if (S.currentToken() == Core.LPAREN) {
            t = Core.LPAREN;
            S.nextToken();
            e = new Expr();
            e.parse(S);

            S.checkKeyword(Core.RPAREN, current);

            S.nextToken();
        } else {
            System.err.println("Error: Invalid factor.");
        }

        return val;
    }

    public void print() {

        switch (t) {
            case CONST:
            case ID:
                System.out.print(v);
                break;

            case SUB:
                System.out.print("-");
                f.print();
                break;

            case LPAREN:
                System.out.print("(");
                e.print();
                System.out.print(")");
            default:
                break;
        }

    }
}
