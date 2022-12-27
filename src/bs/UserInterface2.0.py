import sys
from time import sleep

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QFont, QPixmap
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QPushButton, QLabel, QInputDialog, QMessageBox, QGroupBox)

from IO_Controller import BaseStationSock


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        sockController = BaseStationSock(addr=('localhost', 50000))

        # set left and right layouts
        self.left = QVBoxLayout()
        self.right = QVBoxLayout()

        # right
        # create top video frame
        self.camera1 = QLabel("camera 1")
        self.camera1.setStyleSheet("border : 3px solid orange")
        self.camera1.setMaximumWidth(self.width() // 2)

        # create bottom video frame
        self.camera2 = QLabel("camera 1")
        self.camera2.setStyleSheet("border : 3px solid orange")
        self.camera2.setMaximumWidth(self.width() // 2)

        # left
        self.data = QPushButton("data")
        self.gps_map = QLabel("GPS")
        self.gps_map.setStyleSheet("border : 3px solid orange")

        self.gps_controls = QGroupBox("Test")

        self.left.addWidget(self.gps_map)
        self.left.addWidget(self.gps_controls)

        # add widgets to left and right layouts
        self.right.addWidget(self.camera1)
        self.right.addWidget(self.camera2)

        # set overall layout
        self.layout = QHBoxLayout()

        # self.table_view.setSizePolicy(size)
        self.layout.addLayout(self.left)
        self.layout.addLayout(self.right)

        # Set the layout to the QWidget
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.central_widget = widget

        # Set window parameters
        self.setWindowTitle("Robotics At Iowa")  # Window Title
        self.setWindowIcon(QPixmap("favicon.ico"))  # needs icon for maximum coolness
        self.setMinimumSize(720, 480)  # Cannot resize window to smaller than this

        # Create menu bar at top of the screen
        self.menu = self.menuBar()

        # Create menu dropdowns
        self.file_menu = self.menu.addMenu("File")
        self.view_menu = self.menu.addMenu("View")
        self.actions_menu = self.menu.addMenu("Actions")
        self.telemetry_menu = self.menu.addMenu("Status")
        self.telemetry_menu.setEnabled(False)

        # Create menu actions and add them to the dropdowns
        self.fill_menu_bar()

        self.setCentralWidget(widget)

    def fill_menu_bar(self):
        # ---- File ----
        # Exit with application
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+q")
        exit_action.triggered.connect(self.exit_app)

        # ---- View ----
        toggle_fullscreen_action = QAction("Toggle fullscreen", self)
        toggle_fullscreen_action.setShortcut("F11")
        toggle_fullscreen_action.triggered.connect(self.toggle_fullscreen)

        # ---- Actions ----
        # disconnect from rover
        disconnect_rover_action = QAction("Disconnect rover", self)
        disconnect_rover_action.triggered.connect(self.disconnect_rover)

        # Connect to the rover
        connect_rover_action = QAction("Connect rover", self)
        connect_rover_action.triggered.connect(self.connect_rover)

        # Change port number
        change_port_action = QAction("Port: 50000", self)
        # The lamba expression allows the callable function to passed with arguments
        change_port_action.triggered.connect(lambda: self.change_port(change_port_action))

        # change ip address
        change_ip_action = QAction("IP: 127.0.0.1")
        change_ip_action.triggered.connect(lambda: self.change_ip(change_ip_action))

        # Add all actions to appropriate menu dropdowns
        self.file_menu.addAction(exit_action)
        self.view_menu.addAction(toggle_fullscreen_action)
        self.actions_menu.addAction(connect_rover_action)
        self.actions_menu.addAction(disconnect_rover_action)
        self.actions_menu.addAction(change_port_action)
        self.actions_menu.addAction(change_ip_action)

    @Slot()
    def exit_app(self):
        QApplication.quit()

    @Slot()
    def connect_rover(self):
        print("WARNING: The following is a placeholder message, no action is being performed")
        print("Connecting to rover...")
        sleep(2)
        print("Connected!")
        self.telemetry_menu.setEnabled(True)

    @Slot()
    def disconnect_rover(self):
        print("WARNING: The following is a placeholder message, no action is being performed")
        print("Rover disconnected")

    @Slot()
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    @Slot()
    def change_port(self, qaction):

        # Get input from prompt
        text, ok = QInputDialog.getInt(self, "Change Port", "Enter new port number:", minValue=1024, maxValue=65536,
                                       value=50000)

        # only change port if Ok button is hit
        if ok:
            qaction.setText("Port: {}".format(text))

    @Slot()
    def change_ip(self, qaction):
        # Get input from prompt
        text, ok = QInputDialog.getText(self, "Change IP", "Enter new IP address:", text="192.168.0.0")

        # do nothing if cancel button was hit
        if not ok:
            return

        # check that the IP address is valid
        if [0 <= int(i) < 256 for i in text.split(".") if i.isnumeric()] != [True] * 4:
            QMessageBox.warning(self, "Warning", "Invalid IP address")
            return

        # update the menu option text
        qaction.setText("IP: {}".format(text))

    def resizeEvent(self, ev):
        self.central_widget.camera1.setMaximumWidth(self.width() // 2)
        self.central_widget.camera2.setMaximumWidth(self.width() // 2)


# checks if this file was ran as main (not imported by a different file)
# This isn't necessary here but is good practice in python to indicate the purpose of the code
if __name__ == '__main__':
    # Create application but don't run yet
    app = QApplication([])

    app.setFont(QFont("Helvetica", 10))

    widget = Widget()

    # Create main window and then show it to screen
    window = MainWindow(widget)
    window.show()

    # Run application and exit python program once PyQt application is terminated
    sys.exit(app.exec())
