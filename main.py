"""
Tinlera Research Tool - Ana giriş noktası
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from src.ui.main_window import MainWindow


def main():
    """Ana fonksiyon"""
    app = QApplication(sys.argv)
    app.setApplicationName("Tinlera Research Tool")
    
    # Ana pencere
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

