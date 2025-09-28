//  배경색 변경
package ActionEvent;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class ActionEventFrame1 extends JFrame {

    private JButton button1;
    private JButton button2;
    private JPanel panel;

    private class MyListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            if (e.getSource() == button1) {
                panel.setBackground(Color.YELLOW);
            } else if (e.getSource() == button2) {
                panel.setBackground(Color.PINK);
            }
        }
    }

    public ActionEventFrame1() {
        this.setSize(300, 200);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setTitle("Event Frame Exercise");
        panel = new JPanel();

        button1 = new JButton("YELLOW");
        button2 = new JButton("PINK");
        button1.addActionListener(new MyListener());
        button2.addActionListener(new MyListener());
        panel.add(button1);
        panel.add(button2);

        this.add(panel);
        this.setVisible(true);
        this.setDefaultCloseOperation(EXIT_ON_CLOSE);
    }

    public static void main(String[] args) {
        ActionEventFrame1 frame = new ActionEventFrame1();
    }
}
