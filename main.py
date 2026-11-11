import sys
from PySide6.QtWidgets import QApplication
from shell.desktop import HexDesktop
from core.config import load_config

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("HexOS")
    app.setOrganizationName("HexOS Project")
    config = load_config()
    app.setStyle("Fusion")
    desktop = HexDesktop(config)
    desktop.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
