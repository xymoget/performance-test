# tests_ui.py

import random
from PyQt5 import QtWidgets, QtGui, QtCore
import database
import psutil
import platform
from datetime import datetime

class StopwatchLabel(QtWidgets.QLabel):
    """A label that acts as a stopwatch."""
    def __init__(self):
        super().__init__("00:00")
        self.setStyleSheet("font-size: 36px; color: #4B0082; font-family: 'Segoe UI', Arial;")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.time_elapsed = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_time)

    def start(self):
        self.time_elapsed = 0
        self.setText("00:00")
        self.timer.start(1000)  # Update every second

    def stop(self):
        self.timer.stop()

    def update_time(self):
        self.time_elapsed += 1
        minutes = self.time_elapsed // 60
        seconds = self.time_elapsed % 60
        self.setText(f"{minutes:02}:{seconds:02}")

def get_cpu_info():
    """Retrieve CPU information."""
    cpu_name = platform.processor() or "Unknown CPU"
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    frequency = psutil.cpu_freq().max if psutil.cpu_freq() else "Unknown"
    return f"CPU Name: {cpu_name}", f"CPU Characteristics: {cores} Cores, {threads} Threads, {frequency / 1000:.2f} GHz"

def get_ram_info():
    """Retrieve RAM information."""
    total_memory = psutil.virtual_memory().total / (1024 ** 3)  # Convert to GB
    return f"RAM Name: Physical Memory", f"RAM Characteristics: {total_memory:.2f} GB"

def get_disk_info():
    """Retrieve Disk information."""
    disk = psutil.disk_usage('/')
    total_disk = disk.total / (1024 ** 3)  # Convert to GB
    return f"Disk Name: System Disk", f"Disk Characteristics: {total_disk:.2f} GB Total"

def show_other_results():
    """Show a dialog with hardcoded benchmark results for different configurations."""
    dialog = QtWidgets.QDialog()
    dialog.setWindowTitle("Other Benchmark Results")
    dialog.setGeometry(200, 200, 600, 300)  # Set a larger width to display all text

    # Table with hardcoded results
    table = QtWidgets.QTableWidget(5, 4)  # 5 rows, 4 columns
    table.setHorizontalHeaderLabels(["Configuration", "CPU Result", "RAM Result", "Disk Result"])
    
    # Resize columns to fit content
    table.setColumnWidth(0, 250)  # Wider column for configuration description
    table.setColumnWidth(1, 100)  # CPU result column
    table.setColumnWidth(2, 100)  # RAM result column
    table.setColumnWidth(3, 100)  # Disk result column

    # Hardcoded data
    data = [
        ["Intel i7-9700K, 16GB RAM, SSD", "6200", "2900", "4800"],
        ["AMD Ryzen 5 3600, 16GB RAM, SSD", "5900", "2700", "4500"],
        ["Intel i5-9400F, 8GB RAM, HDD", "5400", "2400", "3000"],
        ["AMD Ryzen 7 3700X, 32GB RAM, SSD", "6400", "3000", "4900"],
        ["Intel i9-9900K, 32GB RAM, NVMe", "6500", "3100", "5000"],
    ]

    # Populate table
    for row, (config, cpu, ram, disk) in enumerate(data):
        table.setItem(row, 0, QtWidgets.QTableWidgetItem(config))
        table.setItem(row, 1, QtWidgets.QTableWidgetItem(cpu))
        table.setItem(row, 2, QtWidgets.QTableWidgetItem(ram))
        table.setItem(row, 3, QtWidgets.QTableWidgetItem(disk))

    layout = QtWidgets.QVBoxLayout(dialog)
    layout.addWidget(table)

    # Close button
    close_button = QtWidgets.QPushButton("Close")
    close_button.clicked.connect(dialog.close)
    layout.addWidget(close_button)

    dialog.exec_()

