import javax.swing.*;
import java.awt.*;

public class CP2_GUI_002 extends JFrame {
    public CP2_GUI_002() {
        setTitle("Add Button");               //setTitle() 타이틓 바의 제목 변경
        setSize(200, 400);        //setSize() 프레임 크기 설정
        setLayout(new  FlowLayout());
        getContentPane().setBackground(Color.orange); //배경색 변경

        JButton b1 = new JButton("Add Button");
        // 중요한 메소드
        this.add(b1);                              //add(component) 프레임에 컴포넌트 추가
        setLocation(100, 100);          //setLocation(x, y) 프레임 위치 설정
        //setIconImage(IconImage) 타이틀 바, 태스크 스위처에 표시할 아이콘 설정

        setResizable(true);                   //setResizable() 사용자가 크기를 조절할 수 있는지 설정

        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
    public static void main(String[] args) {
        CP2_GUI_002 f = new CP2_GUI_002();
    }
}
