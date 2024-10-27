# main.py

import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Performance Test Program (PTP)")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: black; color: white;")

        # Central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(central_widget)

        # Welcome label
        welcome_label = QtWidgets.QLabel("Hello!\nWelcome to the Performance Test Program (PTP)!\nSelect one of the tests below and start improving your PC now!")
        welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 16px;")
        main_layout.addWidget(welcome_label)

        # Grid layout for buttons
        grid_layout = QtWidgets.QGridLayout()
        main_layout.addLayout(grid_layout)

        # Button data
        button_data = [
            ("CPU", "icons/icon.jpg"),
            ("GPU", "icons/images.png"),
            ("RAM", "path/to/ram_icon.png"),
            ("DISK", "path/to/disk_icon.png"),
            ("Profile", "path/to/profile_icon.png"),
            ("Tips", "path/to/tips_icon.png")
        ]

        # Create buttons with icons and labels
        for i, (text, icon_path) in enumerate(button_data):
            # Create button widget
            button = QtWidgets.QPushButton()
            button.setIcon(QtGui.QIcon(icon_path))
            button.setIconSize(QtCore.QSize(64, 64))  # Adjust icon size as needed
            button.setText(text)
            
            # Set stylesheet for centering icon above text
            button.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    color: black;
                    background-color: white;
                    padding-top: 10px;
                    padding-bottom: 10px;
                }
                QPushButton::icon {
                    margin-bottom: 5px;
                }
            """)
            button.setFixedSize(100, 100)

            # Set the text to appear below the icon
            button.setToolTip(text)  # Optional tooltip for better accessibility

            # Add button to grid layout
            row, col = divmod(i, 3)
            grid_layout.addWidget(button, row, col)

            # Connect button signals to slots
            button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        sender = self.sender()
        print(f"{sender.text()} button clicked")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
