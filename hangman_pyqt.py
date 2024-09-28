import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QGridLayout,
    QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
)
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from string import ascii_uppercase

class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 400)
        self.lines = [
            ((40, 55), (180, 55), 10),
            ((165, 60), (165, 365), 10),
            ((160, 360), (100, 360), 10),
            ((100, 365), (100, 330), 10),
            ((100, 330), (100, 310), 1),
        ]

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black)
        painter.setRenderHint(QPainter.Antialiasing)

        height = self.height()  # 창의 높이를 가져옵니다.

        for line in self.lines:
            (x1, y1), (x2, y2), width = line
            pen.setWidth(width)
            painter.setPen(pen)
            # y좌표를 반전시켜 그립니다.
            painter.drawLine(x1, height - y1, x2, height - y2)
        
        painter.end()

class Hangman(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hangman")
        self.init_ui()
        self.show()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 상단 레이아웃: 캔버스와 글자 버튼
        top_layout = QHBoxLayout()
        
        # 캔버스 프레임
        canvas_frame = QFrame()
        canvas_layout = QVBoxLayout()
        self.canvas = Canvas()
        canvas_layout.addWidget(self.canvas)
        canvas_frame.setLayout(canvas_layout)
        canvas_frame.setFrameShape(QFrame.StyledPanel)
        
        top_layout.addWidget(canvas_frame)

        # 글자 버튼 프레임
        letters_frame = QFrame()
        letters_layout = QVBoxLayout()
        letters_layout.setAlignment(Qt.AlignTop)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        letter_groups = [ascii_uppercase[i:i+4] for i in range(0, len(ascii_uppercase), 4)]
        for row, group in enumerate(letter_groups):
            for col, letter in enumerate(group):
                btn = QPushButton(f" {letter} ")
                btn.setFixedSize(50, 50)
                btn.setStyleSheet("font: 20px Courier; border: none; background-color: {}".format(
                    self.palette().color(self.backgroundRole()).name()))
                btn.clicked.connect(self.letter_clicked)
                btn.setObjectName(f"letter-{letter}")
                grid_layout.addWidget(btn, row, col)
        
        letters_layout.addLayout(grid_layout)
        letters_frame.setLayout(letters_layout)
        letters_frame.setFrameShape(QFrame.StyledPanel)
        
        top_layout.addWidget(letters_frame)

        main_layout.addLayout(top_layout)

        # 추측한 단어 표시 프레임
        guessed_word_frame = QFrame()
        guessed_word_layout = QVBoxLayout()
        self.display_word = QLabel("")
        self.display_word.setAlignment(Qt.AlignCenter)
        self.display_word.setStyleSheet("font: 20px Courier;")
        guessed_word_layout.addWidget(self.display_word)
        guessed_word_frame.setLayout(guessed_word_layout)
        guessed_word_frame.setFrameShape(QFrame.StyledPanel)
        
        main_layout.addWidget(guessed_word_frame)

        # 액션 버튼 프레임
        action_buttons_frame = QFrame()
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.addStretch(1)
        
        btn_new = QPushButton("New")
        btn_new.setFixedSize(100, 50)
        btn_new.setStyleSheet("font: 20px;")
        btn_new.clicked.connect(self.new_game)
        action_buttons_layout.addWidget(btn_new)
        
        action_buttons_layout.addSpacing(60)
        
        btn_restart = QPushButton("Restart")
        btn_restart.setFixedSize(100, 50)
        btn_restart.setStyleSheet("font: 20px;")
        btn_restart.clicked.connect(self.restart_game)
        action_buttons_layout.addWidget(btn_restart)
        
        action_buttons_layout.addSpacing(60)
        
        btn_quit = QPushButton("Quit")
        btn_quit.setFixedSize(100, 50)
        btn_quit.setStyleSheet("font: 20px;")
        btn_quit.clicked.connect(self.close)
        action_buttons_layout.addWidget(btn_quit)
        
        action_buttons_layout.addStretch(1)
        action_buttons_frame.setLayout(action_buttons_layout)
        action_buttons_frame.setFrameShape(QFrame.StyledPanel)
        
        main_layout.addWidget(action_buttons_frame)

        self.setLayout(main_layout)
        self.setFixedSize(self.sizeHint())

    def letter_clicked(self):
        button = self.sender()
        if button:
            letter = button.text().strip()
            print(f"클릭된 글자: {letter}")  # 실제 게임 로직을 위한 자리 표시자
            button.setEnabled(False)
            # 여기에 추측한 글자를 처리하는 로직을 추가하세요

    def new_game(self):
        print("새 게임 시작")  # 실제 게임 로직을 위한 자리 표시자
        # 게임 상태를 초기화하세요

    def restart_game(self):
        print("게임 재시작")  # 실제 게임 로직을 위한 자리 표시자
        # 현재 게임을 재시작하세요

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Hangman()
    sys.exit(app.exec_())
