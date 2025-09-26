//  이벤트 리스너
package GUI2;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

//  1.먼저 이벤트 리스너를 작성한다.
//  리스너 인터페이스를 구현해야지 이벤트 리스너가 될 수 있다.
//  버튼의 경우, ActionListener
class MyListener implements ActionListener {
    private int a = 1;
    public void actionPerformed(ActionEvent e) {
        System.out.println(a);
        a++;
    }
}

public class Frame1 extends JFrame {
    public Frame1() {
        JPanel p;
        p = new JPanel();

        //  버튼
        JButton b;
        b = new JButton("클릭해 봐");

        //  이벤트 리스너를 컴포넌트에 등록한다.
        //  이벤트 리스너 객체를 생성하고 버튼에 그 객체를 등록한다.
        b.addActionListener(new MyListener());
        p.add(b);

        add(p);

        pack();

        setSize(400,400);
        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    public static void main(String[] args) {
        new Frame1();
    }

}
