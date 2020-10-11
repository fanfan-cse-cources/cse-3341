
public class Expr {

    private Term t;
    private Expr e;
    private Core type;

    Expr() {
        t = null;
        e = null;
        type = null;
    }

    public int[] parse(Scanner S) {
        t = new Term();
        int[] val = t.parse(S);
        type = S.currentToken();

        if (S.currentToken() == Core.ADD) {
            S.nextToken();
            e = new Expr();
            e.parse(S);
        } else if (S.currentToken() == Core.SUB) {
            S.nextToken();
            e = new Expr();
            e.parse(S);
        }

        return val;
    }

    public void print() {
        t.print();

        if (e != null) {

            if (type == Core.ADD) {
                System.out.print("+");
            } else if (type == Core.SUB) {
                System.out.print("-");
            }

            e.print();
        }

    }
}
