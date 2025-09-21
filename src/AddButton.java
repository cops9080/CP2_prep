import javax.swing.*;
import java.awt.FlowLayout;

//프레임 생성 방법 2
public class AddButton extends JFrame {
    public AddButton() {
        setSize(300, 200);
        setTitle("MyFrame");

        //버튼 추가
        setLayout(new FlowLayout());
        JButton button = new JButton("Button");
        add(button);

        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
    public static void main(String[] args) {
        AddButton f = new AddButton();
    }
}
