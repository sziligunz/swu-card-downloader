from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QComboBox, QProgressBar, QLabel
from PyQt6.QtCore import QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal, Qt
import sys
import new_tech as BusinessLogic

class WorkerSignals(QObject):
    finished = pyqtSignal()


class DownloadWorker(QRunnable):
    def __init__(self, combo_box: QComboBox, progress_bar: QProgressBar, label: QLabel):
        super().__init__()
        self.signals = WorkerSignals()
        self.is_running = True
        self.combo_box = combo_box
        self.progress_bar = progress_bar
        self.label = label

    @pyqtSlot()
    def run(self):
        count = 0
        steps = BusinessLogic.download_images(self.combo_box.currentText().lower())
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(next(steps))
        while (step := next(steps, None)) is not None and self.is_running:
            count += 1
            self.progress_bar.setValue(count)
            self.label.setText("Processing: {}".format(step))
            QApplication.processEvents()

    def stop(self):
        self.is_running = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("It's Time To Steal")
        self.setMinimumSize(500, 300)

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        combo_box = QComboBox()
        combo_box.addItems([x.upper() for x in BusinessLogic.Config.SETS])
        vbox.addWidget(combo_box)
        button = QPushButton("Download")
        button.setFixedWidth(150)
        button.clicked.connect(lambda : self.start_download(combo_box, progress_bar, label))
        vbox.addWidget(button)
        progress_bar = QProgressBar()
        progress_bar.setFixedWidth(300)
        vbox.addWidget(progress_bar)
        label = QLabel()
        label.setFixedWidth(400)
        vbox.addWidget(label)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.threadpool = QThreadPool()
        self.workers = []
    
    def start_download(self, combo_box: QComboBox, progress_bar: QProgressBar, label: QLabel):
        download_worker = DownloadWorker(combo_box, progress_bar, label)
        self.workers.append(download_worker)
        self.threadpool.start(download_worker)

    def closeEvent(self, event):
        self._stopped = True
        for worker in self.workers:
            worker.stop()
        self.threadpool.waitForDone()
        event.accept()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
