from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QTextEdit, QFileDialog, QMessageBox, QToolBar
)
from PySide6.QtGui import QAction, QKeySequence

class NotepadWindow(QMainWindow):
    def __init__(self, desktop, file_path=None):
        super().__init__(desktop)
        self.setWindowTitle("Блокнот HexOS")
        self.resize(700, 520)
        self.current_path = None
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Начните вводить текст...")
        self.setCentralWidget(self.editor)

        toolbar = QToolBar("Файл")
        self.addToolBar(toolbar)
        new_action = QAction("Новый", self)
        new_action.triggered.connect(self.new_file)
        open_action = QAction("Открыть", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file)
        save_action = QAction("Сохранить", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_file)
        for action in (new_action, open_action, save_action):
            toolbar.addAction(action)

        if file_path:
            self.load_path(file_path)

    def new_file(self):
        self.editor.clear()
        self.current_path = None
        self.setWindowTitle("Блокнот HexOS — новый файл")

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", str(Path.home()),
            "Текстовые файлы (*.txt *.md *.py *.json *.log);;Все файлы (*.*)"
        )
        if path:
            self.load_path(path)

    def load_path(self, path):
        try:
            self.editor.setPlainText(Path(path).read_text(encoding="utf-8"))
            self.current_path = Path(path)
            self.setWindowTitle(f"Блокнот HexOS — {self.current_path.name}")
        except (OSError, UnicodeError) as error:
            QMessageBox.warning(self, "Ошибка открытия", str(error))

    def save_file(self):
        path = self.current_path
        if path is None:
            selected, _ = QFileDialog.getSaveFileName(
                self, "Сохранить файл", str(Path.home() / "Новый документ.txt"),
                "Текстовые файлы (*.txt);;Все файлы (*.*)"
            )
            if not selected:
                return
            path = Path(selected)
        try:
            path.write_text(self.editor.toPlainText(), encoding="utf-8")
            self.current_path = path
            self.setWindowTitle(f"Блокнот HexOS — {path.name}")
        except OSError as error:
            QMessageBox.warning(self, "Ошибка сохранения", str(error))
