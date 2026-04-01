from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QComboBox, QProgressBar, QLabel
from PyQt6.QtCore import Qt
import sys
import new_tech as BusinessLogic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("It's Time To Steal")
        self.setMinimumSize(500, 300)

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        drop_down = QComboBox()
        drop_down.addItems([x.upper() for x in BusinessLogic.Config.SETS])
        vbox.addWidget(drop_down)
        button = QPushButton("Download")
        button.setFixedWidth(150)
        button.clicked.connect(lambda : self.start_download(drop_down, progress_bar, label))
        vbox.addWidget(button)
        progress_bar = QProgressBar()
        progress_bar.setFixedWidth(300)
        vbox.addWidget(progress_bar)
        label = QLabel()
        vbox.addWidget(label)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
    
    def start_download(self, combo_box: QComboBox, progress_bar: QProgressBar, label: QLabel):
        count = 0
        steps = BusinessLogic.download_images(combo_box.currentText().lower())
        progress_bar.setMaximum(next(steps))
        progress_bar.setValue(count)
        for step in steps:
            count += 1
            progress_bar.setValue(count)
            label.setText("Processing: {}".format(step))

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


