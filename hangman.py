import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QGridLayout,
    QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
)
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from string import ascii_uppercase
import random

class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 400)
        self.mistakes = 0  # 잘못된 추측 횟수
        
        # 스캐폴딩 (항상 보임)
        self.scaffolding = [
            ((40, 345), (180, 345), 10),  # 바닥
            ((165, 340), (165, 35), 10),  # 기둥
            ((160, 40), (100, 40), 10),   # 가로 지지대
            ((100, 35), (100, 96), 5),   # 줄
            ((100, 70), (100, 90), 1),    # 고리
        ]

        # 행맨 파트 (잘못된 추측에 따라 보임)
        self.hangman_parts = [
            ('circle', (100, 120), 20),          # 1. 머리 (원)
            ((100, 140), (100, 200), 5),         # 2. 몸통 (선)
            ((100, 150), (80, 170), 5),          # 3. 왼팔
            ((100, 150), (120, 170), 5),         # 4. 오른팔
            ((100, 200), (80, 240), 5),          # 5. 왼다리
            ((100, 200), (120, 240), 5),         # 6. 오른다리
        ]

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black)
        painter.setRenderHint(QPainter.Antialiasing)

        # 스캐폴딩 그리기 (항상 보임)
        for line in self.scaffolding:
            (x1, y1), (x2, y2), width = line
            pen.setWidth(width)
            painter.setPen(pen)
            painter.drawLine(x1, y1, x2, y2)
        
        # 행맨 그리기 (잘못된 추측 횟수에 따라 그리기)
        for i in range(self.mistakes):
            part = self.hangman_parts[i]
            if part[0] == 'circle':
                # 머리 그리기 (원)
                _, center, radius = part
                pen.setWidth(2)  # 원의 선 두께 설정
                painter.setPen(pen)
                x, y = center
                painter.drawEllipse(x - radius, y - radius, 2 * radius, 2 * radius)
            else:
                # 몸통, 팔, 다리 그리기 (선)
                (x1, y1), (x2, y2), width = part
                pen.setWidth(width)
                painter.setPen(pen)
                painter.drawLine(x1, y1, x2, y2)

        # 모든 파트가 그려졌을 때 GAME OVER 표시
        if self.mistakes >= len(self.hangman_parts):
            painter.setPen(QPen(Qt.red))
            font = painter.font()
            font.setPointSize(20)
            painter.setFont(font)

            # 텍스트를 중앙에 배치
            rect = self.rect()
            painter.drawText(rect, Qt.AlignCenter, "GAME OVER")
    
        painter.end()

    def update_hangman(self):
        # 행맨의 파트를 업데이트하고 다시 그리기
        if self.mistakes < len(self.hangman_parts):
            self.mistakes += 1
            self.update()
                

class Hangman(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hangman")
        self.word_to_guess = ""  # 추측할 단어
        self.guessed_letters = []  # 사용자가 추측한 글자들
        self.letter_buttons = []  # 글자 버튼을 관리할 리스트
        self.load_words()  # words.txt 파일에서 단어를 로드
        self.init_ui()  # UI 초기화
        self.restart_game()  # 새로운 게임 시작 (init_ui 이후에 호출)
        self.show()

    def load_words(self):
        try:
            with open("words.txt", "r") as f:
                self.words_list = [word.strip() for word in f.readlines()]
        except FileNotFoundError:
            print("Error: words.txt 파일을 찾을 수 없습니다.")
            self.words_list = []

    def select_random_word(self):
        if self.words_list:
            self.word_to_guess = random.choice(self.words_list).upper()
            self.guessed_letters = ["_"] * len(self.word_to_guess)
        else:
            self.word_to_guess = ""
            self.guessed_letters = []

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
                self.letter_buttons.append(btn)  # 버튼을 리스트에 추가
        
        letters_layout.addLayout(grid_layout)
        letters_frame.setLayout(letters_layout)
        letters_frame.setFrameShape(QFrame.StyledPanel)
        
        top_layout.addWidget(letters_frame)

        main_layout.addLayout(top_layout)

        # 추측한 단어 표시 프레임
        guessed_word_frame = QFrame()
        guessed_word_layout = QVBoxLayout()
        self.display_word = QLabel(" ".join(self.guessed_letters))
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
        
        btn_new = QPushButton("Restart")
        btn_new.setFixedSize(100, 50)
        btn_new.setStyleSheet("font: 20px;")
        btn_new.clicked.connect(self.restart_game)
        action_buttons_layout.addWidget(btn_new)
        
        action_buttons_layout.addSpacing(120)
        
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
            button.setEnabled(False)
            
            # 추측된 글자 업데이트
            if letter in self.word_to_guess:
                for i, char in enumerate(self.word_to_guess):
                    if char == letter:
                        self.guessed_letters[i] = letter
                self.display_word.setText(" ".join(self.guessed_letters))
            else:
                # 틀린 경우 캔버스 업데이트
                self.canvas.update_hangman()
            
            # 게임 종료 확인
            if "_" not in self.guessed_letters:
                print("축하합니다! 단어를 맞추셨습니다.")
            elif self.canvas.mistakes >= len(self.canvas.hangman_parts):
                print("GAME OVER")

    def restart_game(self):
        self.canvas.mistakes = 0
        self.select_random_word()
        self.display_word.setText(" ".join(self.guessed_letters))
        self.canvas.update()
        
        # 모든 버튼을 활성화
        for btn in self.letter_buttons:
            btn.setEnabled(True)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Hangman()
    sys.exit(app.exec_())
