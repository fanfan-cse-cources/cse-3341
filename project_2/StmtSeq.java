
public class StmtSeq {

    private Stmt st;
    private StmtSeq ss;

    public StmtSeq() {
        st = null;
        ss = null;
    }

    public void parse(Scanner S) {
        st = new Stmt();
        st.parse(S);

        Core token = S.currentToken();

        if (token == Core.ID || token == Core.IF || token == Core.WHILE || token == Core.INPUT || token == Core.OUTPUT
                || token == Core.INT) {
            ss = new StmtSeq();
            ss.parse(S);
        }

    }

    public void print() {
        st.print();

        if (ss != null) {
            ss.print();
        }

    }
}
