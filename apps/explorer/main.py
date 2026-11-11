from PySide6.QtCore import QDir
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QFileSystemModel, QTreeView, QMessageBox
)

class ExplorerWindow(QMainWindow):
    def __init__(self, desktop, start_path=None):
        super().__init__(desktop)
        self.setWindowTitle("Проводник HexOS")
        self.resize(850, 560)
        self.setMinimumSize(500, 350)

        central = QWidget()
        layout = QVBoxLayout(central)
        bar = QHBoxLayout()
        self.path = QLineEdit(start_path or str(QDir.homePath()))
        self.path.returnPressed.connect(self.navigate)
        go = QPushButton("Перейти")
        go.clicked.connect(self.navigate)
        home = QPushButton("Домой")
        home.clicked.connect(lambda: self.set_path(QDir.homePath()))
        bar.addWidget(self.path, 1)
        bar.addWidget(go)
        bar.addWidget(home)
        layout.addLayout(bar)

        self.model = QFileSystemModel(self)
        self.model.setRootPath(QDir.rootPath())
        self.model.setReadOnly(True)
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.path.text()))
        self.tree.doubleClicked.connect(self.open_item)
        layout.addWidget(self.tree)
        self.setCentralWidget(central)

    def set_path(self, path):
        self.path.setText(path)
        self.navigate()

    def navigate(self):
        path = self.path.text()
        index = self.model.index(path)
        if not index.isValid():
            QMessageBox.warning(self, "HexOS Explorer", "Папка не найдена.")
            return
        self.tree.setRootIndex(index)

    def open_item(self, index):
        path = self.model.filePath(index)
        if self.model.isDir(index):
            self.path.setText(path)
            self.tree.setRootIndex(self.model.index(path))
        else:
            import os
            try:
                os.startfile(path)
            except OSError as error:
                QMessageBox.warning(self, "Не удалось открыть файл", str(error))
