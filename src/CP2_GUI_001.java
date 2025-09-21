import javax.swing.*;

//프레임 생성 방법 1
public class CP2_GUI_001 {
    public static void main(String[] args) {
        //Graphical User Interface, GUI는 컴포넌트들로 구성됨
        // 자바에서 GUI의 종류는 AWT와 SWING이 있다

        //프레임 생성
        JFrame f = new JFrame("Frame Test");
        f.setTitle("My Frame");
        f.setSize(300,200);
        f.setVisible(true);
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
}
