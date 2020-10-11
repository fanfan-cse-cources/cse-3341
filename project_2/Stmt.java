
public class Stmt {

    private Decl d;
    private If i;
    private Loop loop;
    private In in;
    private Out out;
    private Assign ass;
    private Core type;

    public Stmt() {
        d = null;
        i = null;
        loop = null;
        in = null;
        out = null;
        ass = null;
        type = null;
    }

    public void parse(Scanner S) {
        Core token = S.currentToken();
        type = token;

        switch (token) {
            case INT:
                d = new Decl();
                d.parse(S);
                break;

            case IF:
                i = new If();
                i.parse(S);
                break;

            case WHILE:
                loop = new Loop();
                loop.parse(S);
                break;

            case INPUT:
                in = new In();
                in.parse(S);
                break;

            case OUTPUT:
                out = new Out();
                out.parse(S);
                break;

            default:
                ass = new Assign();
                ass.parse(S);
                break;
        }

    }

    public void print() {

        switch (type) {
            case INT:
                d.print();
                break;

            case ID:
                ass.print();
                break;

            case IF:
                i.print();
                break;

            case WHILE:
                loop.print();
                break;

            case INPUT:
                in.print();
                break;

            case OUTPUT:
                out.print();
                break;

            default:
                break;
        }

    }
}
