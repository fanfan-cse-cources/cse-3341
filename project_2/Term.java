
public class Term {

    private Factor f;
    private Term t;

    Term() {
        f = null;
        t = null;
    }

    public int[] parse(Scanner S) {
        f = new Factor();
        int[] val = f.parse(S);

        if (S.currentToken() == Core.MULT) {
            S.nextToken();
            t = new Term();
            t.parse(S);
        }

        return val;
    }

    public void print() {
        f.print();

        if (t != null) {
            System.out.print("*");
            t.print();
        }

    }
}
