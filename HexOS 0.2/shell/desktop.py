from PySide6.QtCore import Qt, QTimer, QTime, QDate
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QBrush, QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
    QMenu, QLineEdit, QGraphicsDropShadowEffect, QSizePolicy
)
from core.app_manager import AppManager
from core.config import save_config

class DesktopWallpaper(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#071A43"))
        gradient.setColorAt(0.48, QColor("#123D91"))
        gradient.setColorAt(1, QColor("#050D25"))
        painter.fillRect(self.rect(), QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(40, 115, 245, 75))
        painter.drawEllipse(self.width() * 0.45, -self.height() * 0.28,
                            self.width() * 0.7, self.height() * 0.85)
        painter.setBrush(QColor(35, 90, 210, 55))
        painter.drawEllipse(-self.width() * 0.12, self.height() * 0.48,
                            self.width() * 0.72, self.height() * 0.72)

class HexDesktop(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle("HexOS")
        self.resize(1280, 800)
        self.setMinimumSize(900, 600)
        self.setWindowFlags(Qt.WindowType.Window)
        self.apps = AppManager(self)

        self.wallpaper = DesktopWallpaper(self)
        self.wallpaper.setGeometry(self.rect())
        self.wallpaper.lower()

        self.taskbar = QFrame(self)
        self.taskbar.setObjectName("Taskbar")
        self.taskbar.setFixedHeight(58)
        self.taskbar_layout = QHBoxLayout(self.taskbar)
        self.taskbar_layout.setContentsMargins(14, 6, 14, 6)
        self.taskbar_layout.setSpacing(8)

        self.start_button = QPushButton("⬡")
        self.start_button.setObjectName("StartButton")
        self.start_button.setFixedSize(44, 42)
        self.start_button.clicked.connect(self.show_start_menu)

        self.search_button = QPushButton("⌕")
        self.search_button.setFixedSize(42, 42)
        self.search_button.setToolTip("Поиск приложений")
        self.search_button.clicked.connect(self.show_start_menu)

        self.taskbar_layout.addWidget(self.start_button)
        self.taskbar_layout.addWidget(self.search_button)
        self.taskbar_layout.addSpacing(10)

        self.explorer_button = self._task_button("📁", "Проводник", "explorer")
        self.notepad_button = self._task_button("📝", "Блокнот", "notepad")
        self.calc_button = self._task_button("▦", "Калькулятор", "calculator")
        self.settings_button = self._task_button("⚙", "Параметры", "settings")

        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.clock.setMinimumWidth(100)
        self.taskbar_layout.addStretch()
        self.taskbar_layout.addWidget(self.clock)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()

        self.start_menu = QFrame(self)
        self.start_menu.setObjectName("StartMenu")
        self.start_menu.setFixedSize(390, 470)
        self.start_menu.hide()
        self._build_start_menu()

        self._apply_style()
        self._place_taskbar()

        # Desktop shortcuts
        self._shortcut("📁", "Проводник", "explorer", 28, 28)
        self._shortcut("📝", "Блокнот", "notepad", 28, 125)
        self._shortcut("▦", "Калькулятор", "calculator", 28, 222)
        self._shortcut("⚙", "Параметры", "settings", 28, 319)

    def _task_button(self, icon, label, app_id):
        button = QPushButton(icon)
        button.setFixedSize(42, 42)
        button.setToolTip(label)
        button.clicked.connect(lambda: self.apps.launch(app_id))
        self.taskbar_layout.addWidget(button)
        return button

    def _shortcut(self, icon, label, app_id, x, y):
        button = QPushButton(f"{icon}\n{label}", self)
        button.setObjectName("DesktopShortcut")
        button.setGeometry(x, y, 92, 82)
        button.setToolTip(f"Открыть: {label}")
        button.clicked.connect(lambda: self.apps.launch(app_id))
        button.show()

    def _build_start_menu(self):
        layout = QVBoxLayout(self.start_menu)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        heading = QLabel("HexOS")
        heading.setObjectName("StartHeading")
        layout.addWidget(heading)

        search = QLineEdit()
        search.setPlaceholderText("Поиск приложений...")
        layout.addWidget(search)

        self.start_apps = []
        entries = [
            ("📁  Проводник", "explorer"),
            ("📝  Блокнот", "notepad"),
            ("▦  Калькулятор", "calculator"),
            ("⚙  Параметры", "settings"),
        ]
        for label, app_id in entries:
            button = QPushButton(label)
            button.setMinimumHeight(43)
            button.clicked.connect(lambda checked=False, a=app_id: self._launch_from_start(a))
            layout.addWidget(button)
            self.start_apps.append((button, label.lower()))

        search.textChanged.connect(
            lambda text: [
                button.setVisible(text.lower() in label)
                for button, label in self.start_apps
            ]
        )
        layout.addStretch()
        footer = QLabel("HexOS Desktop · 0.2 Preview")
        footer.setObjectName("Muted")
        layout.addWidget(footer)

    def _launch_from_start(self, app_id):
        self.start_menu.hide()
        self.apps.launch(app_id)

    def show_start_menu(self):
        if self.start_menu.isVisible():
            self.start_menu.hide()
        else:
            self.start_menu.move(12, self.height() - self.taskbar.height() - self.start_menu.height() - 10)
            self.start_menu.show()
            self.start_menu.raise_()

    def _place_taskbar(self):
        self.taskbar.setGeometry(0, self.height() - 58, self.width(), 58)
        self.taskbar.raise_()

    def update_clock(self):
        self.clock.setText(QTime.currentTime().toString("HH:mm") + "\n" +
                           QDate.currentDate().toString("dd.MM.yyyy"))

    def resizeEvent(self, event):
        self.wallpaper.setGeometry(self.rect())
        self._place_taskbar()
        if self.start_menu.isVisible():
            self.start_menu.move(12, self.height() - self.taskbar.height() - self.start_menu.height() - 10)
        super().resizeEvent(event)

    def _apply_style(self):
        accent = self.config.get("accent", "#2878E8")
        self.setStyleSheet(f"""
            QWidget {{ color: #F4F7FF; font-family: 'Segoe UI'; font-size: 10pt; }}
            QFrame#Taskbar {{
                background: rgba(12, 19, 39, 225);
                border-top: 1px solid rgba(255,255,255,35px);
            }}
            QFrame#StartMenu {{
                background: rgba(19, 27, 48, 248);
                border: 1px solid rgba(255,255,255,45);
                border-radius: 16px;
            }}
            QPushButton {{
                background: rgba(255,255,255,20);
                border: 1px solid rgba(255,255,255,20);
                border-radius: 9px;
                padding: 7px 12px;
            }}
            QPushButton:hover {{ background: {accent}; }}
            QPushButton#StartButton {{
                background: {accent}; font-size: 21pt; font-weight: bold;
            }}
            QPushButton#DesktopShortcut {{
                background: transparent; border: none; font-size: 10pt;
                padding: 4px;
            }}
            QPushButton#DesktopShortcut:hover {{
                background: rgba(255,255,255,35); border: 1px solid rgba(255,255,255,35);
            }}
            QLabel#StartHeading {{ font-size: 19pt; font-weight: 600; }}
            QLabel#Muted {{ color: #AAB7D0; }}
            QLineEdit {{
                background: rgba(255,255,255,18); border: 1px solid rgba(255,255,255,40);
                border-radius: 8px; padding: 9px;
            }}
        """)

    def apply_config(self, config):
        self.config = config
        save_config(config)
        self._apply_style()
        self.update()