def create_test_ui(main_window, test_type):
    if test_type == "CPU":
        name_text, characteristics_text = get_cpu_info()
    elif test_type == "RAM":
        name_text, characteristics_text = get_ram_info()
    elif test_type == "DISK":
        name_text, characteristics_text = get_disk_info()
    else:
        name_text, characteristics_text = "Unknown", "No information available"

    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(widget)
    layout.setAlignment(QtCore.Qt.AlignTop)
    layout.setSpacing(15)

    # Customize the background and text color
    widget.setStyleSheet("""
        background-color: #F5F5F5;
        color: #4B0082;
        font-family: 'Segoe UI', Arial;
    """)

    # Test Information
    name_label = QtWidgets.QLabel(name_text)
    characteristics_label = QtWidgets.QLabel(characteristics_text)
    name_label.setStyleSheet("font-size: 20px; font-weight: 600; margin-bottom: 5px;")
    characteristics_label.setStyleSheet("font-size: 18px; margin-bottom: 15px;")
    layout.addWidget(name_label)
    layout.addWidget(characteristics_label)

    # Stopwatch
    stopwatch = StopwatchLabel()
    layout.addWidget(stopwatch)

    # Start button and output label
    start_button = QtWidgets.QPushButton("Start Test")
    start_button.setIcon(QtGui.QIcon("icons/start.png"))  # Replace with your icon path
    start_button.setIconSize(QtCore.QSize(32, 32))
    start_button.setStyleSheet("""
        QPushButton {
            background-color: #4B0082;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #551A8B;
        }
    """)
    output_label = QtWidgets.QLabel("")
    output_label.setStyleSheet("font-size: 16px; color: #800080; margin-top: 10px;")

    # Export and Other Results button layout
    button_layout = QtWidgets.QHBoxLayout()

    # Export button (initially hidden, shown after test ends)
    export_button = QtWidgets.QPushButton("Export")
    export_button.setIcon(QtGui.QIcon("icons/export.png"))  # Replace with your icon path
    export_button.setIconSize(QtCore.QSize(24, 24))
    export_button.setStyleSheet("""
        QPushButton {
            background-color: #4B0082;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #551A8B;
        }
    """)
    export_button.setVisible(False)  # Hide initially

    # Other Results button (initially hidden)
    other_results_button = QtWidgets.QPushButton("Compare")
    other_results_button.setIcon(QtGui.QIcon("icons/results.png"))  # Replace with your icon path
    other_results_button.setIconSize(QtCore.QSize(24, 24))
    other_results_button.setStyleSheet("""
        QPushButton {
            background-color: #4B0082;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #551A8B;
        }
    """)
    other_results_button.clicked.connect(show_other_results)
    other_results_button.setVisible(False)  # Hide initially
    button_layout.addWidget(export_button)
    button_layout.addWidget(other_results_button)
    layout.addLayout(button_layout)

    # Variable to store the random result
    test_result = {"value": None}  # Use a mutable dictionary to allow updates in inner functions

    # Define export action
    def export_result():
        if test_result["value"] is not None:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                None, "Save Test Result", "", "Text Files (*.txt)"
            )
            if filename:
                current_time = datetime.now().strftime("%m/%d/%Y %I:%M%p")
                content = (
                    f"{test_type} Benchmark\n"
                    f"Result: {test_result['value']}\n"
                    f"Time taken: {stopwatch.time_elapsed} seconds\n"
                    f"Datetime of the test: {current_time}"
                )
                with open(filename, "w") as file:
                    file.write(content)

    export_button.clicked.connect(export_result)

    back_button = QtWidgets.QPushButton("Back")
    back_button.setIcon(QtGui.QIcon("icons/back.png"))  # Replace with your icon path
    back_button.setIconSize(QtCore.QSize(24, 24))
    back_button.setStyleSheet("""
        QPushButton {
            background-color: #4B0082;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #551A8B;
        }
    """)

    def start_test():
        start_button.setEnabled(False)
        back_button.setEnabled(False)  # Block navigation until the test ends
        output_label.setText("Running test...")
        stopwatch.start()
        QtCore.QTimer.singleShot(20000, lambda: finish_test(output_label, start_button, back_button, stopwatch, export_button, other_results_button, test_type, test_result))

    start_button.clicked.connect(start_test)
    layout.addWidget(start_button)
    layout.addWidget(output_label)

    # Buttons for history and recommendations
    button_layout = QtWidgets.QHBoxLayout()
    button_layout.setSpacing(20)

    history_button = QtWidgets.QPushButton("Test History")
    history_button.setIcon(QtGui.QIcon("icons/history.png"))  # Replace with your icon path
    history_button.setIconSize(QtCore.QSize(24, 24))
    history_button.setStyleSheet("""
        QPushButton {
            background-color: #D3D3D3;
            color: #4B0082;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #C0C0C0;
        }
    """)
    history_button.clicked.connect(main_window.show_history_dialog)

    recommendations_button = QtWidgets.QPushButton("Recommendations")
    recommendations_button.setIcon(QtGui.QIcon("icons/recommendations.png"))  # Replace with your icon path
    recommendations_button.setIconSize(QtCore.QSize(24, 24))
    recommendations_button.setStyleSheet("""
        QPushButton {
            background-color: #D3D3D3;
            color: #4B0082;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #C0C0C0;
        }
    """)
    recommendations_button.clicked.connect(main_window.show_recommendations_dialog)

    button_layout.addWidget(history_button)
    button_layout.addWidget(recommendations_button)
    layout.addLayout(button_layout)

    back_button.clicked.connect(lambda: main_window.central_widget.setCurrentWidget(main_window.main_menu))
    layout.addWidget(back_button)

    return widget

def finish_test(output_label, start_button, back_button, stopwatch, export_button, other_results_button, test_type, test_result):
    if test_type == "CPU":
        random_number = random.randint(5000, 6500)
    elif test_type == "RAM":
        random_number = random.randint(2000, 3000)
    elif test_type == "DISK":
        random_number = random.randint(4000, 5000)
    else:
        random_number = 0  # Default result if test type is unknown

    stopwatch.stop()
    output_label.setText(f"Test completed. Result: {random_number}")
    database.insert_test_result(test_type, random_number)  # Save to the database
    start_button.setEnabled(True)
    back_button.setEnabled(True)  # Enable back button after the test ends
    export_button.setVisible(True)  # Show the export button
    other_results_button.setVisible(True)  # Show the Other Results button after test ends

    # Store the test result for exporting
    test_result["value"] = random_number
