from PyQt5.QtWidgets import QLabel, QPushButton, QMainWindow
from PyQt5.QtGui import QMovie, QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from API_main import get_currency_data as callback


class FrameGif(QLabel):                                                     # GIF image initialization
    def __init__(self, gif_frame):
        super().__init__()
        self.bgc = 'black'                                                  # This belongs to a hidden feature discontinued due to logical complexity or developers' brain is not yet ready for it
        self.setStyleSheet(f"background-color: {self.bgc};")
        self.setGeometry(0, 15, 360, 280)

        self.clipFile = QMovie(gif_frame)                                   # Initializing an element property type
        self.clipFile.frameChanged.connect(self.colorInvert)
        self.clipFile.start()

    def colorSwitch(self):                                                  # For color inversion
        self.bgc = 'white' if self.bgc == 'black' else 'black'
        self.setStyleSheet(f"background-color: {self.bgc};")

    def colorInvert(self):                                                  # GIF image color inversion
        frame = self.clipFile.currentPixmap().toImage()
        if self.bgc == 'black':
            frame.invertPixels()

        self.setPixmap(QPixmap.fromImage(frame).scaled(self.width(),
                                                       self.height(),
                                                       Qt.KeepAspectRatio,
                                                       Qt.SmoothTransformation))

    def resizeEvent(self, event):                                           # Resizing the GIF image according to window resize event
        self.clipFile.setScaledSize(self.size())

        if self.clipFile.currentPixmap():
            self.colorInvert()

        super().resizeEvent(event)


