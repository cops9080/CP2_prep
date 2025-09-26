package GUI2;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Frame2 extends JFrame {
    private JButton addBtn, subBtn;

    public Frame2() {
        JPanel p = new JPanel();
        JTextField t1 = new JTextField(5);
        JTextField t2 = new JTextField(5);
        JLabel l1 = new JLabel("결과: ");

        addBtn = new JButton("더하기");
        subBtn = new JButton("빼기");

        // 무명 클래스 이용
        ActionListener al = new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                int num1 = Integer.parseInt(t1.getText());
                int num2 = Integer.parseInt(t2.getText());
                int result = 0;

                if (e.getSource() == addBtn) {
                    result = num1 + num2;
                } else if (e.getSource() == subBtn) {
                    result = num1 - num2;
                }

                l1.setText("결과: " + result);
            }
        };

        addBtn.addActionListener(al);
        subBtn.addActionListener(al);

        p.add(t1);
        p.add(t2);
        p.add(addBtn);
        p.add(subBtn);
        p.add(l1);

        add(p);

        pack();
        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    public static void main(String[] args) {
        new Frame2();
    }
}
