//  키 이벤트 정보 출력하기
//  키 이벤트는 사용자가 키보드를 이용하여 입력을 하는 경우에 발생한다.
package KeyEvent;

import javax.swing.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

//  어떤 클래스가 키보드 이벤트를 처리하려면 KeyListener 인터페이스를 구현해야함
//  Action도 마찬가지
public class KeyEventFrame1 extends JFrame implements KeyListener {
    public KeyEventFrame1() {
        setTitle("이벤트 예제");
        setSize(300, 200);

        //  포커스란 키 입력을 받을 권리를 말한다.
        //  컴포넌트가 키 이벤트를 받으려면 반드시 포커스가 필요함.
        //  JTextField는 키보드 입력을 받기 위한 컴포넌트라서 자동으로 초기 포커스를 받음
        JTextField tf = new JTextField(20);
        tf.addKeyListener(this);
        add(tf);
        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    public void keyTyped(KeyEvent e) {
        display(e, "KeyTyped");
    }

    public void keyPressed(KeyEvent e) {
        display(e, "KeyPressed");
    }

    public void keyReleased(KeyEvent e) {
        display(e, "KeyReleased");
    }

    protected void display(KeyEvent e, String s) {
        //  KeyEvent에 들어있는 글자(유니코드)를 반환한다.
        char c = e.getKeyChar();

        //  KeyEvent에 들어 있는 키코드(상수)를 반환한다.
        int keyCode = e.getKeyCode();

        String modifiers = e.isAltDown() + " " + e.isControlDown() + " " + e.isShiftDown();
        System.out.println(s + " " + c + " " + keyCode + " " + modifiers);
    }

    public static void main(String[] args) {
        KeyEventFrame1 f = new KeyEventFrame1();
    }

}
