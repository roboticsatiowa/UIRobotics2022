# importing libraries
# from secret_key import MAP_API_KEY
import os
import sys
import urllib.error
from urllib.request import urlretrieve

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QSlider, QInputDialog

from Rover import RoverTelemetry

MAP_API_KEY = "AIzaSyCOZPpgk37DJCQstaqwhI1Wmd09aE1R48k"


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Object contains data for rover telemetry
        self.rover = RoverTelemetry()

        # Temporary code. In the future these variables will contain rovers live location
        self.rover.pos.lat = 41.702389
        self.rover.pos.lon = -91.582108

        # no idea what this is for
        self.count = 0

        # coords of the robots target position
        self.target_lat = 41.702400
        self.target_lon = -91.582108

        # start flag
        self.isTimerRunning = False

        # set window paramenters and all components to the window
        self.setWindowTitle("Rover GUI")
        # self.setGeometry(1000, 1000, 1000, 800)
        self.initiate_widgets()
        self.showFullScreen()

    def get_map_image(self, lat, lng, zoom):
        urlbase = "https://maps.google.com/maps/api/staticmap?"

        # format API request parameters into the url arguments
        args = "center={},{}&zoom={}&size={}x{}&format=gif&maptype={}&markers=color:red|size:small|{}," \
               "{}&markers=color:blue|size:small|{},{}|&key={}".format(
            lat, lng, zoom, 400, 400, "satellite", lat, lng, self.target_lon, self.target_lat, MAP_API_KEY)

        # add http arguments to the end of the base url
        mapURL = urlbase + args

        # save API response to 'temp.png', convert to QPixmap object and then delete 'temp.png'
        try:
            urlretrieve(mapURL, 'temp.png')
            img = QPixmap('temp.png')
            os.remove('temp.png')
            return img
        except urllib.error.HTTPError as e:
            print("Failed to retrieve map image: {}".format(e))
            return None

    # method for widgets
    def set_video_frame(self, frame):
        pixmap = QPixmap(frame)
        smaller_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.camera1_widget.setPixmap(smaller_pixmap)
        self.camera1_widget.resize(400, 300)
        self.camera1_widget.move(50, 50)
        self.camera1_widget.show()

    def initiate_widgets(self):

        # left camera feed. currently displays map as placeholder image
        self.camera1_widget = QLabel(self)
        self.camera1_widget.setGeometry(50, 50, 400, 300)
        self.camera1_widget.setStyleSheet("border: 3px solid orange")
        self.camera1_widget.setPixmap(self.get_map_image(self.rover.pos.lat, self.rover.pos.lon, 12))

        # right camera feed. currently displays map as placeholer image
        self.camera2_widget = QLabel(self)
        self.camera2_widget.setGeometry(550, 50, 400, 300)
        self.camera2_widget.setStyleSheet("border: 3px solid orange")
        self.camera2_widget.setPixmap(self.get_map_image(self.rover.pos.lat, self.rover.pos.lon, 12))

        # GPS map frame. Display coordinates for lukes house on startup (for some reason)
        self.mapWidget = QLabel(self)
        self.mapWidget.setGeometry(700, 400, 250, 250)
        self.mapWidget.setStyleSheet("border: 3px solid orange")
        self.mapWidget.setPixmap(self.get_map_image(self.rover.pos.lat, self.rover.pos.lon, 12))

        # Visually contains timer controls within frame
        self.clockContainer = QLabel(self)
        self.clockContainer.setGeometry(320, 400, 340, 130)
        self.clockContainer.setStyleSheet("border : 3px solid orange")

        # creating label to show the seconds
        self.timerWidget = QLabel("00:00", self)
        self.timerWidget.setGeometry(330, 410, 320, 50)
        self.timerWidget.setStyleSheet("border : 3px solid black")
        self.timerWidget.setFont(QFont('Arial', 15))

        # creating start button
        self.startButton = QPushButton("Set", self)
        self.startButton.setGeometry(330, 470, 100, 50)
        self.startButton.clicked.connect(self.start_timer)

        # creating pause button
        self.pauseButton = QPushButton("Pause", self)
        self.pauseButton.setGeometry(440, 470, 100, 50)
        self.pauseButton.clicked.connect(self.pause_timer)

        # creating reset button
        self.resetButton = QPushButton("Reset", self)
        self.resetButton.setGeometry(550, 470, 100, 50)
        self.resetButton.clicked.connect(self.reset_timer)

        # creating a timer object
        timer = QTimer(self)
        # adding action to timer
        timer.timeout.connect(self.show_time)
        # update the timer every tenth second
        timer.start(100)

        # creating stop button
        stopButton = QPushButton("STOP ROVER", self)
        stopButton.setGeometry(50, 400, 200, 100)
        stopButton.clicked.connect(self.stop_action)

        # creating auto mode button
        autoButton = QPushButton("AUTO MODE", self)
        autoButton.setGeometry(50, 525, 200, 100)
        autoButton.clicked.connect(self.auto_action)

        # creating manual mode button
        manualButton = QPushButton("MANUAL MODE", self)
        manualButton.setGeometry(50, 650, 200, 100)
        manualButton.clicked.connect(self.manual_action)

        # creating latitude input text box
        latitudeButton = QPushButton("Set Latitude", self)
        latitudeButton.setGeometry(720, 670, 100, 50)
        latitudeButton.clicked.connect(self.get_latitude)
        latitudeButton.setFont(QFont('Arial', 11))

        # creating longitude input text box
        longitudeButton = QPushButton("Set Longitude", self)
        longitudeButton.setGeometry(825, 670, 100, 50)
        longitudeButton.clicked.connect(self.get_longitude)
        longitudeButton.setFont(QFont('Arial', 11))

        # creating latitude input text box
        latitudeButton2 = QPushButton("Set Latitude2", self)
        latitudeButton2.setGeometry(720, 720, 100, 50)
        latitudeButton2.clicked.connect(self.get_latitude)
        latitudeButton2.setFont(QFont('Arial', 11))

        # creating longitude input text box
        longitudeButton2 = QPushButton("Set Longitude2", self)
        longitudeButton2.setGeometry(825, 720, 100, 50)
        longitudeButton2.clicked.connect(self.get_longitude)
        longitudeButton2.setFont(QFont('Arial', 11))

        # Creating slider
        self.mapZoomSlider = QSlider(Qt.Horizontal, self)
        self.mapZoomSlider.setMinimum(1)
        self.mapZoomSlider.setMaximum(24)
        self.mapZoomSlider.setValue(12)
        self.mapZoomSlider.setTickPosition(QSlider.TicksBelow)
        self.mapZoomSlider.setTickInterval(1)
        self.mapZoomSlider.setGeometry(725, 640, 200, 50)
        self.mapZoomSlider.valueChanged.connect(self.slider_value_changed)

    # method called by stop button
    def stop_action(self):
        print("ROVER STOPPED")

    # method called by auto mode button
    def auto_action(self):
        print("ROVER IN AUTO MODE")

    # method called by manual mode button
    def manual_action(self):
        print("ROVER IN MANUAL MODE")

    # method called by timer
    def show_time(self):

        # checking if flag is true
        if self.isTimerRunning:
            self.startButton.setText("Running...")

            # decrementing the counter
            self.count -= 1

            # timer is completed
            if self.count == 0:
                # making flag false
                self.isTimerRunning = False

                # setting text to the label
                self.timerWidget.setText("Finished")

                # reset start button to it's og text
                self.startButton.setText("Set Time")

        if self.isTimerRunning:
            # getting text from count
            text = str(self.count / 10) + " s"

            # showing text
            self.timerWidget.setText(text)

    # slider value change method
    def slider_value_changed(self):
        GPSpixmap = self.get_map_image(self.rover.pos.lat, self.rover.pos.lon, self.mapZoomSlider.value())
        self.mapWidget.clear()
        self.mapWidget.setPixmap(GPSpixmap)

    def start_timer(self):
        # making flag true
        self.isTimerRunning = True

        # count = 0
        if self.count == 0:
            self.isTimerRunning = False
            second, done = QInputDialog.getInt(self, 'Seconds', 'Enter Seconds:', min=0)
            # if flag is true
            if done:
                # changing start button text to reflect it's ready to start counting
                self.startButton.setText("Start")
                # changing the value of count
                if second < 0:
                    self.count = second * -10
                else:
                    self.count = second * 10

                # setting text to the label

                self.timerWidget.setText(str(second))

    def pause_timer(self):

        # making flag false
        self.isTimerRunning = False
        self.startButton.setText("Start")

    def reset_timer(self):

        # making flag false
        self.isTimerRunning = False

        # setting count value to 0
        self.count = 0

        # setting label text
        self.timerWidget.setText("00:00")

        # reset start button text
        self.startButton.setText("Set Time")

    # ---- getter methods ----
    def get_seconds(self):

        # making flag false
        self.isTimerRunning = False

        # getting seconds and flag
        second, done = QInputDialog.getInt(self, 'Seconds', 'Enter Seconds:')

        # if flag is true
        if done:
            # changing the value of count
            self.count = second * 10

            # setting text to the label

            self.timerWidget.setText(str(second))

            # self.label.setText(str(hrs)+":"+str(mins)+":"+str(second))
            # self.label.setText(str(second))

    def get_latitude(self):
        self.latitude, ok = QInputDialog.getDouble(self, "Latitude", "Enter Latitude", self.latitude, -90, 90)
        if ok:
            self.getMapImage(self.latitude, self.longitude, self.mapZoomSlider.value())
            self.mapWidget.clear()
            GPSpixmap = QPixmap('googlemap.png')
            self.mapWidget.setPixmap(GPSpixmap)
        else:
            pass

    def get_longitude(self):
        self.longitude, ok = QInputDialog.getDouble(self, "Longitude", "Enter Longitude", self.longitude, -180, 180)
        if ok:
            self.getMapImage(self.latitude, self.longitude, self.mapZoomSlider.value())
            self.mapWidget.clear()
            GPSpixmap = QPixmap('googlemap.png')
            self.mapWidget.setPixmap(GPSpixmap)
        else:
            pass


def start_gui():
    # create pyqt5 app
    app = QApplication(sys.argv)

    # create the instance of our Window
    window = Window()

    # start the app
    app.exec_()


if __name__ == "__main__":
    start_gui()
