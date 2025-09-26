package GUI2;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Frame3 extends JFrame {
    private JPanel panel1 ,panel2;
    private JButton btn;
    private JLabel label;
    int cnt = 0;

    public Frame3() {
        panel1 = new JPanel();
        panel2 = new JPanel();
        btn = new JButton("버튼");
        label = new JLabel("결과 : ");

        //  내부 클래스로 이벤트 처리기를 작성
        class Listener implements ActionListener {
            public void actionPerformed(ActionEvent e) {
                cnt++;
                label.setText("결과 : " + cnt);
            }
        }

        btn.addActionListener(new Listener());

        panel1.add(label);
        panel2.add(btn);

        add(panel1, BorderLayout.NORTH);
        add(panel2, BorderLayout.CENTER);

        setTitle("숫자 증가");
        setSize(200, 100);
        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    public static void main(String[] args) {
        new Frame3();
    }
}
