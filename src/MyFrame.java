import javax.swing.*;

//프레임 생성 방법 2
public class MyFrame extends JFrame {
    public MyFrame() {
        setSize(300, 200);
        setTitle("MyFrame");

        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
    public static void main(String[] args) {
        MyFrame f = new MyFrame();
    }
}
