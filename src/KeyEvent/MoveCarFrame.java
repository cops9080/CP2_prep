//  자동차 움직이기

package KeyEvent;

import javax.swing.*;
import java.awt.event.*;

public class MoveCarFrame extends JFrame{
    int img_x = 512;
    int img_y = 512;
    JButton button;

    public MoveCarFrame() {
        setSize(1200, 600);
        button = new JButton("");
        ImageIcon icon = new ImageIcon("img\\8308414.png");
        button.setIcon(icon);

        JPanel panel = new JPanel();
        panel.setLayout(null);
        button.setLocation(img_x, img_y);
        button.setSize(512, 512);

        panel.add(button);
        panel.requestFocus();
        panel.setFocusable(true);

        //  익명 클래스를 이용해 KeyListener를 구현하는 클래스 작성
        panel.addKeyListener(new KeyListener() {
            public void keyPressed(KeyEvent e) {
                int keycode = e.getKeyCode();
                switch (keycode) {
                    case KeyEvent.VK_UP: img_y -= 10; break;
                    case KeyEvent.VK_DOWN: img_y += 10; break;
                    case KeyEvent.VK_LEFT: img_x -= 10; break;
                    case KeyEvent.VK_RIGHT: img_x += 10; break;
                }
                button.setLocation(img_x, img_y);
            }
            public void keyReleased(KeyEvent arg0) {}
            public void keyTyped(KeyEvent arg0) {}
        });
        add(panel);
        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    public static void main(String[] args) {
        MoveCarFrame frame = new MoveCarFrame();
    }
}
