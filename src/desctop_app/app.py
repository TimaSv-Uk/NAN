from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QGroupBox
from PySide6.QtGui import QAction, QIntValidator, QFont, QTextCursor

import sys
import os

from cryptall_2.encode_decode import encode_file, decode_file

DEFAULT_SEED = 0


class EncodeWorker(QtCore.QThread):
    finished = QtCore.Signal(bool, str)

    def __init__(self, file_path: str, save_path: str, number: int):
        super().__init__()
        self.file_path = file_path
        self.save_path = save_path
        self.number = number

    def run(self):
        try:
            encode_file(self.file_path, self.save_path, self.number)
            self.finished.emit(True, f"File encoded successfully! seed: {self.number}")
        except Exception as e:
            self.finished.emit(False, str(e))


class DecodeWorker(QtCore.QThread):
    finished = QtCore.Signal(bool, str)

    def __init__(self, file_path: str, save_path: str, number: int):
        super().__init__()
        self.file_path = file_path
        self.save_path = save_path
        self.number = number

    def run(self):
        try:
            decode_file(self.file_path, self.save_path, self.number)
            self.finished.emit(True, f"File decoded successfully!. seed: {self.number}")
        except Exception as e:
            self.finished.emit(False, str(e))


class MainPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        self.title = QtWidgets.QLabel(
            "File Encoder/Decoder", alignment=QtCore.Qt.AlignCenter
        )
        self.title.setObjectName("titleLabel")
        layout.addWidget(self.title)

        # File Selection Group
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout(file_group)

        self.file_button = QtWidgets.QPushButton("Select File")
        self.file_label = QtWidgets.QLabel("No file selected")
        self.file_label.setWordWrap(True)
        self.file_button.clicked.connect(self.open_file_dialog)
        self.file_lineedit = QtWidgets.QLineEdit()
        self.file_lineedit.setPlaceholderText(
            "Enter file path manually or use the button below"
        )
        self.file_lineedit.textChanged.connect(
            lambda text: self.file_label.setText(text)
        )

        file_layout.addWidget(self.file_lineedit)
        file_layout.addWidget(self.file_button)
        file_layout.addWidget(self.file_label)

        # Number Input Group
        seed_group = QGroupBox("Configuration")
        seed_layout = QVBoxLayout(seed_group)

        self.seed_input = QtWidgets.QLineEdit()
        self.seed_input.setPlaceholderText(
            f"Enter a seed (optional default is {DEFAULT_SEED})"
        )
        self.seed_input.setValidator(QIntValidator())
        seed_layout.addWidget(self.seed_input)

        # Save Path Group
        save_group = QGroupBox("Output Destination")
        save_layout = QVBoxLayout(save_group)

        self.save_lineedit = QtWidgets.QLineEdit()
        self.save_lineedit.setPlaceholderText(
            "Enter save path manually or use the button below"
        )
        self.save_lineedit.textChanged.connect(
            lambda text: self.save_label.setText(text)
        )

        self.save_button = QtWidgets.QPushButton("Select Save Path")
        self.save_label = QtWidgets.QLabel("No save path selected")
        self.save_label.setWordWrap(True)
        self.save_button.clicked.connect(self.open_save_dialog)

        save_layout.addWidget(self.save_lineedit)
        save_layout.addWidget(self.save_button)
        save_layout.addWidget(self.save_label)

        # Action Buttons Group
        action_group = QGroupBox("Actions")
        action_layout = QHBoxLayout(action_group)

        self.encode_button = QtWidgets.QPushButton("[ENCODE] Encode File")
        self.decode_button = QtWidgets.QPushButton("[DECODE] Decode File")
        self.swap_encode_decode_file_button = QtWidgets.QPushButton(
            "Swap [ENCODE]<-> [DECODE] filepaths"
        )

        self.encode_button.clicked.connect(self.encode_file_action)
        self.decode_button.clicked.connect(self.decode_file_action)
        self.swap_encode_decode_file_button.clicked.connect(
            self.swap_encode_decode_file
        )

        action_layout.addWidget(self.encode_button)
        action_layout.addWidget(self.decode_button)
        action_layout.addWidget(self.swap_encode_decode_file_button)

        # Status Display
        self.status_text = QtWidgets.QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMinimumHeight(100)
        self.status_text.setMaximumHeight(200)
        self.status_text.setPlaceholderText("Status messages will appear here...")

        # Add all groups to main layout
        layout.addWidget(file_group)
        layout.addWidget(seed_group)
        layout.addWidget(save_group)
        layout.addWidget(action_group)
        layout.addWidget(self.status_text)

    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select a File", ".", "All Files (*)"
        )
        if filename:
            self.file_label.setText(filename)
            self.file_lineedit.setText(filename)
            self.update_status(f"[+] Selected file: {filename}")

    def open_save_dialog(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Select Save Path", ".", "All Files (*)"
        )
        if save_path:
            self.save_label.setText(save_path)
            self.save_lineedit.setText(save_path)
            self.update_status(f"[+] Save path set: {save_path}")

    def swap_encode_decode_file(self):
        file_path = self.file_label.text()
        save_path = self.save_label.text()
        print(file_path, save_path)
        if file_path == "No file selected" or save_path == "No save path selected":
            return

        self.file_label.setText(save_path)
        self.save_label.setText(file_path)

        self.file_lineedit.setText(save_path)
        self.save_lineedit.setText(file_path)

        self.update_status(f"[_] Swap file path: {save_path} <-> {file_path}")

    def update_status(self, message):
        current_text = self.status_text.toPlainText()
        if current_text:
            new_text = current_text + "\n" + message
        else:
            new_text = message
        self.status_text.setPlainText(new_text)
        # Scroll to bottom
        cursor = self.status_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.status_text.setTextCursor(cursor)

    def validate_inputs(self):
        file_path = self.file_label.text()
        save_path = self.save_label.text()

        if not os.path.exists(file_path):
            QtWidgets.QMessageBox.warning(
                self, "Invalid Input", f"Input file [{file_path}] doth not exist."
            )
            return None, None, None
        if file_path == save_path:
            QtWidgets.QMessageBox.warning(
                self,
                "Invalid Input",
                "Can't encode file itself. Select new [Save path]",
            )
            return None, None, None

        if file_path == "No file selected":
            QtWidgets.QMessageBox.warning(
                self, "Invalid Input", "Please select a file first."
            )
            return None, None, None

        if save_path == "No save path selected":
            QtWidgets.QMessageBox.warning(
                self, "Invalid Input", "Please select a save path."
            )
            return None, None, None

        seed_input_text = self.seed_input.text()
        seed = int(seed_input_text) if seed_input_text else DEFAULT_SEED

        return file_path, save_path, seed

    def encode_file_action(self):
        file_path, save_path, seed = self.validate_inputs()
        if file_path is None:
            return

        try:
            self.loader = QtWidgets.QProgressDialog("Encoding...", None, 0, 0, self)
            self.loader.setWindowTitle("Please wait")
            self.loader.setWindowModality(QtCore.Qt.WindowModal)
            self.loader.setCancelButton(None)
            self.loader.show()
            # encode_file(file_path, save_path)
            self.worker = EncodeWorker(file_path, save_path, seed)
            self.worker.finished.connect(self.on_done)
            self.worker.start()

            self.update_status(f"[ENCODED] File encoded successfully!")
            self.update_status(f"   Input: {file_path}")
            self.update_status(f"   Output: {save_path}")
            if seed:
                self.update_status(f"   Number: {seed}")

        except Exception as e:
            self.update_status(f"[ERROR] Error encoding file: {str(e)}")

    def decode_file_action(self):
        file_path, save_path, number = self.validate_inputs()
        if file_path is None:
            return

        try:
            self.loader = QtWidgets.QProgressDialog("Decoding...", None, 0, 0, self)
            self.loader.setWindowTitle("Please wait")
            self.loader.setWindowModality(QtCore.Qt.WindowModal)
            self.loader.setCancelButton(None)
            self.loader.show()
            # encode_file(file_path, save_path)
            self.worker = DecodeWorker(file_path, save_path, number)
            self.worker.finished.connect(self.on_done)
            self.worker.start()

            self.update_status(f"[DECODED] File decoded successfully!")
            self.update_status(f"   Input: {file_path}")
            self.update_status(f"   Output: {save_path}")
            if number:
                self.update_status(f"   Number: {number}")

        except Exception as e:
            self.update_status(f"[ERROR] Error decoding file: {str(e)}")

    def on_done(self, success, message):
        self.loader.close()
        if success:
            QtWidgets.QMessageBox.information(self, "Success", message)
        else:
            QtWidgets.QMessageBox.critical(self, "Error", message)


