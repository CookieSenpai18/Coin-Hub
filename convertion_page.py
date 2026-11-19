from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QComboBox, QListView, QGraphicsOpacityEffect
from PyQt5.QtGui import QDoubleValidator, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer
import json, os

# Initialization of commonly use variables
coin_data = {"KRW": 0, "EGP": 0, "ILS": 0, "JMD": 0, "EUR": 0, "JPY": 0, "PHP": 0, "CAD": 0, "AUD": 0, "BRL": 0}
primary_selection = float(1)
secondary_selection = float(1)
primary_index = 0
secondary_index = 1
tutorial_index = 1

# Main Window callout
class ConvertPage(QMainWindow):
    def closeEvent(self, event):        # Send signal to its caller to tell its about to close
        event.accept()

    def __init__(self):
        super().__init__()
    # Initialize files filepath
        window_icon = "images/win_icon.jpg"
        title_label = "images/label_icon.png"
        self.tutorial_path = "datas/first_time.json"

    # Initialize window properties
        self.setGeometry(700, 100, 360, 700)
        self.setWindowTitle("Exchanges")
        self.setWindowIcon(QIcon(window_icon))
        self.setStyleSheet("background-color: black;")

    # Get the base geometry of window
        self.def_width = 360
        self.def_height = 700


    # Line 36-52: Two horizontal lines on top and bottom (for design only)
        self.navLine1 = QLabel(self)
        self.navLine1.setGeometry(0, 0, 360, 70)
        self.navLine1.setStyleSheet("background-color: black;"
                                    "color: lightgray;"
                                    "border-bottom: 1px solid lightgray;")

        self.navLine2 = QLabel(self)
        self.navLine2.setGeometry(0, 630, self.def_height, 50)
        self.navLine2.setStyleSheet("background-color: black;"
                                    "color: lightgray;"
                                    "border-top: 1px solid lightgray;")

    # Title on top window showing 'CURRENCY CONVERSION'
        self.titleLabel = QLabel(self)
        self.titleLabel.setGeometry(10, 5, self.width() - 20, 55)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("background: transparent;"
                                      f"border-image: url('{title_label}');"
                                      "font-size: 30px;")

    # Back button to close the current page and return to Home Page
        self.backButt = QPushButton("x", self)
        self.backButt.setGeometry(325, 80, 28, 32)
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


    # Input field that only supports numerical inputs like int and double datatypes
        self.inputPrimary = QLineEdit(self)
        self.inputPrimary.setPlaceholderText("Amount")
        self.inputPrimary.setGeometry(20, 250, 130, 50)
        self.inputPrimary.setValidator(QDoubleValidator())
        self.inputPrimary.setStyleSheet("color: lightgray;"
                                        "border-radius: 9px;"
                                        "border: 1px solid lightgray;"
                                        "padding: 7px;")

    # Value indicator for selected currency
        self.primaryValue = QLabel("Value: 1.0",self)
        self.primaryValue.setGeometry(20, 162 + 50, 150, 50)
        self.primaryValue.setStyleSheet("color: lightgray;"
                                        "background: transparent;"
                                        "padding: 2px;"
                                        "font-size: 14px;")

    # Value indicator for selected conversion currency
        self.selectedValue = QLabel("Value: 1.0", self)
        self.selectedValue.setGeometry(200, 162 + 50, 150, 50)
        self.selectedValue.setStyleSheet("color: lightgray;"
                                         "background: transparent;"
                                         "padding: 2px;"
                                         "font-size: 14px;")

    # The computed result of user inputs according to selected currency and conversion currency
        self.convertedValue = QLabel("0.000 KRW",self)
        self.convertedValue.setGeometry(200, 250, 140, 50)
        self.convertedValue.setStyleSheet("color: lightgreen;"
                                          "border-radius: 9px;"
                                          "border: 1px solid lightgray;"
                                          "padding: 7px;"
                                          "font-size: 15px;")

    # Convert button to calculate user inputs
        self.convertButton = QPushButton("Calculate", self)
        self.convertButton.setGeometry(55, 370, 250, 60)
        self.convertButton.clicked.connect(self.calculateValues)
        self.convertButton.setStyleSheet("""
                                         QPushButton {
                                            color: lightgray;
                                            background-color: rgb(10, 10, 10);
                                            border: 1px solid lightgray;
                                            border-radius: 25px;
                                            font-family: Arial;
                                            font-weight: bold;
                                            }
                                         QPushButton:hover {
                                            background-color: rgb(25, 25, 25);
                                            }
                                         QPushButton:pressed {
                                            background-color: rgb(0, 0, 0);
                                            border-radius: 30px;
                                            }""")


    # A dropdown list that contains available currency to choose
        self.dropdownL = QComboBox(self)
        self.dropdownL.setGeometry(15, 190, 140, 30)
        self.dropdownL.setMaxVisibleItems(5)
        self.dropdownL.setFont(QFont("Arial", 10))
        self.dropdownL.setStyleSheet("""
                QComboBox {
                    border: 1px solid black;
                    background-color: black;
                    color: lightgray;
                    border: 1px solid lightgray;
                    border-radius: 15px;
                    font-size: 15px;
                    }
                QComboBox::drop-down {
                    background: transparent;
                    }
                QComboBox QAbstractItemView {
                    background-color: black;
                    color: lightgray;
                    font-size: 7pt;
                    border: 1px solid lightgray;
                    border-radius: 10px;
                    }""")

    # Will add these items to dropdown list
        self.dropdownL.addItems([
            "USD - US Dollar",
            "KRW - South Korea",
            "EGP - Egypt",
            "ILS - Israel",
            "JMD - Jamaica",
            "EUR - Euro",
            "JPY - Japanese Yen",
            "PHP - Philippine Peso",
            "CAD - Canadian Dollar",
            "AUD- Australia",
            "BRL - Brazil Republic"])

    # Initialization of listview to make the dropdown list scrollable
        list_viewL = QListView()
        list_viewL.setSpacing(2)
        list_viewL.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        list_viewL.setStyleSheet("""
                QListView::item {
                    height: 30px;
                    padding-right: 5px;
                    border-radius: 10px;
                    }
                QListView::item:selected {
                    background-color: rgb(130, 130, 130);
                    color: black;
                    padding-left: 15px;
                    }
                QListView::item:hover {
                    background-color: rgb(160, 160, 160);
                    }
                QListView::item:disabled {
                    background-color: rgb(30, 30, 30);
                    }""")
        self.dropdownL.setView(list_viewL)
        self.dropdownL.currentIndexChanged.connect(self.primary_dropdown)

    # Same as the previous dropdown list but this one is for the conversion currency
        self.dropdownR = QComboBox(self)
        self.dropdownR.setGeometry(200, 190, 140, 30)
        self.dropdownR.setMaxVisibleItems(5)
        self.dropdownR.setFont(QFont("Arial", 10))
        self.dropdownR.setStyleSheet("""
                QComboBox {
                    border: 1px solid black;
                    background-color: black;
                    color: lightgray;
                    border: 1px solid lightgray;
                    border-radius: 15px;
                    font-size: 15px;
                    }
                QComboBox::drop-down {
                    background: transparent;
                    }
                QComboBox QAbstractItemView {
                    background-color: black;
                    color: lightgray;
                    font-size: 7pt;
                    border: 1px solid lightgray;
                    border-radius: 10px;
                    }""")

        self.dropdownR.addItems([
            "USD - US Dollar",
            "KRW - South Korea",
            "EGP - Egypt",
            "ILS - Israel",
            "JMD - Jamaica",
            "EUR - Euro",
            "JPY - Japanese Yen",
            "PHP - Philippine Peso",
            "CAD - Canadian Dollar",
            "AUD- Australia",
            "BRL - Brazil Republic"])

        list_viewR = QListView()
        list_viewR.setSpacing(2)
        list_viewR.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        list_viewR.setStyleSheet("""
                QListView::item {
                    height: 30px;
                    padding-right: 5px;
                    border-radius: 10px;
                    }
                QListView::item:selected {
                    background-color: rgb(130, 130, 130);
                    color: black;
                    padding-left: 15px;
                    }
                QListView::item:hover {
                    background-color: rgb(160, 160, 160);
                    }
                QListView::item:disabled {
                    background-color: rgb(30, 30, 30);
                    }""")
        self.dropdownR.setView(list_viewR)


    # Initializing the dropdown elements with their current index
        self.dropdownR.setCurrentIndex(1)
        self.dropdownR.currentIndexChanged.connect(self.secondary_dropdown)
        self.dropdownR.model().item(primary_index).setEnabled(False)
        self.dropdownL.model().item(secondary_index).setEnabled(False)


    # If data is updated (eg. made a new request from API) then the currency values will be updated
        self.updateDelay = QTimer()
        self.updateDelay.timeout.connect(self.update_data)
        self.updateDelay.start(1000)
        self.update_data()

    # Upon opening the page, will initialize their value until update
        self.initial_run()


    # For tutorial event
        cover_opacity = QGraphicsOpacityEffect(self)
        cover_opacity.setOpacity(0.8)
        self.cover = QLabel(self)       # This is the cover with darken opacity
        self.cover.setGeometry(0, 0, self.width(), self.height())
        self.cover.setGraphicsEffect(cover_opacity)
        self.cover.hide()               # Temporarily hide it until called
        self.cover.setStyleSheet("background-color: black;")

        self.fake_cover = QLabel(self)      # Invisible layer to prevent highlighted elements from being interactable
        self.fake_cover.setGeometry(0, 0, self.width(), self.height())
        self.fake_cover.hide()
        self.fake_cover.setStyleSheet("background: transparent;")

        self.next_button = QPushButton("Next",self)     # To move to the next text index
        self.next_button.setGeometry(10, 85, 80, 35)
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

        self.info_label = QLabel(self)      # This is where the text from index will be shown
        self.info_label.setGeometry(10, 180, 340, 180)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.hide()
        self.info_label.setStyleSheet("background: transparent;"
                                      "color: lightgray;"
                                      "font-weight: bold;"
                                      "font-family: Arial;"
                                      "font-size: 18px;")

        self.arrow_left = QLabel("🡸",self)      # To point out/highlight a specific element
        self.arrow_left.setGeometry(120, 205, 60, 60)
        self.arrow_left.hide()
        self.arrow_left.setStyleSheet("background: transparent;"
                                      "color: rgb(200, 200, 0);"
                                      "font-size: 30px;"
                                      "font-weight: bold;")

    # Checks if the user first time on this page
        self.is_first_time()


    # Collect all elements on this page to resize them on window size change
        self.elements = [(self.navLine1, self.navLine1.geometry()),
                             (self.navLine2, self.navLine2.geometry()),
                             (self.backButt, self.backButt.geometry()),
                             (self.inputPrimary, self.inputPrimary.geometry()),
                             (self.convertedValue, self.convertedValue.geometry()),
                             (self.primaryValue, self.primaryValue.geometry()),
                             (self.selectedValue, self.selectedValue.geometry()),
                             (self.convertButton, self.convertButton.geometry()),
                             (self.titleLabel, self.titleLabel.geometry()),
                             (self.dropdownL, self.dropdownL.geometry()),
                             (self.dropdownR, self.dropdownR.geometry()),
                             (self.info_label, self.info_label.geometry()),
                             (self.arrow_left, self.arrow_left.geometry()),
                             (self.cover, self.cover.geometry()),
                             (self.next_button, self.next_button.geometry()),
                             (self.fake_cover, self.fake_cover.geometry())]

        # Triggered when Back Button is clicked and will close this page and open the Home Page
    def backButt_onClick(self):
        global tutorial_index
        tutorial_index = 1
        self.close()



