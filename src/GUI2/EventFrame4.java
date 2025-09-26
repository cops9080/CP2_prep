package GUI2;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

//  프레임 클래스 이용
public class EventFrame4 extends JFrame implements ActionListener {
    private JPanel panel1, panel2;
    private JButton btn;
    private JLabel label;

    int cnt = 0;

    public void actionPerformed(ActionEvent e) {
        cnt++;
        label.setText("현재의 카운트 값: " + cnt + " 다음 카운트 값: "+(cnt+1));
    }

    public EventFrame4() {

        panel1 = new JPanel();
        panel2 = new JPanel();

        label = new JLabel("현재의 카운트 값: " + cnt + " 다음 카운트 값: " + (cnt+1));

        btn = new JButton("카운트 증가");
        btn.addActionListener(this);

        panel1.add(label);
        panel2.add(btn);

        add(panel1, BorderLayout.CENTER);
        add(panel2, BorderLayout.SOUTH);

        this.setTitle("카운트");
        this.setSize(300, 300);
        this.setVisible(true);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    public static void main(String[] args) {
        EventFrame4 frame = new EventFrame4();
    }
}
