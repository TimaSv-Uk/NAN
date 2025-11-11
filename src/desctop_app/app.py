from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QGroupBox
from PySide6.QtGui import QAction, QIntValidator, QFont, QTextCursor

import sys
import os
import json

from cryptall_2.encode_decode import encode_file, decode_file


DEFAULT_SEED = 0


class UILanguageManager:
    def __init__(self, lang_file="en.json"):
        self.translations = {}
        self.current_lang_file = None
        self.load_language(lang_file)

    def load_language(self, lang_file):
        """Loads translations from a JSON file and updates the current_lang_file path."""
        abs_lang_file = os.path.abspath(lang_file)
        try:
            with open(abs_lang_file, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
                self.current_lang_file = abs_lang_file
        except FileNotFoundError:
            print(
                f"Warning: Translation file {
                    abs_lang_file
                } not found. Using empty translations."
            )
            self.translations = {}

    def get(self, key_path, **kwargs):
        """Get translation by dot-separated path, e.g., 'main_page.title'"""
        keys = key_path.split(".")
        value = self.translations

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, key_path)
            else:
                return key_path

        if kwargs and isinstance(value, str):
            try:
                return value.format(**kwargs)
            except KeyError:
                return value

        return value


class EncodeWorker(QtCore.QThread):
    finished = QtCore.Signal(bool, str)

    def __init__(self, file_path: str, save_path: str, seed: int, tr):
        super().__init__()
        self.file_path = file_path
        self.save_path = save_path
        self.seed = seed
        self.tr = tr

    def run(self):
        try:
            encode_file(self.file_path, self.save_path, self.seed)
            msg = self.tr.get("main_page.dialogs.file_encoded", seed=self.seed)
            self.finished.emit(True, msg)
        except Exception as e:
            self.finished.emit(False, str(e))


class DecodeWorker(QtCore.QThread):
    finished = QtCore.Signal(bool, str)

    def __init__(self, file_path: str, save_path: str, seed: int, tr):
        super().__init__()
        self.file_path = file_path
        self.save_path = save_path
        self.seed = seed
        self.tr = tr

    def run(self):
        try:
            decode_file(self.file_path, self.save_path, self.seed)
            msg = self.tr.get("main_page.dialogs.file_decoded", seed=self.seed)
            self.finished.emit(True, msg)
        except Exception as e:
            self.finished.emit(False, str(e))


