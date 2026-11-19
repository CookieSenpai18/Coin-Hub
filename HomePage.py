import sys, json, os, inspect
from PyQt5.QtWidgets import QMainWindow, QApplication,QGraphicsOpacityEffect, QLabel, QPushButton, QWidget, QListWidgetItem, QListWidget, QAbstractItemView
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QThread, pyqtSignal
from aboutPage import AboutPage
from sourcePage import SourcePage
from error_404 import ErrorPage
from convertion_page import ConvertPage
from API_main import get_currency_data as calldata
from time import sleep

currency_data = dict()  # Main source of data collected from API
coinlist = ['USD', 'KRW', 'EGP', 'ILS', 'JMD', 'EUR', 'JPY', 'PHP', 'CAD', 'AUD', 'BRL']  # Initialization of available currencies


class Reloader(QThread):                            # Used to refresh the data (or making new request from API) every 5 mins
    finished = pyqtSignal(dict)                     # Will return the collected data in dictionary type

    def __init__(self, delay_seconds=300):          # Timer for 5 mins
        super().__init__()
        self.delay_seconds = delay_seconds
        self.running = True

    def run(self):                                  # Process of obtaining requests data
        global currency_data
        while self.running:
            print("Fetching data...")
            currency_data = calldata()              # Used to callout the API function
            self.finished.emit(currency_data)
            print(f"Data updated HomePage Line {inspect.currentframe().f_lineno}\n")
            sleep(self.delay_seconds)

    def stop(self):                                 # Will create an interval or rather stop the run() function after occurrence
        self.running = False



