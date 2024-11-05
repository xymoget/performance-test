# main.py

import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Performance Test Program (PTP)")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: black; color: white;")

        # Central widget with stacked layout
        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Create test UIs first to initialize them
        self.cpu_test_ui = self.create_test_ui("CPU", "CPU Name: Example CPU", "CPU Characteristics: 4 Cores, 8 Threads, 3.5 GHz")
        self.ram_test_ui = self.create_test_ui("RAM", "RAM Name: Example RAM", "RAM Characteristics: 16 GB, DDR4, 3200 MHz")
        self.disk_test_ui = self.create_test_ui("DISK", "DISK Name: Example Disk", "DISK Characteristics: 1 TB, SSD, 500 MB/s")

        # Add test UIs to the central widget
        self.central_widget.addWidget(self.cpu_test_ui)
        self.central_widget.addWidget(self.ram_test_ui)
        self.central_widget.addWidget(self.disk_test_ui)

        # Create main menu UI after initializing test UIs
        self.main_menu = self.create_main_menu()
        self.central_widget.addWidget(self.main_menu)

    def create_main_menu(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Welcome label
        welcome_label = QtWidgets.QLabel("Hello!\nWelcome to the Performance Test Program (PTP)!\nSelect one of the tests below and start improving your PC now!")
        welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; margin-bottom: 10px; font-family: 'Segoe UI', Arial;")
        layout.addWidget(welcome_label)

        # Grid layout for buttons
        grid_layout = QtWidgets.QGridLayout()
        layout.addLayout(grid_layout)

        # Button data with icons (replace 'icons/cpu.png', etc., with your own paths)
        button_data = [
            ("CPU", "icons/cpu.png", self.cpu_test_ui),
            ("RAM", "icons/ram.png", self.ram_test_ui),
            ("DISK", "icons/disk.png", self.disk_test_ui)
        ]

        # Create buttons with icons and labels
        for i, (text, icon_path, ui_widget) in enumerate(button_data):
            button = QtWidgets.QPushButton(text)
            button.setFixedSize(150, 150)
            button.setIcon(QtGui.QIcon(icon_path))
            button.setIconSize(QtCore.QSize(64, 64))  # Adjust icon size as needed
            button.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    color: black;
                    background-color: white;
                    font-family: 'Segoe UI', Arial;
                }
            """)
            button.clicked.connect(lambda _, w=ui_widget: self.central_widget.setCurrentWidget(w))
            row, col = divmod(i, 3)
            grid_layout.addWidget(button, row, col)

        return widget

    def create_test_ui(self, test_type, name_text, characteristics_text):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setSpacing(15)

        # Customize the background and text color
        widget.setStyleSheet("background-color: white; color: purple; font-family: 'Segoe UI', Arial;")

        # Test Information
        name_label = QtWidgets.QLabel(name_text)
        characteristics_label = QtWidgets.QLabel(characteristics_text)
        name_label.setStyleSheet("font-size: 18px; margin-bottom: 5px;")
        characteristics_label.setStyleSheet("font-size: 18px; margin-bottom: 15px;")
        layout.addWidget(name_label)
        layout.addWidget(characteristics_label)

        # Start button and output label
        start_button = QtWidgets.QPushButton("Start Test")
        start_button.setIcon(QtGui.QIcon("icons/start.png"))  # Replace with your icon path
        start_button.setIconSize(QtCore.QSize(32, 32))
        start_button.setStyleSheet("font-size: 16px; padding: 5px; color: purple;")
        output_label = QtWidgets.QLabel("")
        output_label.setStyleSheet("font-size: 16px; color: darkviolet;")

        def start_test():
            start_button.setEnabled(False)
            output_label.setText("Running test...")
            QtCore.QTimer.singleShot(20000, lambda: self.finish_test(output_label, start_button))

        start_button.clicked.connect(start_test)
        layout.addWidget(start_button)
        layout.addWidget(output_label)

        # Buttons for history and recommendations
        button_layout = QtWidgets.QHBoxLayout()
        history_button = QtWidgets.QPushButton("Test History")
        history_button.setIcon(QtGui.QIcon("icons/history.png"))  # Replace with your icon path
        history_button.setIconSize(QtCore.QSize(24, 24))
        history_button.setStyleSheet("font-size: 16px; padding: 5px; color: purple;")
        history_button.clicked.connect(self.show_history_dialog)

        recommendations_button = QtWidgets.QPushButton("Recommendations")
        recommendations_button.setIcon(QtGui.QIcon("icons/recommendations.png"))  # Replace with your icon path
        recommendations_button.setIconSize(QtCore.QSize(24, 24))
        recommendations_button.setStyleSheet("font-size: 16px; padding: 5px; color: purple;")
        recommendations_button.clicked.connect(self.show_recommendations_dialog)

        button_layout.addWidget(history_button)
        button_layout.addWidget(recommendations_button)
        layout.addLayout(button_layout)

        # Back button
        back_button = QtWidgets.QPushButton("Back")
        back_button.setIcon(QtGui.QIcon("icons/back.png"))  # Replace with your icon path
        back_button.setIconSize(QtCore.QSize(24, 24))
        back_button.setStyleSheet("font-size: 16px; padding: 5px; color: purple;")
        back_button.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.main_menu))
        layout.addWidget(back_button)

        return widget

    def finish_test(self, output_label, start_button):
        random_number = random.randint(1000, 5000)
        output_label.setText(f"Test completed. Result: {random_number}")
        start_button.setEnabled(True)

    def show_history_dialog(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Test History")
        dialog.setGeometry(150, 150, 400, 300)

        layout = QtWidgets.QVBoxLayout(dialog)
        history_label = QtWidgets.QLabel("Test History:\n(No history available yet)")
        history_label.setAlignment(QtCore.Qt.AlignTop)
        history_label.setStyleSheet("font-size: 16px; color: darkviolet; font-family: 'Segoe UI', Arial;")
        layout.addWidget(history_label)

        close_button = QtWidgets.QPushButton("Close")
        close_button.setStyleSheet("font-size: 16px; color: purple; font-family: 'Segoe UI', Arial;")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        dialog.exec_()

    def show_recommendations_dialog(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Recommendations")
        dialog.setGeometry(150, 150, 400, 300)

        layout = QtWidgets.QVBoxLayout(dialog)
        recommendations_text = "General Recommendations:\n- Keep your drivers up to date.\n- Regularly clean your PC from dust.\n- Use SSDs for faster disk performance."
        recommendations_label = QtWidgets.QLabel(recommendations_text)
        recommendations_label.setAlignment(QtCore.Qt.AlignTop)
        recommendations_label.setStyleSheet("font-size: 16px; color: darkviolet; font-family: 'Segoe UI', Arial;")
        layout.addWidget(recommendations_label)

        close_button = QtWidgets.QPushButton("Close")
        close_button.setStyleSheet("font-size: 16px; color: purple; font-family: 'Segoe UI', Arial;")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        dialog.exec_()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