class MainPage(QtWidgets.QWidget):
    def __init__(self, tr):
        super().__init__()
        self.tr = tr

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        self.title = QtWidgets.QLabel(
            self.tr.get("main_page.title"), alignment=QtCore.Qt.AlignCenter
        )
        self.title.setObjectName("titleLabel")
        layout.addWidget(self.title)

        # File Selection Group (Store reference for refresh)
        self.file_group = QGroupBox(self.tr.get("main_page.file_selection.group_title"))
        file_layout = QVBoxLayout(self.file_group)

        self.file_button = QtWidgets.QPushButton(
            self.tr.get("main_page.file_selection.button")
        )
        self.file_label = QtWidgets.QLabel(
            self.tr.get("main_page.file_selection.no_file")
        )
        self.file_label.setWordWrap(True)
        self.file_button.clicked.connect(self.open_file_dialog)
        self.file_lineedit = QtWidgets.QLineEdit()
        self.file_lineedit.setPlaceholderText(
            self.tr.get("main_page.file_selection.placeholder")
        )
        self.file_lineedit.textChanged.connect(
            lambda text: self.file_label.setText(text)
        )

        file_layout.addWidget(self.file_lineedit)
        file_layout.addWidget(self.file_button)
        file_layout.addWidget(self.file_label)

        # Number Input Group (Store reference for refresh)
        self.seed_group = QGroupBox(self.tr.get("main_page.configuration.group_title"))
        seed_layout = QVBoxLayout(self.seed_group)

        self.seed_input = QtWidgets.QLineEdit()
        self.seed_input.setPlaceholderText(
            self.tr.get("main_page.configuration.placeholder", default=DEFAULT_SEED)
        )
        self.seed_input.setValidator(QIntValidator())
        seed_layout.addWidget(self.seed_input)

        # Save Path Group (Store reference for refresh)
        self.save_group = QGroupBox(self.tr.get("main_page.output.group_title"))
        save_layout = QVBoxLayout(self.save_group)

        self.save_lineedit = QtWidgets.QLineEdit()
        self.save_lineedit.setPlaceholderText(
            self.tr.get("main_page.output.placeholder")
        )
        self.save_lineedit.textChanged.connect(
            lambda text: self.save_label.setText(text)
        )

        self.save_button = QtWidgets.QPushButton(self.tr.get("main_page.output.button"))
        self.save_label = QtWidgets.QLabel(self.tr.get("main_page.output.no_path"))
        self.save_label.setWordWrap(True)
        self.save_button.clicked.connect(self.open_save_dialog)

        save_layout.addWidget(self.save_lineedit)
        save_layout.addWidget(self.save_button)
        save_layout.addWidget(self.save_label)

        # Action Buttons Group (Store reference for refresh)
        self.action_group = QGroupBox(self.tr.get("main_page.actions.group_title"))
        action_layout = QHBoxLayout(self.action_group)

        self.encode_button = QtWidgets.QPushButton(
            self.tr.get("main_page.actions.encode_button")
        )
        self.decode_button = QtWidgets.QPushButton(
            self.tr.get("main_page.actions.decode_button")
        )
        self.swap_encode_decode_file_button = QtWidgets.QPushButton(
            self.tr.get("main_page.actions.swap_button")
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
        self.status_text.setPlaceholderText(self.tr.get("main_page.status.placeholder"))

        # Add all groups to main layout
        layout.addWidget(self.file_group)
        layout.addWidget(self.seed_group)
        layout.addWidget(self.save_group)
        layout.addWidget(self.action_group)
        layout.addWidget(self.status_text)

    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            self.tr.get("main_page.dialogs.select_file"),
            ".",
            self.tr.get("main_page.dialogs.all_files"),
        )
        if filename:
            self.file_label.setText(filename)
            self.file_lineedit.setText(filename)
            self.update_status(
                self.tr.get("main_page.status.file_selected", path=filename)
            )

    def open_save_dialog(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr.get("main_page.dialogs.select_save"),
            ".",
            self.tr.get("main_page.dialogs.all_files"),
        )
        if save_path:
            self.save_label.setText(save_path)
            self.save_lineedit.setText(save_path)
            self.update_status(
                self.tr.get("main_page.status.save_path_set", path=save_path)
            )

    def swap_encode_decode_file(self):
        file_path = self.file_label.text()
        save_path = self.save_label.text()

        no_file = self.tr.get("main_page.file_selection.no_file")
        no_path = self.tr.get("main_page.output.no_path")

        # Use the raw line edit text to handle cases where the label text is localized but the line edit holds the path
        if self.file_lineedit.text() == "" or self.save_lineedit.text() == "":
            # Check if the labels contain the default translated text
            if file_path == no_file or save_path == no_path:
                return

        self.file_label.setText(save_path)
        self.save_label.setText(file_path)

        self.file_lineedit.setText(save_path)
        self.save_lineedit.setText(file_path)

        self.update_status(
            self.tr.get("main_page.status.swap", path1=save_path, path2=file_path)
        )

    def update_status(self, message):
        current_text = self.status_text.toPlainText()
        if current_text:
            new_text = current_text + "\n" + message
        else:
            new_text = message
        self.status_text.setPlainText(new_text)
        cursor = self.status_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.status_text.setTextCursor(cursor)

    def validate_inputs(self):
        file_path = self.file_label.text()
        save_path = self.save_label.text()

        no_file = self.tr.get("main_page.file_selection.no_file")
        no_path = self.tr.get("main_page.output.no_path")

        # Check raw line edit content for better reliability
        if self.file_lineedit.text() == "":
            QtWidgets.QMessageBox.warning(
                self,
                self.tr.get("main_page.warnings.invalid_input"),
                self.tr.get("main_page.warnings.no_file_selected"),
            )
            return None, None, None

        if not os.path.exists(file_path):
            QtWidgets.QMessageBox.warning(
                self,
                self.tr.get("main_page.warnings.invalid_input"),
                self.tr.get("main_page.warnings.file_not_exist", path=file_path),
            )
            return None, None, None

        if file_path == save_path:
            QtWidgets.QMessageBox.warning(
                self,
                self.tr.get("main_page.warnings.invalid_input"),
                self.tr.get("main_page.warnings.same_paths"),
            )
            return None, None, None

        if self.save_lineedit.text() == "":
            QtWidgets.QMessageBox.warning(
                self,
                self.tr.get("main_page.warnings.invalid_input"),
                self.tr.get("main_page.warnings.no_save_path"),
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
            self.loader = QtWidgets.QProgressDialog(
                self.tr.get("main_page.dialogs.encoding"), None, 0, 0, self
            )
            self.loader.setWindowTitle(self.tr.get("main_page.dialogs.please_wait"))
            self.loader.setWindowModality(QtCore.Qt.WindowModal)
            self.loader.setCancelButton(None)
            self.loader.show()

            self.worker = EncodeWorker(file_path, save_path, seed, self.tr)
            self.worker.finished.connect(self.on_done)
            self.worker.start()

            self.update_status(self.tr.get("main_page.status.encoded"))
            self.update_status(self.tr.get("main_page.status.input", path=file_path))
            self.update_status(self.tr.get("main_page.status.output", path=save_path))
            if seed != DEFAULT_SEED:
                self.update_status(self.tr.get("main_page.status.number", number=seed))

        except Exception as e:
            self.update_status(self.tr.get("main_page.status.error", error=str(e)))

    def decode_file_action(self):
        file_path, save_path, number = self.validate_inputs()
        if file_path is None:
            return

        try:
            self.loader = QtWidgets.QProgressDialog(
                self.tr.get("main_page.dialogs.decoding"), None, 0, 0, self
            )
            self.loader.setWindowTitle(self.tr.get("main_page.dialogs.please_wait"))
            self.loader.setWindowModality(QtCore.Qt.WindowModal)
            self.loader.setCancelButton(None)
            self.loader.show()

            self.worker = DecodeWorker(file_path, save_path, number, self.tr)
            self.worker.finished.connect(self.on_done)
            self.worker.start()

            self.update_status(self.tr.get("main_page.status.decoded"))
            self.update_status(self.tr.get("main_page.status.input", path=file_path))
            self.update_status(self.tr.get("main_page.status.output", path=save_path))
            if number != DEFAULT_SEED:
                self.update_status(
                    self.tr.get("main_page.status.number", number=number)
                )

        except Exception as e:
            self.update_status(self.tr.get("main_page.status.error", error=str(e)))

    def on_done(self, success, message):
        self.loader.close()
        if success:
            QtWidgets.QMessageBox.information(
                self, self.tr.get("main_page.dialogs.success"), message
            )
        else:
            QtWidgets.QMessageBox.critical(
                self, self.tr.get("main_page.dialogs.error"), message
            )

    def refresh_ui(self):
        self.title.setText(self.tr.get("main_page.title"))

        # 1. Update GroupBox titles explicitly
        self.file_group.setTitle(self.tr.get("main_page.file_selection.group_title"))
        self.seed_group.setTitle(self.tr.get("main_page.configuration.group_title"))
        self.save_group.setTitle(self.tr.get("main_page.output.group_title"))
        self.action_group.setTitle(self.tr.get("main_page.actions.group_title"))

        # 2. Update Buttons
        self.file_button.setText(self.tr.get("main_page.file_selection.button"))
        self.save_button.setText(self.tr.get("main_page.output.button"))
        self.encode_button.setText(self.tr.get("main_page.actions.encode_button"))
        self.decode_button.setText(self.tr.get("main_page.actions.decode_button"))
        self.swap_encode_decode_file_button.setText(
            self.tr.get("main_page.actions.swap_button")
        )

        # 3. Update Placeholders
        self.file_lineedit.setPlaceholderText(
            self.tr.get("main_page.file_selection.placeholder")
        )
        self.seed_input.setPlaceholderText(
            self.tr.get("main_page.configuration.placeholder", default=DEFAULT_SEED)
        )
        self.save_lineedit.setPlaceholderText(
            self.tr.get("main_page.output.placeholder")
        )
        self.status_text.setPlaceholderText(self.tr.get("main_page.status.placeholder"))

        # 4. Update Labels if they contain the default placeholder text (i.e., no file selected yet)
        if not self.file_lineedit.text():
            self.file_label.setText(self.tr.get("main_page.file_selection.no_file"))
        if not self.save_lineedit.text():
            self.save_label.setText(self.tr.get("main_page.output.no_path"))


class PageOne(QtWidgets.QWidget):
    def __init__(self, tr):
        super().__init__()
        self.tr = tr
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)

        self.label = QtWidgets.QLabel(
            self.tr.get("documentation_page.title"), alignment=QtCore.Qt.AlignCenter
        )
        self.label.setFont(QFont("Arial", 20, QFont.Bold))

        self.content = QtWidgets.QLabel(
            self.tr.get("documentation_page.content"),
            alignment=QtCore.Qt.AlignLeft,
        )
        self.content.setWordWrap(True)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.content)
        self.layout.addStretch()

    def refresh_ui(self):
        self.label.setText(self.tr.get("documentation_page.title"))
        # Note: Newlines stored as \n in JSON need to be treated as such.
        self.content.setText(
            self.tr.get("documentation_page.content").replace("\\n", "\n")
        )


