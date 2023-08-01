from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel, QSlider, QSpinBox
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import json
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.current_video = 0
        self.videos = ['/home/shonsk/Downloads/1.mp4','/home/shonsk/Downloads/2.mp4']
        self.ratings = {video: 0 for video in self.videos}

        self.layout = QVBoxLayout()

        self.player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)

        self.player.setVideoOutput(self.video_widget)
        self.play_video()

        self.rating_slider = QSlider(Qt.Horizontal)
        self.rating_slider.setRange(1, 10)
        self.layout.addWidget(self.rating_slider)

        self.rating_spinbox = QSpinBox()
        self.rating_spinbox.setRange(1, 10)
        self.layout.addWidget(self.rating_spinbox)

        self.rating_slider.valueChanged.connect(self.rating_spinbox.setValue)
        self.rating_spinbox.valueChanged.connect(self.rating_slider.setValue)

        self.next_button = QPushButton("Next Video")
        self.next_button.clicked.connect(self.next_video)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)

    def play_video(self):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.videos[self.current_video])))
        self.player.play()

    def next_video(self):
        self.ratings[self.videos[self.current_video]] = self.rating_slider.value()

        if self.current_video + 1 < len(self.videos):
            self.current_video += 1
            self.rating_slider.setValue(1)
            self.rating_spinbox.setValue(1)
            self.play_video()
        else:
            print("All videos have been rated. Ratings:", self.ratings)
            self.player.stop()
            with open('ratings.json', 'w') as json_file:  # Open the file in write mode
                json.dump(self.ratings, json_file)
app = QApplication([])

window = MainWindow()
window.show()

app.exec_()