class PageOne(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)

        label = QtWidgets.QLabel("Documentation", alignment=QtCore.Qt.AlignCenter)
        label.setFont(QFont("Arial", 20, QFont.Bold))

        content = QtWidgets.QLabel(
            "This application allows you to encode and decode files.\n\n"
            "Features:\n"
            "* Select any file for processing\n"
            "* Choose output destination\n"
            "* Encode files for security\n"
            "* Decode previously encoded files\n"
            "* Real-time status updates\n\n"
            "Use the main page to process your files.",
            alignment=QtCore.Qt.AlignLeft,
        )
        content.setWordWrap(True)

        layout.addWidget(label)
        layout.addWidget(content)
        layout.addStretch()


class PageTwo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)

        label = QtWidgets.QLabel("About", alignment=QtCore.Qt.AlignCenter)
        label.setFont(QFont("Arial", 20, QFont.Bold))

        content = QtWidgets.QLabel(
            "File Encoder/Decoder Application\n\n"
            "Version: 2.0\n"
            "Built with: PySide6\n\n"
            "This application provides a simple and intuitive interface\n"
            "for encoding and decoding files using custom algorithms.\n\n"
            "Features a clean black and white design for\n"
            "professional appearance and ease of use.",
            alignment=QtCore.Qt.AlignLeft,
        )
        content.setWordWrap(True)

        layout.addWidget(label)
        layout.addWidget(content)
        layout.addStretch()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Encoder/Decoder - Professional Edition")

        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()

        self.page_width = int(screen_width * 0.70)  # 70% of screen width

        # Create pages
        self.main_page = MainPage()
        self.page_one = PageOne()
        self.page_two = PageTwo()
        # Stacked widget
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.addWidget(self.main_page)  # index 0
        self.stacked_widget.addWidget(self.page_one)  # index 1
        self.stacked_widget.addWidget(self.page_two)  # index 2
        self.stacked_widget.setMaximumSize(self.page_width, 1100)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)

        scroll.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )
        scroll.setFixedWidth(self.page_width)

        scroll.setWidget(self.stacked_widget)

        central_container = QtWidgets.QWidget()
        container_layout = QtWidgets.QVBoxLayout(central_container)
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addStretch(1)  # Left spacer
        h_layout.addWidget(scroll)
        h_layout.addStretch(1)  # Right spacer
        container_layout.addLayout(h_layout)

        self.setCentralWidget(central_container)

        menu_bar = self.menuBar()
        navigate_menu = menu_bar.addMenu("Menu")

        main_action = QAction("Main Page", self)
        docs_action = QAction("Documentation", self)

        about_action = QAction("About", self)
        navigate_menu.addAction(main_action)
        navigate_menu.addAction(docs_action)
        navigate_menu.addAction(about_action)

        main_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        docs_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        about_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        self.apply_styles()

    def apply_styles(self):
        # Main application style - Black and White theme
        self.setStyleSheet("""
            * { 
                font-size: 20px;
            }
            /* Main Window */
            QMainWindow {
                background-color: #ffffff;
                color: #000000;

            }
            /* Stacked Widget */
            QStackedWidget {
                background-color: #ffffff;
                border: none;
            }
            
            /* Labels */
            QLabel {
                color: #000000;
                padding: 5px;
            }
            #titleLabel {
                font-size: 42px;
                font-weight: bold;
            }
            /* Group Boxes */
            QGroupBox {
                font-weight: bold;
                border: 2px solid #000000;
                border-radius: 8px;
                margin: 10px 0px;
                padding-top: 15px;
                background-color: #f8f8f8;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: #ffffff;
                color: #000000;
            }
            
            /* Buttons */
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                border: none;
                padding: 12px 20px;

                font-weight: bold;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QPushButton:hover {
                background-color: #333333;
            }
            
            QPushButton:pressed {
                background-color: #666666;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            
            /* Line Edit */
            QLineEdit {
                border: 2px solid #000000;
                border-radius: 4px;
                padding: 8px 12px;
                background-color: #ffffff;
                color: #000000;
            }
            
            QLineEdit:focus {
                border-color: #444444;
            }
            
            /* Text Edit */
            QTextEdit {
                border: 2px solid #000000;
                border-radius: 4px;
                padding: 8px;
                background-color: #fafafa;
                color: #000000;
                font-family: 'Courier New', monospace;
                font-size: 20px;
            }
            
            /* Menu Bar */
            QMenuBar {
                background-color: #000000;
                color: #ffffff;
                font-weight: bold;
                border-bottom: 2px solid #333333;
            }
            
            QMenuBar::item {
                spacing: 3px;
                padding: 8px 15px;
                background: transparent;
            }
            
            QMenuBar::item:selected {
                background: #333333;
                border-radius: 4px;
            }
            
            /* Menu Dropdown */
            QMenu {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #000000;
                border-radius: 4px;
            }
            
            QMenu::item {
                padding: 8px 20px;
                background: transparent;
            }
            
            QMenu::item:selected {
                background-color: #000000;
                color: #ffffff;
            }
            
            /* Message Box */
            QMessageBox {
                background-color: #ffffff;
                color: #000000;
            }
            
            QMessageBox QPushButton {
                min-width: 80px;
                margin: 5px;
            }
        """)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(900, 700)
    window.show()
    sys.exit(app.exec())