class PageTwo(QtWidgets.QWidget):
    def __init__(self, tr):
        super().__init__()
        self.tr = tr
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)

        self.label = QtWidgets.QLabel(
            self.tr.get("about_page.title"), alignment=QtCore.Qt.AlignCenter
        )
        self.label.setFont(QFont("Arial", 20, QFont.Bold))

        self.content = QtWidgets.QLabel(
            self.tr.get("about_page.content"),
            alignment=QtCore.Qt.AlignLeft,
        )
        self.content.setWordWrap(True)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.content)
        self.layout.addStretch()

    def refresh_ui(self):
        self.label.setText(self.tr.get("about_page.title"))
        # Note: Newlines stored as \n in JSON need to be treated as such.
        self.content.setText(self.tr.get("about_page.content").replace("\\n", "\n"))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, tr, lang_dir):
        super().__init__()
        self.tr = tr
        self.lang_dir = lang_dir
        self.setWindowTitle(self.tr.get("window_title"))

        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()

        self.page_width = int(screen_width * 0.70)

        # Create pages
        self.main_page = MainPage(tr)
        self.page_one = PageOne(tr)
        self.page_two = PageTwo(tr)

        # Stacked widget
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.page_one)
        self.stacked_widget.addWidget(self.page_two)
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
        h_layout.addStretch(1)
        h_layout.addWidget(scroll)
        h_layout.addStretch(1)
        container_layout.addLayout(h_layout)

        self.setCentralWidget(central_container)

        menu_bar = self.menuBar()
        self.navigate_menu = menu_bar.addMenu(self.tr.get("menu.menu"))

        self.main_action = QAction(self.tr.get("menu.main_page"), self)
        self.docs_action = QAction(self.tr.get("menu.documentation"), self)
        self.about_action = QAction(self.tr.get("menu.about"), self)

        self.navigate_menu.addAction(self.main_action)
        self.navigate_menu.addAction(self.docs_action)
        self.navigate_menu.addAction(self.about_action)

        self.main_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentIndex(0)
        )
        self.docs_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentIndex(1)
        )
        self.about_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentIndex(2)
        )

        self.language_menu = menu_bar.addMenu(
            self.tr.get("language_menu")
        )  # Language menu label is fixed
        self.create_language_menu()

        self.apply_styles()

    def create_language_menu(self):
        self.language_menu.clear()

        if not os.path.exists(self.lang_dir):
            no_lang_action = QAction("No languages folder found", self)
            no_lang_action.setEnabled(False)
            self.language_menu.addAction(no_lang_action)
            return

        lang_files = [f for f in os.listdir(self.lang_dir) if f.endswith(".json")]

        if not lang_files:
            no_lang_action = QAction("No language files found", self)
            no_lang_action.setEnabled(False)
            self.language_menu.addAction(no_lang_action)
            return

        # Create action for each language file
        for lang_file in sorted(lang_files):
            lang_name = os.path.splitext(lang_file)[0].upper()
            lang_path = os.path.join(self.lang_dir, lang_file)
            abs_lang_path = os.path.abspath(lang_path)

            lang_action = QAction(lang_name, self)
            lang_action.setCheckable(True)

            if abs_lang_path == self.tr.current_lang_file:
                lang_action.setChecked(True)

            lang_action.triggered.connect(
                lambda checked, path=abs_lang_path: self.change_language(path)
            )
            self.language_menu.addAction(lang_action)

    def change_language(self, lang_file):
        try:
            self.tr.load_language(lang_file)
            self.refresh_all_ui()
            self.create_language_menu()

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Error", f"Failed to load language file:\n{str(e)}"
            )

    # "language_menu": "Мова",
    def refresh_all_ui(self):
        self.setWindowTitle(self.tr.get("window_title"))

        # Refresh main navigation menu titles
        self.navigate_menu.setTitle(self.tr.get("menu.menu"))
        self.main_action.setText(self.tr.get("menu.main_page"))
        self.docs_action.setText(self.tr.get("menu.documentation"))
        self.about_action.setText(self.tr.get("menu.about"))
        self.language_menu.setTitle(self.tr.get("language_menu"))
        # Refresh all pages
        self.main_page.refresh_ui()
        self.page_one.refresh_ui()
        self.page_two.refresh_ui()

    def apply_styles(self):
        self.setStyleSheet("""
            * {
                font-size: 20px;

                font-family: monospace;
            }
            QMainWindow {
                background-color: #ffffff;
                color: #000000;
            }
            QStackedWidget {
                background-color: #ffffff;
                border: none;
            }
            QLabel {
                color: #000000;
                padding: 5px;
            }
            #titleLabel {
                font-size: 42px;
                font-weight: bold;
            }
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
            QTextEdit {
                border: 2px solid #000000;
                border-radius: 4px;
                padding: 8px;
                background-color: #fafafa;
                color: #000000;
                font-family: 'Courier New', monospace;
                font-size: 20px;
            }
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
            QProgressDialog{
            background-color: white;
            }
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
    BASE_DIR = (
        os.path.dirname(os.path.abspath(__file__))
        if "__file__" in locals()
        else os.getcwd()
    )
    LANG_DIR = os.path.join(BASE_DIR, "languages")

    initial_lang_path = os.path.join(LANG_DIR, "uk.json")
    tr = UILanguageManager(initial_lang_path)

    window = MainWindow(tr, LANG_DIR)
    window.resize(900, 700)
    window.show()
    sys.exit(app.exec())
