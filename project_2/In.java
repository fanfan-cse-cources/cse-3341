import java.util.LinkedList;

public class In {

    private IDList idList;
    private LinkedList<String> listOfIDs;
    private Decl declList;

    In() {
        idList = null;
        listOfIDs = new LinkedList<String>();
        declList = new Decl();
    }

    public void parse(Scanner S) {
        String current = this.getClass().getName();
        S.checkKeyword(Core.INPUT, current);

        S.nextToken();
        idList = new IDList();
        listOfIDs = idList.parse(S);

        for (String id : listOfIDs) {

            if (!declList.getVarMap().containsKey(id)) {
                System.err.println("Error: Variable \"" + id + "\" did not undeclared.");
            } else {
                declList.getVarMap().put(id, S.getCONST());
            }

        }

        idList.clear();

        S.checkKeyword(Core.SEMICOLON, current);

        S.nextToken();

    }

    public void print() {
        System.out.print("  input ");
        idList.print();
        System.out.println(";");
    }
}
