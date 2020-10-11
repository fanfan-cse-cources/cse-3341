
public class DeclSeq {
    private DeclSeq ds;
    private Decl d;

    DeclSeq() {
        ds = null;
        d = null;
    }

    public void parse(Scanner S) {
        d = new Decl();
        d.parse(S);

        if (S.currentToken() == Core.INT) {
            ds = new DeclSeq();
            ds.parse(S);
        }

    }

    public void print() {
        d.print();

        if (ds != null) {
            ds.print();
        }

    }
}