class ErrorPage(QMainWindow):                                               # Main Window callout
    invertSignal = pyqtSignal()
    def closeEvent(self, event):                                            # Send signal to caller when closing
        event.accept()

    def __init__(self):
        super().__init__()

        window_icon = "images/win_icon.jpg"                                 # Initializing files filepath
        error_icon = "images/404_err.gif"

        self.bgc = 'black'                                                  # Initial window background and elements color such as elements background color and fonts color
        self.bgf = 'lightgray'

        self.setWindowTitle("Error")                                        # Initializing window property
        self.setStyleSheet(f"background-color: {self.bgc};")
        self.setWindowIcon(QIcon(window_icon))
        self.setGeometry(700, 100, 360, 700)

        self.def_width = 360                                                # Getting window base geometry
        self.def_height = 700

        self.win = FrameGif(error_icon)                                     # Line 63-65: Calling and showing GIF image
        self.win.setParent(self)
        self.win.show()


        self.invertSignal.connect(self.win.colorSwitch)                     # An invert color signal that will be sent to class FrameGif to match other elements color changes


        self.invButt = QPushButton(self)                                    # A button to trigger color light and dark switch
        self.invButt.setGeometry(320, 10, 28, 32)
        self.invButt.clicked.connect(self.invButt_onClick)
        self.invButt.setStyleSheet(f"""
                                    color: {self.bgf};
                                    font-size: 40px;
                                    font-family: Arial;
                                    font-weight: bold;
                                    background: transparent;
                                    """)


        self.error_message = QLabel(self)                                   # Error message that contains possible reason for the error
        self.error_message.setText("An error has occurred\n"
                                   "Possible cause:\n"
                                   "- No internet connection\n"
                                   "- Invalid URL\n"
                                   "- Server is unreachable\n"
                                   "- Invalid or expired API key")
        self.error_message.setGeometry(0, 270, 360, 360)
        self.error_message.setAlignment(Qt.AlignCenter)

        self.error_title = QLabel("404 Error", self)                        # A title showing 404 Error.
        self.error_title.setGeometry(-40, 296, self.width() + 100, 80)
        self.error_title.setAlignment(Qt.AlignCenter)

        self.refresh_button = QPushButton("Reload", self)                   # To refresh page/to try making another request on API
        self.refresh_button.setGeometry(95, 600, 180, 40)
        self.refresh_button.clicked.connect(self.reload_page)
        self.refresh_button.setStyleSheet(f"""
                                            QPushButton {{
                                                background-color: {self.bgc};
                                                color: {self.bgf};
                                                border: 1px solid {self.bgf};
                                                font-size: 18px;
                                                font-family: Arial;
                                                border-radius: 20px;
                                                }}
                                            QPushButton:hover {{
                                                background-color: rgb(40,40,40);
                                                }}""")


        self.progress_label = QLabel("",self)
        self.progress_label.setGeometry(110, 540, 150, 40)
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet(f"""
                                              background: transparent;
                                              color: {self.bgf};
                                              font-size: 18px;
                                              font-family: Arial;
                                              """)

        self.update_styles()                                                # This is to update elements style specifically their colors


        self.elements = [                                                   # Collection of all elements for resize event
            (self.error_message, self.error_message.geometry()),
            (self.error_title, self.error_title.geometry()),
            (self.invButt, self.invButt.geometry()),
            (self.win, self.win.geometry()),
            (self.refresh_button, self.refresh_button.geometry()),
            (self.progress_label, self.progress_label.geometry())]



    def reload_page(self):                                                  # Callout when Reload button is triggered
        self.refresh_button.setDisabled(True)                               # Temporarily disable the reload button to prevent spam and making multiple request that may cause DOS(Denial of Service) due to system overload
        print("Attempting to reload page")
        def update_label_load():
            step = [("Reloading.", 1000),                                   # These are for visual message effects only
                    ("Reloading..", 1000),
                    ("Reloading...", 1000),
                    ("Reloading.", 1000),
                    ("Reloading..", 1000),
                    ("Reloading...", 1000),
                    ("Failed to reload.", 2500),
                    ("", 0)]

            def update_text(index):                                         # Update the text every after delay
                if index < len(step):
                    self.progress_label.setText(step[index][0])
                    QTimer.singleShot(step[index][1], lambda: update_text(index + 1))

                    if index == 4:
                        try:
                            data = callback()                               # Starts making a new request on API while on index 4
                            if "status" in data and data['status'] == "404Error":        # Check if returned data is valid
                                print("Failed to fetch data")

                            else:
                                self.close()                                # If returned data is valid, then this window will close and open the Home Page

                        except:
                            print("Aray KOOooo")                            # Not really necessary but this is crucial for debugging XD

                else:
                    self.refresh_button.setDisabled(False)                  # After the index cycle is over and data collected

            update_text(0)                                                  # To loop cycle until last index

        update_label_load()



    def update_styles(self):                                                # Function call to change some elements color properties
        self.progress_label.setStyleSheet(f"""
                                              background: transparent;
                                              color: {self.bgf};
                                              font-size: 18px;
                                              font-family: Arial;
                                              """)

        self.setStyleSheet(f"background-color: {self.bgc};")

        self.invButt.setStyleSheet(f"""
                                    color: {self.bgf};
                                    font-size: 40px;
                                    font-family: Arial;
                                    font-weight: bold;
                                    background: transparent;
                                    """)

        self.error_message.setStyleSheet(f"""
                                        background: transparent;
                                        color: {self.bgf};
                                        font-size: 15px;
                                        font-family: Trebuchet MS;
                                        font-weight: bold;
                                        padding: 50%;
                                        """)

        self.error_title.setStyleSheet(f"""
                                        background: transparent;
                                        border-top: 2px solid {self.bgf};
                                        color: {self.bgf};
                                        font-size: 50px;
                                        font-family: Trebuchet MS;
                                        padding: 100%;
                                        """)



    def invButt_onClick(self):                                              # This is for color inversion event when Invert button is triggered
        self.bgc = 'white' if self.bgc == 'black' else 'black'
        self.bgf = 'black' if self.bgc == 'white' else 'lightgray'

        if self.bgc == 'white':
            self.refresh_button.setStyleSheet(f"""
                                                  QPushButton {{
                                                      background-color: rgb(230,230,230);
                                                      color: {self.bgf};
                                                      border: 1px solid {self.bgf};
                                                      font-size: 18px;
                                                      font-family: Arial;
                                                      border-radius: 20px;
                                                      }}
                                                  QPushButton:hover {{
                                                      background-color: rgb(210,210,210);
                                                      }}""")

        else:
            self.refresh_button.setStyleSheet(f"""
                                                  QPushButton {{
                                                      background-color: {self.bgc};
                                                      color: {self.bgf};
                                                      border: 1px solid {self.bgf};
                                                      font-size: 18px;
                                                      font-family: Arial;
                                                      border-radius: 20px;
                                                      }}
                                                  QPushButton:hover {{
                                                      background-color: rgb(40,40,40);
                                                      }}""")

        self.update_styles()
        self.invertSignal.emit()



    def resizeEvent(self, event):                                       # Will use collected list from self.elements and resize them according to window resize event changes
        w_scale = self.width() / self.def_width
        h_scale = self.height() / self.def_height

        for widget, geom in self.elements:
            new_x = int(geom.x() * w_scale)
            new_y = int(geom.y() * h_scale)
            new_w = int(geom.width() * w_scale)
            new_h = int(geom.height() * h_scale)

            widget.setGeometry(new_x, new_y, new_w, new_h)

            font = widget.font()
            font.setPointSizeF(max(8, 12 * min(w_scale, h_scale)))
            widget.setFont(font)

        super().resizeEvent(event)