class MainWindow(QMainWindow):                      # The main user interface
    def __init__(self):
        super().__init__()

        window_icon = "images/win_icon.jpg"         # Line 42-47: Initialization of file paths for easy access
        mini_icon = "images/mini_icon.png"
        globe_icon = "images/globe_img.gif"
        logo = "images/coinhub.png"
        self.usable_data = "datas/usable_data.json"
        self.first_time = "datas/first_time.json"

        self.setGeometry(700, 100, 360, 700)        # Line 49-52: Main window initialization
        self.setWindowTitle("Coin Hub")
        self.setStyleSheet("background-color: black;")
        self.setWindowIcon(QIcon(window_icon))

        self.def_width = 360                        # Taking window height and width for other elements reference
        self.def_height = 700

        self.reload_data = Reloader()               # Activating auto refresh API requests
        self.reload_data.start()
        self.reload_data.finished.connect(self.task_finished)



        self.central_widget = QWidget()             # Line 63-70: Initialization of menu panel interface
        self.setCentralWidget(self.central_widget)
        self.panel_width = 200
        self.panel = QWidget(self)
        self.panel.setStyleSheet("background-color: black;"
                                 "border-right: 1px solid lightgray;")
        self.panel.setGeometry(-self.panel_width, 0, self.panel_width, self.height())
        self.panel_open = False

        self.cover = QLabel(self)                   # Line 72-78: Background blurr/darken effect when open
        self.cover.setGeometry(0, 0, self.width(), self.height())
        self.cover.setStyleSheet("background-color: rgb(5, 5, 5);")
        self.opacity = QGraphicsOpacityEffect()
        self.opacity.setOpacity(0.5)
        self.cover.setGraphicsEffect(self.opacity)
        self.cover.hide()

        self.img2 = QLabel(self)                    # Picture icon/logo
        self.img2.setParent(self.panel)
        self.img2.setGeometry(15, 30, 170, 150)
        self.img2.setStyleSheet(f"image: url('{mini_icon}') 0 0 0 0 stretch stretch;"
                                "border-radius: 5px;")

        self.minilabel1 = QLabel(self)      # Line 86-95: Coinhub logo on menu panel
        self.minilabel1.setParent(self.panel)
        self.minilabel1.setGeometry(23, 230, 150, 50)
        self.minilabel1.setAlignment(Qt.AlignCenter)
        self.minilabel1.setStyleSheet("background: transparent;"
                                      "font-size: 24px;"
                                      f"image: url('{logo}') 0 0 0 0 stretch stretch;"
                                      "border-right: 1px solid black;")

        self.aboutButt = QPushButton("About")       # About button initialization
        self.aboutButt.setParent(self.panel)
        self.aboutButt.setGeometry(25, 580, 150, 30)
        self.aboutButt.clicked.connect(self.aboutButt_onClick)          # Calling aboutButt_onClick function when triggered
        self.aboutButt.setStyleSheet("""
                                     QPushButton {
                                        background-color: black;
                                        border: 1px solid lightgray;
                                        font-family: Arial;
                                        font-size: 12px;
                                        font-weight: bold;
                                        color: white;
                                        border-radius: 15px;
                                        }
                                     QPushButton:hover {
                                        background-color: rgb(40,40,40);
                                        }
                                     QPushButton:pressed {
                                        background-color: rgb(20,20,20);
                                        }""")

        self.sourceButt = QPushButton("Source")     # Source button initialization
        self.sourceButt.setParent(self.panel)
        self.sourceButt.setGeometry(25, 630, 150, 30)
        self.sourceButt.clicked.connect(self.sourceButt_onClick)        # Calling sourceButt_onClick function when triggered
        self.sourceButt.setStyleSheet("""
                                     QPushButton {
                                        background-color: black;
                                        border: 1px solid lightgray;
                                        font-family: Arial;
                                        font-size: 12px;
                                        font-weight: bold;
                                        color: white;
                                        border-radius: 15px;
                                        }
                                     QPushButton:hover {
                                        background-color: rgb(40,40,40);
                                        }
                                     QPushButton:pressed {
                                        background-color: rgb(20,20,20);
                                        }""")



        self.navLine1 = QLabel(self)                # Line 139-147: these are the two horizontal lines on top and bottom of main screen (for design only)
        self.navLine1.setGeometry(0, 0, 360, 45)
        self.navLine1.setStyleSheet("background-color: black; color: lightgray;"
                                    "border-bottom: 1px solid lightgray;")

        self.navLine2 = QLabel(self)
        self.navLine2.setGeometry(0, 630, self.def_height, 50)
        self.navLine2.setStyleSheet("background-color: black; color: lightgray;"
                                    "border-top: 1px solid lightgray;")


        self.convButt = QPushButton("Convert",self)# Convert button initialization
        self.convButt.setGeometry(197, 640, 150, 50)
        self.convButt.clicked.connect(self.convButt_onClick)    # Calling convButt_onClick function if triggered
        self.convButt.setStyleSheet("""
                                    QPushButton {
                                        background-color: black;
                                        border-radius: 15px;
                                        color: lightgray;
                                        font-size: 13px;
                                        font-weight: bold;
                                        font-family: sans-serif;
                                        border: 2px solid lightgray;
                                        }
                                    QPushButton:hover {
                                        background-color: rgb(25, 25, 25);
                                        color: rgb(255, 255, 255);
                                        }""")


        self.clip_file = QMovie(globe_icon)        # Line 169-178: The Globe gif image in main screen

        self.front_image = QLabel(self)
        self.front_image.setMovie(self.clip_file)
        self.front_image.setGeometry(40, 65, 280, 240)
        self.front_image.setAlignment(Qt.AlignCenter)

        self.clip_file.setSpeed(400)
        self.clip_file.setScaledSize(self.front_image.size())
        self.clip_file.start()


        self.live_price = QLabel("Rates Basis: USD", self)              # Live price is canceled due to some unexpected discovery on API limitation
        self.live_price.setGeometry(13, 638, 170, 55)
        self.live_price.setStyleSheet("""
                                        background-color: black;
                                        border-radius: 7px;
                                        color: rgb(190, 190, 190);
                                        font-size: 17px;
                                        border: 2px solid green;
                                        padding: 5px;
                                        """)

        self.menuButt = QPushButton("≡", self)      # Menu button to open panel
        self.menuButt.setGeometry(10, 3, 28, 32)
        self.menuButt.clicked.connect(self.menuButt_onClick)
        self.menuButt.setStyleSheet("""
                                    QPushButton {
                                       color: lightgray; 
                                       font-size: 40px;
                                       }
                                    QPushButton:hover {
                                       color: rgb(180, 180, 180);
                                       font-size: 37px;
                                       }
                                    QPushButton:pressed {
                                       color: rgb(140, 140, 140);
                                       font-size: 34px;
                                       }""")


        self.list_coins = QListWidget(self)         # Line 210-229: Scrollable panel for available currencies
        self.list_coins.setGeometry(0, 330, self.width(), 300)
        self.list_coins.setSpacing(5)
        self.list_coins.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list_coins.setSelectionMode(QAbstractItemView.NoSelection)
        self.list_coins.setFocusPolicy(Qt.NoFocus)
        self.list_coins.setStyleSheet("""
                                    QListWidget{
                                       background: transparent;
                                       color: lightgray;
                                       border: none;
                                       padding: 15px;
                                       font-family: Arial;
                                       font-size: 19px;
                                       }
                                    QListWidget::item {
                                       border-bottom: 1px solid lightgray;
                                       padding-left: 20px;
                                       padding-bottom: 10px;
                                       }""")

        for coin in coinlist:                       # Initializing available currencies from global coinlist to scrollable panel
            QListWidgetItem(coin, self.list_coins)

        self.list_coins.setVerticalScrollBarPolicy(True)    # Hiding/disabling vertical scrollbar tooltip on right side of panel

        self.update_list()                          # Setting currencies data to scroll list items

        self.coin_tag = QLabel("Currency\t\tValue",self)# Just a label for user to identify the info about the displayed items on scroll list
        self.coin_tag.setGeometry(5, 315, self.width(), 30)
        self.coin_tag.setStyleSheet("background: transparent;"
                                    "padding-left: 20px;"
                                    "color: lightgray;"
                                    "font-family: Arial;"
                                    "font-weight: bold;"
                                    "font-size: 17px;")

        self.fakeLbl1 = QLabel(self)         # Line 247-256: Coinhub logo in main screen
        self.fakeLbl1.setGeometry(117, 2, 130, 40)
        self.fakeLbl1.setStyleSheet("background: transparent;"
                                    f"border-image: url('{logo}') 0 0 0 0 stretch stretch;"
                                    "color: white;"
                                    "font-weight: bold;"
                                    "font-size: 25px;"
                                    "font-weight: bold;"
                                    "font-family: Segoe UI;"
                                    "padding-bottom: 3px;")


        self.cover.raise_()                         # This is to override all elements or to send them behind making sure the blurr/darken effect of the menu panel is consistent


        self.tutorial_cover = QLabel(self)          # Line 262-268: Tutorial cover screen with more darker/lower opacity
        self.tutorial_cover.setGeometry(0, 0, self.width(), self.height())
        self.tutorial_cover.setStyleSheet("background-color: black;")
        self.tutorial_cover.hide()
        cover_opacity = QGraphicsOpacityEffect(self)
        cover_opacity.setOpacity(0.6)
        self.tutorial_cover.setGraphicsEffect(cover_opacity)

        self.next_button = QPushButton("Next",self) # Next Button to increment the tutorial progress
        self.next_button.setGeometry(260, 50, 100, 50)
        self.next_button.hide()
        self.next_button.setStyleSheet("""
                                    QPushButton {
                                        color: rgb(210, 210, 210);
                                        background-color: transparent;
                                        font-weight: bold;
                                        font-size: 23px;
                                        font-family: Arial;}
                                    QPushButton:hover {
                                        color: rgb(170, 170, 170);
                                        font-size: 22px;
                                        }
                                    QPushButton:pressed {
                                        color: rgb(120, 120, 120);
                                        font-size: 20px;
                                        }""")

        self.info_label = QLabel(self)              # Line 289-297: This is where the tutorial text is shown
        self.info_label.setGeometry(30, 100, 300, 200)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.hide()
        self.info_label.setStyleSheet("background: transparent;"
                                      "color: lightgray;"
                                      "font-weight: bold;"
                                      "font-family: Arial;"
                                      "font-size: 18px;")

        self.fake_cover = QLabel(self)              # Line 299-303: This is to prevent highlighted buttons to be interactable
        self.fake_cover.setGeometry(0, 0, self.width(), self.height())
        self.fake_cover.setStyleSheet("background: transparent;")
        self.fake_cover.lower()
        self.fake_cover.hide()

        self.arrow_menu = QLabel("🡸", self)        # To point out or highlight a specific element
        self.arrow_menu.setGeometry(40, -11, 65, 65)
        self.arrow_menu.hide()
        self.arrow_menu.setStyleSheet("background: transparent;"
                                      "color: rgb(200, 200, 0);"
                                      "font-size: 30px;"
                                      "font-weight: bold;")

        self.arrow_convert = QLabel("🡇",self)      # To point out or highlight a specific element
        self.arrow_convert.setGeometry(235, 577, 55, 55)
        self.arrow_convert.hide()
        self.arrow_convert.setStyleSheet("background: transparent;"
                                          "color: rgb(200, 200, 0);"
                                          "font-size: 70px;"
                                          "font-weight: bold;")

        if "status" not in currency_data:           # Check first if datas are successfully retrieved
            self.is_first_time()                    # Trigger tutorial function


        self.elements = [
            (self.fakeLbl1, self.fakeLbl1.geometry()),
            (self.convButt, self.convButt.geometry()),
            (self.front_image, self.front_image.geometry()),
            (self.live_price, self.live_price.geometry()),
            (self.navLine1, self.navLine1.geometry()),
            (self.navLine2, self.navLine2.geometry()),
            (self.menuButt, self.menuButt.geometry()),
            (self.minilabel1, self.minilabel1.geometry()),
            (self.cover, self.cover.geometry()),
            (self.aboutButt, self.aboutButt.geometry()),
            (self.sourceButt, self.sourceButt.geometry()),
            (self.img2, self.img2.geometry()),
            (self.panel, self.panel.geometry()),
            (self.list_coins, self.list_coins.geometry()),
            (self.coin_tag, self.coin_tag.geometry()),
            (self.arrow_menu, self.arrow_menu.geometry()),
            (self.arrow_convert, self.arrow_convert.geometry()),
            (self.fake_cover, self.fake_cover.geometry()),
            (self.tutorial_cover, self.tutorial_cover.geometry()),
            (self.info_label, self.info_label.geometry()),
            (self.next_button, self.next_button.geometry())]                       # Collection of all elements to allow them to stay in place even after window resize event



    def is_first_time(self):                        # Check if the user first time in the app
        if not os.path.exists(self.first_time):     # Check the file if exists, if not then will trigger start of tutorial
            self.tutorial()
        else:
            with open(self.first_time, "r") as f:   # If file exists then it will read it to check if the tutorial is finished else it will restart again upon reopening the app
                new_data = json.load(f)
                if "complete" not in new_data or new_data["complete"] == 0:
                    self.tutorial()



    def tutorial(self):                             # Main method for tutorial
        tutorial_index = 1
        text_script = ["Greetings! Dear user.",
                       "Before you proceed on using\nthis software. Allow me\nto introduce you the basics",
                       "This is the Menu button\nwhere you can find info about\nthis software.",
                       "This is a scrollable area where the\nlist of some currencies as\nwell as their current value shown",
                       "Press this button to\ncalculate exchange rates",
                       "That's all, for now."]      # Scripts used for tutorial stored in a list for easy indexing

        self.info_label.setText(text_script[0])     # Set the primary text of tutorial label from index 1
        self.fake_cover.show()                      # Line 370-378: for activating tutorial elements as well as their correct front/back arrangement
        self.info_label.show()
        self.tutorial_cover.show()
        self.next_button.show()
        self.arrow_menu.show()
        self.arrow_convert.show()
        self.arrow_menu.lower()
        self.arrow_convert.lower()

        def next_button_clicked():                  # Function call when Next button is triggered
            nonlocal tutorial_index
            if tutorial_index < len(text_script):
                self.info_label.setText(text_script[tutorial_index])    # This will update the text of label everytime Next button is clicked

            tutorial_index += 1                     # Increment the index by 1 when Next button is clicked
            match tutorial_index:                   # Actions that will occur in each specific index
                case 3:                             # Highlights Menu button
                    self.menuButt.raise_()
                    self.fake_cover.raise_()
                    self.arrow_menu.raise_()
                    self.next_button.raise_()

                case 4:                             # Highlights the scrollable area (list oF currencies)
                    self.arrow_menu.lower()
                    self.tutorial_cover.raise_()
                    self.info_label.raise_()
                    self.next_button.raise_()
                    self.list_coins.raise_()

                case 5:                             # Highlights the Convert button
                    self.tutorial_cover.raise_()
                    self.arrow_convert.raise_()
                    self.convButt.raise_()
                    self.fake_cover.raise_()
                    self.info_label.raise_()
                    self.next_button.raise_()

                case 6:
                    self.arrow_convert.lower()
                    self.tutorial_cover.raise_()
                    self.info_label.raise_()
                    self.next_button.raise_()

                case 7:                             # Closing event
                    self.tutorial_cover.hide()
                    self.fake_cover.hide()
                    self.next_button.hide()
                    self.info_label.hide()
                    self.cover.raise_()
                    with open(self.first_time, "w") as f:   # Create a file to mark the tutorial on this page complete
                        json.dump({"complete": 1}, f, indent=4)

        self.next_button.clicked.connect(next_button_clicked)



    def update_list(self):                          # Will update the scrollable list of currencies once called
        try:
            with open(self.usable_data, "r") as file:
                data = json.load(file)
                print(f"HomePage Line {inspect.currentframe().f_lineno}. Files loaded.")

                if "status" in data and data['status'] == "404Error":   # Checker if collected data is valid
                    print(f"HomePage Line {inspect.currentframe().f_lineno}. Error 404")

                else:
                    print(f"HomePage Line {inspect.currentframe().f_lineno}. Success launch")
                    ct = 0

                    for coin in coinlist:
                        self.list_coins.item(ct).setText(f"{coin} :\t\t{float(data[coin]):13.3f}")
                        ct += 1

        except:
            print(f"HomePage Line {inspect.currentframe().f_lineno}: Failed to update lists")



    def task_finished(self, data):                  # Checks if data retrieved is valid before opening main window else will be sent to error page
        try:
            if "status" in currency_data and currency_data["status"] == "404Error":
                self.error404_page()
                print(f"HomePage Line {inspect.currentframe().f_lineno}: Error 404")

            else:
                print("Data has been updated")
                self.update_list()

        except:
            print(f"Crap {inspect.currentframe().f_lineno}")



    def menuButt_onClick(self):                     # Menu panel logics open/close
        self.panel.raise_()

        w_scale = self.width() / self.def_width
        panel_width_scaled = int(self.panel_width * w_scale)

        animation = QPropertyAnimation(self.panel, b"geometry")
        animation.setDuration(300)

        if self.panel_open:                         # Closing Menu Panel
            self.cover.hide()
            animation.setStartValue(QRect(0, 0, panel_width_scaled, self.height()))
            animation.setEndValue(QRect(-panel_width_scaled, 0, panel_width_scaled, self.height()))

        else:                                       # Opening Menu Panel
            self.cover.show()
            animation.setStartValue(QRect(-panel_width_scaled, 0, panel_width_scaled, self.height()))
            animation.setEndValue(QRect(0, 0, panel_width_scaled, self.height()))

        animation.start()                           # Trigger the open/close of panel animation

        self.panel_open = not self.panel_open       # Switching between true and false each cycle
        self.animation = animation



    def mousePressEvent(self, event):               # Check if user clicked outside the Menu panel, it true then it will close the Menu panel
        if self.panel_open:
            if not self.panel.geometry().contains(event.pos()):
                self.menuButt_onClick()



    def error404_page(self):                        # Quick access for error page
        self.errorPg = ErrorPage()
        self.errorPg.setGeometry(self.geometry())
        self.errorPg.show()
        self.hide()

        def openMain(event):
            global currency_data
            if os.path.exists(self.usable_data):
                with open(self.usable_data, "r") as file:
                    data = json.load(file)
                    currency_data = data
            else:
                currency_data["status"] = "404Error"

            if "status" in currency_data and currency_data["status"] == "404Error":
                print(f"{inspect.currentframe().f_lineno} error")
                self.close()

            else:
                print(f"Success {inspect.currentframe().f_lineno}")
                self.setGeometry(self.errorPg.geometry())
                self.reload_data.start()
                self.show() 
                self.update_list()
                event.accept()

        print(f"HomePage Line {inspect.currentframe().f_lineno} error")
        self.errorPg.closeEvent = openMain
        print(f"HomePage Line {inspect.currentframe().f_lineno} error")



    def convButt_onClick(self):                     # Sends the page to Conversion page
        self.conv = ConvertPage()
        self.conv.setGeometry(self.geometry())
        self.conv.show()
        self.hide()

        def openMain(event):
            self.setGeometry(self.conv.geometry())
            self.show()
            event.accept()

        self.conv.closeEvent = openMain



    def aboutButt_onClick(self):                    # Sends the page to About page
        self.aboutPg = AboutPage()
        self.aboutPg.setGeometry(self.geometry())
        self.aboutPg.show()
        self.hide()

        def openMain(event):
            self.setGeometry(self.aboutPg.geometry())
            self.show()
            event.accept()

        self.aboutPg.closeEvent = openMain



    def sourceButt_onClick(self):                   # Sends the page to Source page
        self.sourcePg = SourcePage()
        self.sourcePg.setGeometry(self.geometry())
        self.sourcePg.show()
        self.hide()

        def openMain(event):
            self.setGeometry(self.sourcePg.geometry())
            self.show()
            event.accept()

        self.sourcePg.closeEvent = openMain



    def resizeEvent(self, event):                   # Will collect all elements from self.elements list and will resize/re-arrange them according to screen size changes
        self.clip_file.setScaledSize(self.front_image.size())
        w_scale = self.width() / self.def_width
        h_scale = self.height() / self.def_height

        for widget, geom in self.elements:
            if widget == self.panel:
                continue
            new_x = int(geom.x() * w_scale)
            new_y = int(geom.y() * h_scale)
            new_w = int(geom.width() * w_scale)
            new_h = int(geom.height() * h_scale)

            widget.setGeometry(new_x, new_y, new_w, new_h)

            font = widget.font()
            font.setPointSizeF(max(8, 12 * min(w_scale, h_scale)))
            widget.setFont(font)

        panel_width_scaled = int(self.panel_width * w_scale)
        current_x = 0 if self.panel_open else -panel_width_scaled
        self.panel.setGeometry(current_x, 0, panel_width_scaled, self.height())



if __name__ == '__main__':                          # To show and activate the main window as well as its functionalities
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())