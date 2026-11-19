from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class AboutPage(QMainWindow):                                   # Main window callout
    def closeEvent(self, event):
        event.accept()

    def __init__(self):
        super().__init__()

        window_icon = "images/win_icon.jpg"                     # App icon filepath
        logo = "images/coinhub.png"

        self.setWindowTitle("About Us")                         # Line 16-19: Window initialization
        self.setStyleSheet("background-color: black;")
        self.setWindowIcon(QIcon(window_icon))
        self.setGeometry(700, 100, 360, 700)

        self.def_width = 360                                    # Get window default geometry
        self.def_height = 700


        self.contentText = QLabel(self)                         # Line 25-43: Screen main content
        self.contentText.setGeometry(15, 100, 330, 380)
        self.contentText.setAlignment(Qt.AlignCenter)
        self.contentText.setText("\nCoin hub Group\n"
                                 "Leader: Ashlee Garcia\n"
                                 "Researcher: Carl Mananquil\n\n"
                                 "Frontend Developers:\n"
                                 "- Kean Dayrit\n"
                                 "- Justine Isada\n\n"
                                 "Backend Developers:\n"
                                 "- Arbie Basilio\n"
                                 "- Justine Manio")

        self.contentText.setStyleSheet("background-color: rgb(30, 30, 30);"
                                       "font-size: 15px;"
                                       "font-family: Trebuchet MS;"
                                       "font-weight: bold;"
                                       "color: lightgray;"
                                       "border-radius: 7px;")

        self.titleText = QLabel("About Us", self)               # Title Label
        self.titleText.setGeometry(-20, 10, 380, 80)
        self.titleText.setAlignment(Qt.AlignCenter)
        self.titleText.setParent(self.contentText)
        self.titleText.setStyleSheet("background: transparent;"
                                     "color: yellow;"
                                     "font-size: 30px;"
                                     "font-family: sans-serif;"
                                     "font-weight: bold;")

        self.line1 = QLabel(self)                               # Line 55-63: Two horizontal lines on top and bottom (for design only)
        self.line1.setGeometry(0, 0, 380, 60)
        self.line1.setStyleSheet("background: transparent;"
                                 "border-bottom: 1px solid lightgray;")

        self.line2 = QLabel(self)
        self.line2.setGeometry(0, 630, 380, 60)
        self.line2.setStyleSheet("background: transparent;"
                                 "border-top: 1px solid lightgray;")

        self.footer = QLabel("© 2025-2026 BSIT 3I. All rights reserved.",self)  # Copyright Content
        self.footer.setGeometry(-10, 640, 380, 50)
        self.footer.setAlignment(Qt.AlignCenter)
        self.footer.setStyleSheet("color: lightgray;"
                                  "background: transparent;"
                                  "font-family: Trebuchet MS;"
                                  "font-size: 12px;")


        self.fakeLbl = QLabel(self)                     # Line 74-83: Coinhub logo
        self.fakeLbl.setGeometry(78, 515, 195, 70)
        self.fakeLbl.setStyleSheet("background: transparent;"
                                   f"image: url('{logo}') 0 0 0 0 stretch stretch;"
                                   "color: lightgray;"
                                   "font-weight: bold;"
                                   "font-size: 35px;"
                                   "font-weight: bold;"
                                   "font-family: Segoe UI;"
                                   "padding-bottom: 3px;")



        self.backButt = QPushButton("x", self)                  # Back button to close the window
        self.backButt.setGeometry(320, 10, 28, 32)
        self.backButt.clicked.connect(self.backButt_onClick)
        self.backButt.setStyleSheet("""
                                    QPushButton {color: lightgray;
                                        font-size: 40px;
                                        font-family: Arial;
                                        font-weight: bold;
                                        background: transparent;}
                                    QPushButton:hover {
                                        color: rgb(170,170,170);
                                        font-size: 37px;}
                                    QPushButton:pressed {                                    
                                        color: rgb(130,130,130);
                                        font-size: 34px;
                                        }""")


        self.elements = [(self.line1, self.line1.geometry()),   # Get all elements in this page to resize them on window resize event
                         (self.line2, self.line2.geometry()),
                         (self.footer, self.footer.geometry()),
                         (self.backButt, self.backButt.geometry()),
                         (self.contentText, self.contentText.geometry()),
                         (self.titleText, self.titleText.geometry()),
                         (self.fakeLbl, self.fakeLbl.geometry())]



    def backButt_onClick(self):                                 # Callout when Back button is triggered
        self.close()



    def resizeEvent(self, event):                               # Function to resize all elements according to window resize changes event
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