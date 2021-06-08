// Skip List Node.
public class Node {
    int value; // Data
    Node next;
    Node down;

    private Node() {}
    public Node(int value) {
        this.value = value;
    }

    public Node(int value, Node next, Node down) {
        this.value = value;
        this.next = next;
        this.down = down;
    }

    @Override
    public String toString() {
        return String.format("[%d]", value);
    }
}
