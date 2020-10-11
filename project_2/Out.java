
public class Out {
    private IDList idList;

    Out() {
        idList = null;
    }

    public void parse(Scanner S) {
        String current = this.getClass().getName();
        S.checkKeyword(Core.OUTPUT, current);

        S.nextToken();
        idList = new IDList();
        idList.parse(S);

        S.checkKeyword(Core.SEMICOLON, current);

        S.nextToken();
    }

    public void print() {
        System.out.print("  output ");
        idList.print();
        System.out.println(";");
    }
}
