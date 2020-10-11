
public class Cmpr {

    private Expr e1;
    private Expr e2;
    private Oper cmp;

    Cmpr() {
        e1 = null;
        e2 = null;
        cmp = null;
    }

    public void parse(Scanner S) {

        e1 = new Expr();
        e1.parse(S);
        cmp = new Oper();
        cmp.parse(S);
        e2 = new Expr();
        e2.parse(S);
    }

    public void print() {
        e1.print();
        cmp.print();
        e2.print();

    }

}
