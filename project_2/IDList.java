import java.util.LinkedList;

public class IDList {

    private LinkedList<String> listOfIDs = new LinkedList<String>();
    private IDList idList;

    public IDList() {
        idList = null;
    }

    public LinkedList<String> parse(Scanner S) {

        if (S.currentToken() == Core.ID) {
            listOfIDs.add(S.getID());
        }

        S.nextToken();

        if (S.currentToken() == Core.COMMA) {
            S.nextToken();
            idList = new IDList();
            idList.parse(S);
        }

        return listOfIDs;
    }

    public void clear() {
        listOfIDs.clear();
    }

    public void print() {

        if (listOfIDs.size() == 1) {
            System.out.print(listOfIDs.getFirst());
        } else {

            for (String id : listOfIDs) {

                if (id == listOfIDs.getLast()) {
                    System.out.print(id);
                } else {
                    System.out.print(id + ",");
                }

            }

        }

    }
}