# Checks if first time
    def is_first_time(self):
        if os.path.exists(self.tutorial_path):
            with open(self.tutorial_path, 'r') as f:        # Check if file exists
                first_time = json.load(f)

                if first_time['complete'] < 2:              # Value '1' means tutorial on home page is complete, while '2' means tutorial on home page and conversion page is complete
                    self.tutorial()                         # If Value is '1' then trigger the tutorial

        else:                                               # If file didn't exists then trigger the tutorial
            self.tutorial()


# Tutorial method
    def tutorial(self):
# Show and arrange elements for tutorial
        self.cover.show()
        self.info_label.show()
        self.next_button.show()
        self.fake_cover.show()
        self.cover.raise_()
        self.fake_cover.raise_()
        self.info_label.raise_()
        self.next_button.raise_()

    # Scripts for tutorial stored in list for easy indexing
        tutorial_script = ["Ah, I see. So you want to\ncalculate exchange rates huh.",
                          "Well you are in the\nright place!",
                          "Allow me to introduce you\nthe buttons in this page",
                          "Here you can select the currency\nyou want to exchange",
                          "Upon clicking, it will show you\nvariety of choices you can pick",
                          "You can also scroll it down\nto see more available options",
                          "You'll be able to see the current value\nof your selected currency here",
                          "On the other hand, this\nsection will be the conversion rate\nof your selected currency",
                          "In this field, you can input the\namount you want to exchange",
                          "And by clicking this button,\nyour input will be converted\nto your selected exchange",
                          "You'll see the converted value\nin this section",
                          "Assuming you input 3.5\nin input field",
                          "This will be the converted\nvalue based on your selected\ncurrency and target currency",
                          "That's all for now",
                          ""]

    # Set the primary text for tutorial label
        self.info_label.setText(tutorial_script[0])

    # Trigger when Next button is clicked
        def next_button_click():
            global tutorial_index

            if tutorial_index < len(tutorial_script):       # Updating tutorial label each click
                self.info_label.setText(tutorial_script[tutorial_index])

            tutorial_index += 1                             # Moving to the next index

            match tutorial_index:                           # Actions that will occur in each specific index
                case 4:                                     # Highlights dropdown button
                    self.dropdownL.raise_()
                    self.info_label.raise_()
                    self.next_button.raise_()

                case 5:                                     # Opens dropdown list
                    self.dropdownL.showPopup()
                    self.info_label.move(self.info_label.x(), 180 + 260)

                case 6:                                     # Reopen the dropdown list
                    self.dropdownL.showPopup()
                    self.info_label.move(self.info_label.x(), 180 + 260)

                case 7:                                     # Highlights the currency value indicator with arrow pointing at it
                    self.arrow_left.show()
                    self.arrow_left.raise_()
                    self.dropdownL.hidePopup()
                    self.primaryValue.raise_()
                    self.info_label.move(self.info_label.x(), 180 + 260)

                case 8:                                     # Highlights dropdown convertion currency
                    self.arrow_left.hide()
                    self.dropdownL.hidePopup()
                    self.dropdownL.lower()
                    self.primaryValue.lower()
                    self.dropdownR.raise_()
                    self.info_label.move(self.info_label.x(), 180 + 260)

                case 9:                                     # Highlights input field
                    self.dropdownR.lower()
                    self.inputPrimary.raise_()
                    self.info_label.move(self.info_label.x(), 180 + 260)

                case 10:                                    # Highlights convert button
                    self.inputPrimary.lower()
                    self.convertButton.raise_()
                    self.next_button.raise_()
                    self.info_label.raise_()
                    self.info_label.move(self.info_label.x(), 180 + 260)

                case 11:                                    # Highlights converted results
                    self.convertedValue.raise_()
                    self.convertButton.lower()
                    self.info_label.move(self.info_label.x(), 250)

                case 12:                                    # Show a sample input in input field
                    self.cover.raise_()
                    self.inputPrimary.raise_()
                    self.inputPrimary.setText("3.5")
                    self.convertedValue.setText(
                        f"{(3.5 * float(coin_data[self.dropdownR.currentText()[0:3]])):.3f}"
                        f" {self.dropdownR.currentText()[0:3]}")
                    self.fake_cover.raise_()
                    self.next_button.raise_()
                    self.info_label.raise_()
                    self.info_label.move(self.info_label.x(), 250)

                case 13:                                    # Show the sample result
                    self.convertedValue.raise_()
                    self.inputPrimary.lower()
                    self.info_label.move(self.info_label.x(), 250)

                case 14:
                    self.info_label.move(self.info_label.x(), 180)
                    self.convertedValue.lower()

                case 15:                                    # Closing the tutorial and overwriting the file data to mark as completed tutorial
                    self.cover.hide()
                    self.info_label.hide()
                    self.next_button.hide()
                    self.fake_cover.hide()

                    with open(self.tutorial_path, "w") as f:
                        json.dump({"complete":2}, f, indent=4)

        self.next_button.clicked.connect(next_button_click)



