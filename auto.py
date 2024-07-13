import sys
import threading
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QPalette
import keyboard
from pynput.mouse import Button, Controller

class AutoClicker:
    def __init__(self, delay, button):
        self.delay = delay
        self.button = button
        self.running = False
        self.click_thread = None
        self.mouse = Controller()

    def start_clicking(self):
        self.running = True
        self.click_thread = threading.Thread(target=self.click)
        self.click_thread.start()

    def stop_clicking(self):
        self.running = False
        if self.click_thread:
            self.click_thread.join()

    def click(self):
        while self.running:
            start_time = time.perf_counter()
            self.mouse.press(self.button)
            self.mouse.release(self.button)
            elapsed_time = time.perf_counter() - start_time
            sleep_time = max(0, self.delay - elapsed_time)
            time.sleep(sleep_time)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Arruenclicker')
        self.setGeometry(100, 100, 400, 300)

        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-size: 14px;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)

        layout = QVBoxLayout()
        
        self.label = QLabel('"f" tuşuna basarak aç/kapa yapabilirsiniz "q" tuşuna basarsanız kapanır.')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.start_button = QPushButton('Başlat')
        self.start_button.clicked.connect(self.start_clicking)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Durdur')
        self.stop_button.clicked.connect(self.stop_clicking)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.autoclicker = AutoClicker(0.04, Button.left) 

        # Add hotkeys
        keyboard.add_hotkey('f', self.toggle_clicking)
        keyboard.add_hotkey('q', self.close_program)


        self.leans_label = QLabel('Leans', self)
        self.leans_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.leans_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.leans_label.setStyleSheet("color: white;")
        self.leans_label.setGeometry(self.width() - 90, 10, 80, 40)  

        self.rgb_timer = QTimer(self)
        self.rgb_timer.timeout.connect(self.update_color)
        self.rgb_timer.start(50)  

        self.color_index = 0
        self.colors = [
            QColor(255, 255, 255), QColor(192, 192, 192), QColor(128, 128, 128),
            QColor(64, 64, 64), QColor(32, 32, 32), QColor(0, 0, 0)
        ]

    def update_color(self):
        self.color_index = (self.color_index + 1) % len(self.colors)
        color = self.colors[self.color_index]
        palette = self.leans_label.palette()
        palette.setColor(QPalette.WindowText, color)
        self.leans_label.setPalette(palette)

    def resizeEvent(self, event):
        self.leans_label.setGeometry(self.width() - 90, 10, 80, 40)
        super().resizeEvent(event)

    def start_clicking(self):
        self.autoclicker.start_clicking()

    def stop_clicking(self):
        self.autoclicker.stop_clicking()

    def toggle_clicking(self):
        if self.autoclicker.running:
            self.stop_clicking()
        else:
            self.start_clicking()

    def close_program(self):
        self.autoclicker.stop_clicking()
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
