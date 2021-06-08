import java.util.Deque;
import java.util.LinkedList;


/**
 * @author: HUY NGUYEN
 * Skip List implementation (Just for academia purpose only).
 * Extremely naive without MAX_LAYERS
 * SOURCE: https://drum.lib.umd.edu/bitstream/handle/1903/544/CS-TR-2286.1.pdf;sequence=2
 */

public class SkipList {
    public static void main(String[] args) {
        SkipList myList = new SkipList();
        myList.insert(1);
        myList.insert(1);
        assert myList.search(1) == true;
        myList.insert(3);
        myList.insert(-5);
        myList.insert(2);
        assert myList.search(3) == true;
        assert myList.search(-5) == true;
        assert myList.search(-1) == false;
        assert myList.delete(1) == true;
        assert myList.delete(1) == true;
        assert myList.delete(1) == false;
    }

    private Node head; // Top left node.
    private double p; // Probability for adding new level.

    public SkipList() {
        head = new Node(Integer.MIN_VALUE);
        p = 0.5;
    }
    
    public SkipList(double p) {
        assert p > 0 && p < 1;
        head = new Node(Integer.MIN_VALUE);
        this.p = p;
    }

    public boolean flip() { // Binomial random.
        return Math.random() < p;
    }

    // Time: θ(log(n)), space: θ(log(n))
    // Time: O(n), space: O(n)
    public void insert(int value) {
        Node currNode = head;
        Deque<Node> stack = new LinkedList<>();

        while(currNode != null) {
            while(currNode.next != null && currNode.next.value < value)
                currNode = currNode.next;
            stack.addFirst(currNode); // Add last node of each layer to the stack.
            currNode = currNode.down;
        }

        boolean add = true;
        Node down = null;

        while(add && !stack.isEmpty()) { // Add a new layer if add is true.
            currNode = stack.removeFirst();
            currNode.next = new Node(value, currNode.next, down);
            down = currNode.next;
            add = flip();
        }
        if(add) head = new Node(Integer.MIN_VALUE, null, head); // Assign new head for new layer.
    }

    // Time: θ(log(n)), space: θ(1)
    // Time: O(n), space: O(1)
    public boolean search(int value) {
        Node currNode = head;
        while(currNode != null) {
            while(currNode.next != null && currNode.next.value < value)
                currNode = currNode.next;
            if(currNode.next != null && currNode.next.value == value) return true; // FOUND!
            else currNode = currNode.down;
        }

        return false;
    }
    
    // Time: θ(log(n)), space: θ(1)
    // Time: O(n), space: O(1)
    public boolean delete(int value) {
        Node currNode = head;
        boolean found = false;

        while(currNode != null) {
            while(currNode.next != null && currNode.next.value < value)
                currNode = currNode.next;
            if(currNode.next != null && currNode.next.value == value) { // FOUND
                currNode.next = currNode.next.next;
                found = true;
            }
            currNode = currNode.down;
        }

        return found;
    }
}
