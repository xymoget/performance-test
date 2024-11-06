# main.py

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import database
import tests_ui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Benchmark")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: black; color: white;")
        
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

        # Central widget with stacked layout
        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Create test UIs
        self.cpu_test_ui = tests_ui.create_test_ui(self, "CPU")
        self.ram_test_ui = tests_ui.create_test_ui(self, "RAM")
        self.disk_test_ui = tests_ui.create_test_ui(self, "DISK")

        # Add test UIs to the central widget
        self.central_widget.addWidget(self.cpu_test_ui)
        self.central_widget.addWidget(self.ram_test_ui)
        self.central_widget.addWidget(self.disk_test_ui)

        # Create main menu UI after initializing test UIs
        self.main_menu = self.create_main_menu()
        self.central_widget.addWidget(self.main_menu)

        # Set the main menu as the initial widget
        self.central_widget.setCurrentWidget(self.main_menu)

    def create_main_menu(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Welcome label
        welcome_label = QtWidgets.QLabel("Hello!\nSelect one of the tests below!")
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

    def show_history_dialog(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Test History")
        dialog.setGeometry(150, 150, 400, 300)

        layout = QtWidgets.QVBoxLayout(dialog)

        # Retrieve and display test results
        results = database.get_test_results()
        if results:
            history_text = "\n".join([f"{test_type} | Result: {result} | Time: {timestamp}"
                                     for test_type, result, timestamp in results])
        else:
            history_text = "No test history available."

        history_label = QtWidgets.QLabel(history_text)
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
