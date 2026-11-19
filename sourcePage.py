from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class SourcePage(QMainWindow):                                  # Main Window callout
    def closeEvent(self, event):                                # Signal will be sent to its caller to identify its closing state
        event.accept()

    def __init__(self):
        super().__init__()

        window_icon = "images/win_icon.jpg"                     # File location for icon
        logo = "images/coinhub.png"

        self.setWindowTitle("Source")                           # Line 16-19: Window layout initialization
        self.setWindowIcon(QIcon(window_icon))
        self.setStyleSheet("background-color: black;")
        self.setGeometry(700, 100, 360, 700)

        self.def_width = 360                                    # Getting screen original geometry
        self.def_height = 700


        self.contentText = QLabel("API source URL:\nhttps://api.currencyfreaks.com/v2.0/rates/", self)
        self.contentText.setGeometry(15, 120, 330, 200)         # Line 26-33: Main content label text
        self.contentText.setAlignment(Qt.AlignCenter)
        self.contentText.setStyleSheet("background-color: lightgray;"
                                       "font-size: 15px;"
                                       "font-family: Trebuchet MS;"
                                       "font-weight: bold;"
                                       "color: black;"
                                       "border-radius: 7px;")


        self.line1 = QLabel(self)                               # Line 36-44: two horizontal lines on top and bottom(for design only)
        self.line1.setGeometry(0, 0, 380, 60)
        self.line1.setStyleSheet("background: transparent;"
                                 "border-bottom: 1px solid lightgray;")

        self.line2 = QLabel(self)
        self.line2.setGeometry(0, 630, 380, 60)
        self.line2.setStyleSheet("background: transparent;"
                                 "border-top: 1px solid lightgray;")


        self.fakeLbl = QLabel(self)                     # Line 47-56: Coinhub logo
        self.fakeLbl.setGeometry(78, 420, 195, 70)
        self.fakeLbl.setStyleSheet("background: transparent;"
                                    f"image: url('{logo}') 0 0 0 0 stretch stretch;"
                                    "color: lightgray;"
                                    "font-weight: bold;"
                                    "font-size: 35px;"
                                    "font-weight: bold;"
                                    "font-family: Segoe UI;"
                                    "padding-bottom: 3px;")



        self.backButt = QPushButton("x", self)                  # Back button to close/terminate the current window(this window)
        self.backButt.setGeometry(320, 10, 28, 32)
        self.backButt.clicked.connect(self.backButt_onClick)
        self.backButt.setStyleSheet("""
                                    QPushButton {
                                        color: lightgray;
                                        font-size: 40px;
                                        font-family: Arial;
                                        font-weight: bold;
                                        background: transparent;
                                        }
                                    QPushButton:hover {
                                        color: rgb(170,170,170);
                                        font-size: 37px;
                                        }
                                    QPushButton:pressed {                                    
                                        color: rgb(130,130,130);
                                        font-size: 34px;
                                        }""")


        self.footer = QLabel(self)                              # Disclaimer text
        self.footer.setGeometry(0, 632, self.width(), 67)
        self.footer.setAlignment(Qt.AlignCenter)
        self.footer.setText("Disclaimer! We do not claim ownership of the API\n"
                            "nor the images used in this project.\n"
                            "All rights remain on their respective owners.")
        self.footer.setStyleSheet("color: lightgray;"   
                                  "background: transparent;"
                                  "font-family: Trebuchet MS;"
                                  "font-size: 11px;"
                                  "font-weight: bold;")



        self.elements = [(self.line1, self.line1.geometry()),   # Collects all elements to resize them later
                         (self.line2, self.line2.geometry()),
                         (self.backButt, self.backButt.geometry()),
                         (self.contentText, self.contentText.geometry()),
                         (self.fakeLbl, self.fakeLbl.geometry()),
                         (self.footer, self.footer.geometry())]



    def backButt_onClick(self):                                 # Callout when Back button is triggered
        self.close()



    def resizeEvent(self, event):                               # Collects all elements and resize them and re-arrange them according to screen size changes
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