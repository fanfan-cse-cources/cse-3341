import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;

public class Decl {

    private IDList listOfIDs;
    private LinkedList<String> ids;
    Map<String, Integer> v = new HashMap<String, Integer>();

    public Decl() {
        listOfIDs = null;
    }

    public void parse(Scanner S) {
        String current = this.getClass().getName();

        S.checkKeyword(Core.INT, current);

        S.nextToken(); // advance the token

        listOfIDs = new IDList();
        ids = listOfIDs.parse(S);

        for (String id : ids) {

            if (v.containsKey(id)) {
                System.err.println("Error: Variable \"" + id + "\" cannot be redeclare.");
            } else {
                v.put(id, null);
                S.addSet(id);
            }

        }

        S.checkKeyword(Core.SEMICOLON, current);

        S.nextToken();
    }

    public Map<String, Integer> getVarMap() {
        return v;
    }

    public void print() {
        System.out.print("  int ");
        listOfIDs.print();
        System.out.println(";");
    }
}
