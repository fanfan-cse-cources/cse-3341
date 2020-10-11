
public class Oper {

    private Core type;

    Oper() {
        type = null;
    }

    public void parse(Scanner S) {
        Core token = S.currentToken();

        if (token == Core.EQUAL || token == Core.LESS || token == Core.LESSEQUAL) {
            type = token;
        } else {
            System.err.println("Error: Invalid operator around " + S.currentToken() + ".");
        }

        S.nextToken();
    }

    public void print() {

        switch (type) {
            case EQUAL:
                System.out.print("==");
                break;

            case LESS:
                System.out.print("<");
                break;

            case LESSEQUAL:
                System.out.print("<=");
                break;

            default:
                break;
        }

    }
}
