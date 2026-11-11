from apps.explorer.main import ExplorerWindow
from apps.notepad.main import NotepadWindow
from apps.calculator.main import CalculatorWindow
from apps.settings.main import SettingsWindow
from PySide6.QtCore import Qt

class AppManager:
    def __init__(self, desktop):
        self.desktop = desktop
        self.windows = []

    def launch(self, app_id, *args):
        constructors = {
            "explorer": ExplorerWindow,
            "notepad": NotepadWindow,
            "calculator": CalculatorWindow,
            "settings": SettingsWindow,
        }
        constructor = constructors.get(app_id)
        if not constructor:
            return
        window = constructor(self.desktop, *args)
        window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        window.destroyed.connect(lambda: self._forget(window))
        self.windows.append(window)
        window.show()
        window.raise_()
        window.activateWindow()

    def _forget(self, window):
        if window in self.windows:
            self.windows.remove(window)
