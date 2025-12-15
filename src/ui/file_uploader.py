"""
Dosya yükleyici widget - Drag & drop, çoklu dosya
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QListWidget, QListWidgetItem, QLabel, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QFont
from pathlib import Path

from ..utils.constants import SUPPORTED_FILE_EXTENSIONS


class FileUploader(QWidget):
    """Dosya yükleyici widget"""
    
    files_changed = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_paths = []
        self.init_ui()
        self.setAcceptDrops(True)
    
    def init_ui(self):
        """UI oluştur"""
        layout = QVBoxLayout()
        
        # Başlık
        title = QLabel("Dosya Yükleme")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Dosya listesi
        self.file_list = QListWidget()
        self.file_list.setMaximumHeight(150)
        layout.addWidget(self.file_list)
        
        # Butonlar
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Dosya Ekle")
        self.add_btn.clicked.connect(self._add_files)
        btn_layout.addWidget(self.add_btn)
        
        self.remove_btn = QPushButton("Seçiliyi Kaldır")
        self.remove_btn.clicked.connect(self._remove_selected)
        btn_layout.addWidget(self.remove_btn)
        
        self.clear_btn = QPushButton("Tümünü Temizle")
        self.clear_btn.clicked.connect(self._clear_all)
        btn_layout.addWidget(self.clear_btn)
        
        layout.addLayout(btn_layout)
        
        # Bilgi etiketi
        self.info_label = QLabel("Dosyaları buraya sürükleyip bırakın veya 'Dosya Ekle' butonunu kullanın")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("color: #666; font-size: 9pt; padding: 5px;")
        layout.addWidget(self.info_label)
        
        self.setLayout(layout)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Drop event"""
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if self._is_supported(file_path):
                files.append(file_path)
        
        if files:
            self._add_file_paths(files)
        event.acceptProposedAction()
    
    def _is_supported(self, file_path: str) -> bool:
        """Dosya formatı destekleniyor mu?"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        for extensions in SUPPORTED_FILE_EXTENSIONS.values():
            if ext in extensions:
                return True
        
        return False
    
    def _add_files(self):
        """Dosya ekle dialog"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Dosya Seç",
            "",
            "Tüm Desteklenen Dosyalar (*.pdf *.txt *.md *.py *.js *.java *.cpp *.c *.h *.hpp *.cs *.go *.rs *.rb *.php *.html *.css *.json *.xml *.yaml *.yml *.jpg *.jpeg *.png *.gif *.bmp *.webp);;"
            "PDF Dosyaları (*.pdf);;"
            "Metin Dosyaları (*.txt *.md);;"
            "Kod Dosyaları (*.py *.js *.java *.cpp *.c *.h *.hpp *.cs *.go *.rs *.rb *.php *.html *.css *.json *.xml *.yaml *.yml);;"
            "Resim Dosyaları (*.jpg *.jpeg *.png *.gif *.bmp *.webp);;"
            "Tüm Dosyalar (*.*)"
        )
        
        if files:
            self._add_file_paths(files)
    
    def _add_file_paths(self, file_paths: list):
        """Dosya yollarını ekle"""
        for file_path in file_paths:
            if file_path not in self.file_paths:
                self.file_paths.append(file_path)
                item = QListWidgetItem(Path(file_path).name)
                item.setData(Qt.ItemDataRole.UserRole, file_path)
                self.file_list.addItem(item)
        
        self.files_changed.emit(self.file_paths.copy())
        self._update_info()
    
    def _remove_selected(self):
        """Seçili dosyayı kaldır"""
        current_item = self.file_list.currentItem()
        if current_item:
            file_path = current_item.data(Qt.ItemDataRole.UserRole)
            if file_path in self.file_paths:
                self.file_paths.remove(file_path)
            self.file_list.takeItem(self.file_list.row(current_item))
            self.files_changed.emit(self.file_paths.copy())
            self._update_info()
    
    def _clear_all(self):
        """Tüm dosyaları temizle"""
        self.file_paths.clear()
        self.file_list.clear()
        self.files_changed.emit([])
        self._update_info()
    
    def _update_info(self):
        """Bilgi etiketini güncelle"""
        count = len(self.file_paths)
        if count == 0:
            self.info_label.setText("Dosyaları buraya sürükleyip bırakın veya 'Dosya Ekle' butonunu kullanın")
        else:
            self.info_label.setText(f"{count} dosya yüklendi")
    
    def get_files(self) -> list:
        """Yüklenen dosyaları al"""
        return self.file_paths.copy()
    
    def clear_files(self):
        """Dosyaları temizle"""
        self._clear_all()

