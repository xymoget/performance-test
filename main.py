# main.py

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import database
import tests_ui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Benchmark")
        self.setFixedSize(700, 400)  # Fixed window size

        # Set icon and overall style
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
                color: #E1E1E1;
            }
            QLabel, QPushButton {
                font-family: 'Segoe UI', Arial;
                color: #FFFFFF;
            }
        """)

        # Central widget with stacked layout
        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Load UI pages
        self.cpu_test_ui = tests_ui.create_test_ui(self, "CPU")
        self.ram_test_ui = tests_ui.create_test_ui(self, "RAM")
        self.disk_test_ui = tests_ui.create_test_ui(self, "DISK")
        self.central_widget.addWidget(self.cpu_test_ui)
        self.central_widget.addWidget(self.ram_test_ui)
        self.central_widget.addWidget(self.disk_test_ui)

        # Add main menu and set as initial page
        self.main_menu = self.create_main_menu()
        self.central_widget.addWidget(self.main_menu)
        self.central_widget.setCurrentWidget(self.main_menu)

    def create_main_menu(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title label
        title_label = QtWidgets.QLabel("Welcome to Benchmark")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        """)
        layout.addWidget(title_label)

        # Instruction label
        instruction_label = QtWidgets.QLabel("Select a test to begin:")
        instruction_label.setAlignment(QtCore.Qt.AlignCenter)
        instruction_label.setStyleSheet("font-size: 18px; margin-bottom: 20px;")
        layout.addWidget(instruction_label)

        # Grid layout for buttons
        grid_layout = QtWidgets.QGridLayout()
        layout.addLayout(grid_layout)

        button_data = [
            ("CPU", "icons/cpu.png", self.cpu_test_ui),
            ("RAM", "icons/ram.png", self.ram_test_ui),
            ("DISK", "icons/disk.png", self.disk_test_ui)
        ]

        # Create styled buttons with icons
        for i, (text, icon_path, ui_widget) in enumerate(button_data):
            button = QtWidgets.QPushButton(text)
            button.setFixedSize(180, 180)
            button.setIcon(QtGui.QIcon(icon_path))
            button.setIconSize(QtCore.QSize(80, 80))
            button.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    color: #121212;
                    background-color: #F0F0F0;
                    border: 2px solid #CCCCCC;
                    border-radius: 20px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #E1E1E1;
                }
            """)
            button.clicked.connect(lambda _, w=ui_widget: self.central_widget.setCurrentWidget(w))
            row, col = divmod(i, 3)
            grid_layout.addWidget(button, row, col)

        return widget

    def show_history_dialog(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Test History")
        dialog.setFixedSize(500, 350)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1E1E1E;
            }
            QLabel {
                font-size: 16px;
                color: #E1E1E1;
            }
            QPushButton {
                font-size: 16px;
                color: #E1E1E1;
                background-color: #333333;
                border-radius: 10px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)

        layout = QtWidgets.QVBoxLayout(dialog)
        results = database.get_test_results()

        history_text = "\n".join([f"{test_type} | Result: {result} | Time: {timestamp}"
                                  for test_type, result, timestamp in results]) if results else "No test history available."

        history_label = QtWidgets.QLabel(history_text)
        history_label.setAlignment(QtCore.Qt.AlignTop)
        layout.addWidget(history_label)

        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button, alignment=QtCore.Qt.AlignCenter)

        dialog.exec_()

    def show_recommendations_dialog(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Recommendations")
        dialog.setFixedSize(500, 350)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1E1E1E;
            }
            QLabel {
                font-size: 16px;
                color: #E1E1E1;
            }
            QPushButton {
                font-size: 16px;
                color: #E1E1E1;
                background-color: #333333;
                border-radius: 10px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)

        layout = QtWidgets.QVBoxLayout(dialog)
        recommendations_text = ("General Recommendations:\n"
                                "- Keep your drivers up to date.\n"
                                "- Regularly clean your PC from dust.\n"
                                "- Use SSDs for faster disk performance.")
        recommendations_label = QtWidgets.QLabel(recommendations_text)
        recommendations_label.setAlignment(QtCore.Qt.AlignTop)
        layout.addWidget(recommendations_label)

        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button, alignment=QtCore.Qt.AlignCenter)

        dialog.exec_()

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
