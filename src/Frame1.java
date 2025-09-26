import javax.swing.*;
import java.awt.FlowLayout;

//배치관리자
public class Frame1 extends JFrame {
    public Frame1() {
        setTitle("operater");
        setSize(400, 400);

        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    public static void main(String[] args) {
        Frame1 f = new Frame1();
    }
}
