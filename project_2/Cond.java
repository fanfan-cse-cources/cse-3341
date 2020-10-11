
public class Cond {

    private Cmpr cm;
    private Cond c1;
    private Cond c2;
    private Core type;

    Cond() {
        cm = null;
        c1 = null;
        c2 = null;
        type = null;
    }

    public void parse(Scanner S) {
        String current = this.getClass().getName();
        Core token = S.currentToken();

        switch (token) {
            case LESS:
            case CONST:
                type = token;
                cm = new Cmpr();
                cm.parse(S);
                break;

            case NEGATION:
                type = token;
                S.nextToken();
                c1 = new Cond();
                c1.parse(S);
                break;

            case LPAREN:
                S.nextToken();
                c1 = new Cond();
                c1.parse(S);
                if (S.currentToken() == Core.OR) {
                    type = Core.OR;
                } else {
                    System.err.println("ERROR: Invalid operator in condition");
                }
                S.nextToken();
                c2 = new Cond();
                c2.parse(S);

                S.checkKeyword(Core.RPAREN, current);

                S.nextToken();
                break;

            default:
                System.err.println("ERROR: Invalid operator in condition");
                break;

        }

    }

    public void print() {

        switch (type) {
            case CONST:
            case LESS:
                cm.print();
                break;

            case NEGATION:
                System.out.print("!");
                c1.print();
                break;

            default:
                c1.print();
                if (type == Core.OR) {
                    System.out.print(" || ");
                }
                c2.print();
                break;
        }

    }

}