# Will set the primary values upon opening the page
    def initial_run(self):
        global primary_selection, secondary_selection
        self.primaryValue.setText(f"Value: {float(coin_data["USD"[0:3]]):.3f}")
        self.selectedValue.setText(f"Value: {float(coin_data["KRW"[0:3]]):.3f}")


# The computation event where it will show the result on convertedValue label
    def calculateValues(self):
        global primary_selection, secondary_selection
        get_input = self.inputPrimary.text()

        try:
            if get_input == "":
                self.convertedValue.setText(f"Enter a value")

            else:
                if primary_index == 0:
                    self.convertedValue.setText(f"{(float(get_input) * float(coin_data[self.dropdownR.currentText()[0:3]])):.3f}"
                                                f" {self.dropdownR.currentText()[0:3]}")

                else:
                    self.convertedValue.setText(f"{((float(get_input) / primary_selection) * secondary_selection):.3f}"
                                                f" {self.dropdownR.currentText()[0:3]}")

        except:
            self.convertedValue.setText(f"Invalid Input")


# constantly updates currency datas in case of changes or update
    def update_data(self):
        global coin_data
        file_location = "datas/usable_data.json"

        if os.path.exists(file_location):
            with open(file_location, "r") as file:
                coin_data = json.load(file)

        self.primaryValue.setText(f"Value: {float(coin_data[self.dropdownL.currentText()[0:3]]):.3f}")
        self.selectedValue.setText(f"Value: {float(coin_data[self.dropdownR.currentText()[0:3]]):.3f}")



