from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QColorDialog,
    QHBoxLayout
)
from PySide6.QtGui import QColor

class SettingsWindow(QMainWindow):
    def __init__(self, desktop):
        super().__init__(desktop)
        self.desktop = desktop
        self.setWindowTitle("Параметры HexOS")
        self.resize(520, 390)
        central = QWidget()
        layout = QVBoxLayout(central)
        title = QLabel("Параметры")
        title.setStyleSheet("font-size: 22pt; font-weight: 600;")
        layout.addWidget(title)
        layout.addWidget(QLabel("Персонализация"))
        layout.addWidget(QLabel("Выберите основной акцентный цвет HexOS."))
        row = QHBoxLayout()
        color_button = QPushButton("Выбрать цвет")
        color_button.clicked.connect(self.choose_color)
        row.addWidget(color_button)
        row.addStretch()
        layout.addLayout(row)
        layout.addSpacing(20)
        layout.addWidget(QLabel("О системе"))
        layout.addWidget(QLabel("HexOS Desktop · 0.2 Preview"))
        layout.addWidget(QLabel("Среда рабочего стола на Python и PySide6"))
        layout.addStretch()
        self.setCentralWidget(central)

    def choose_color(self):
        current = QColor(self.desktop.config.get("accent", "#2878E8"))
        color = QColorDialog.getColor(current, self, "Цвет HexOS")
        if color.isValid():
            self.desktop.config["accent"] = color.name()
            self.desktop.apply_config(self.desktop.config)
