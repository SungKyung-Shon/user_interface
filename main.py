from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel, QSlider, QSpinBox
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import json
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Please give us a score on how effective you think it is")

        self.current_video = 0
        self.videos = ['/home/sung/videos/recording0.mp4','/home/sung/videos/recording1.mp4','/home/sung/videos/rrecording2.mp4',
                       '/home/sung/videos/recording3.mp4','/home/sung/videos/recording4.mp4','/home/sung/videos/recording5.mp4',
                       '/home/sung/videos/recording6.mp4','/home/sung/videos/recording7.mp4','/home/sung/videos/recording8.mp4',
                       '/home/sung/videos/recording9.mp4'
                       ]
        self.ratings = {video: 0 for video in self.videos}

        self.layout = QVBoxLayout()

        self.player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)

        self.player.setVideoOutput(self.video_widget)

        self.rating_slider = QSlider(Qt.Horizontal)
        self.rating_slider.setRange(1, 10)
        self.layout.addWidget(self.rating_slider)

        self.rating_spinbox = QSpinBox()
        self.rating_spinbox.setRange(1, 10)
        self.layout.addWidget(self.rating_spinbox)

        self.rating_slider.valueChanged.connect(self.rating_spinbox.setValue)
        self.rating_spinbox.valueChanged.connect(self.rating_slider.setValue)

        self.pause_play_button = QPushButton("Pause")
        self.pause_play_button.clicked.connect(self.toggle_pause_play)
        self.layout.addWidget(self.pause_play_button)

        self.prev_button = QPushButton("Previous Video")
        self.prev_button.clicked.connect(self.prev_video)
        self.layout.addWidget(self.prev_button)

        self.replay_button = QPushButton("Replay")
        self.replay_button.clicked.connect(self.play_video)
        self.layout.addWidget(self.replay_button)

        self.next_button = QPushButton("Next Video")
        self.next_button.clicked.connect(self.next_video)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)

        self.player.mediaStatusChanged.connect(self.handle_media_status)

        self.play_video()
    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.next_button.setEnabled(True)
            self.rating_slider.setEnabled(True)
            self.rating_spinbox.setEnabled(True)
    def play_video(self):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.videos[self.current_video])))
        self.player.play()
        self.next_button.setEnabled(False)
        self.rating_slider.setEnabled(False)
        self.rating_spinbox.setEnabled(False)

    def toggle_pause_play(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.pause_play_button.setText("Play")
        else:
            self.player.play()
            self.pause_play_button.setText("Pause")

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

    def prev_video(self):
        if self.current_video > 0:
            self.current_video -= 1
            self.rating_slider.setValue(self.ratings[self.videos[self.current_video]])
            self.rating_spinbox.setValue(self.ratings[self.videos[self.current_video]])
            self.play_video()

app = QApplication([])

window = MainWindow()
window.show()

app.exec_()