# Currency dropdown list located on left
    def primary_dropdown(self, index):
        global primary_selection, primary_index

        self.dropdownR.model().item(primary_index).setEnabled(True)

        selected = self.dropdownL.currentText()
        selected_index = self.dropdownL.currentIndex()

        text = float(coin_data[selected[0:3]])      # Get the selected currency current price

        self.primaryValue.setText(f"Value: {text:.3f}")         # Update the currency value upon selecting new currency
        self.dropdownR.model().item(selected_index).setEnabled(False)       # Disable the selected currency on the other dropdown to prevent similar selection

        primary_index = selected_index              # Update the global with the new index
        primary_selection = float(text)             # Update the global with the new selected currency price



# Conversion currency dropdown list located on right
    def secondary_dropdown(self, index):
        global secondary_selection, secondary_index

        self.dropdownL.model().item(secondary_index).setEnabled(True)

        selected = self.dropdownR.currentText()
        selected_index = self.dropdownR.currentIndex()

        text = float(coin_data[selected[0:3]])      # Get the selected conversion currency current price

        self.selectedValue.setText(f"Value: {text:.3f}")        # Update the conversion currency value upon selecting new currency
        self.dropdownL.model().item(selected_index).setEnabled(False)       # Disable the selected conversion currency on the other dropdown to prevent similar selection

        secondary_index = selected_index            # Update the global with the new index
        secondary_selection = float(text)           # Update the global with the new selected conversion currency price



# Collects all the UI elements and resize them according to window size change event
    def resizeEvent(self, event):
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