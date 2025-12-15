"""
Model seçici widget - Dropdown + arama
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                             QLineEdit, QLabel, QPushButton, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ..utils.constants import POPULAR_MODELS
from ..core.hf_api import HuggingFaceAPI


class ModelSelector(QWidget):
    """Model seçici widget"""
    
    model_changed = pyqtSignal(str)
    model_searched = pyqtSignal(str)
    
    def __init__(self, hf_api: HuggingFaceAPI, parent=None):
        super().__init__(parent)
        self.hf_api = hf_api
        self.all_models = POPULAR_MODELS.copy()
        self.init_ui()
    
    def init_ui(self):
        """UI oluştur"""
        layout = QVBoxLayout()
        
        # Başlık
        title = QLabel("Model Seçimi")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Model dropdown
        self.model_combo = QComboBox()
        self.model_combo.addItems(self.all_models)
        self.model_combo.setEditable(True)
        self.model_combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.model_combo.currentTextChanged.connect(self._on_model_changed)
        layout.addWidget(self.model_combo)
        
        # Arama kutusu
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Model ara...")
        self.search_input.textChanged.connect(self._on_search)
        search_layout.addWidget(self.search_input)
        
        self.search_btn = QPushButton("Ara")
        self.search_btn.clicked.connect(self._do_search)
        search_layout.addWidget(self.search_btn)
        layout.addLayout(search_layout)
        
        # Model bilgisi
        self.info_label = QLabel("Model bilgisi yükleniyor...")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("color: #666; font-size: 10pt;")
        layout.addWidget(self.info_label)
        
        # Yenile butonu
        refresh_btn = QPushButton("Model Listesini Yenile")
        refresh_btn.clicked.connect(self._refresh_models)
        layout.addWidget(refresh_btn)
        
        self.setLayout(layout)
        
        # İlk model bilgisini yükle
        self._load_model_info(self.all_models[0] if self.all_models else "")
    
    def _on_model_changed(self, model: str):
        """Model değiştiğinde"""
        if model:
            self.model_changed.emit(model)
            self._load_model_info(model)
    
    def _on_search(self, text: str):
        """Arama metni değiştiğinde filtrele"""
        if not text:
            self.model_combo.clear()
            self.model_combo.addItems(self.all_models)
            return
        
        filtered = [m for m in self.all_models if text.lower() in m.lower()]
        current_text = self.model_combo.currentText()
        self.model_combo.clear()
        if filtered:
            self.model_combo.addItems(filtered)
        else:
            self.model_combo.addItem(text)  # Kullanıcı yazdığı modeli ekle
    
    def _do_search(self):
        """Model araması yap"""
        query = self.search_input.text()
        if not query:
            return
        
        self.model_searched.emit(query)
        
        # HuggingFace'den model ara
        if self.hf_api and self.hf_api.token:
            models = self.hf_api.search_models(query)
            if models:
                model_names = [m.get("id", "") for m in models[:20]]  # İlk 20
                self.model_combo.clear()
                self.model_combo.addItems(model_names)
                if model_names:
                    self.model_combo.setCurrentIndex(0)
    
    def _refresh_models(self):
        """Model listesini yenile"""
        # Popüler modelleri tekrar yükle
        self.model_combo.clear()
        self.model_combo.addItems(self.all_models)
        if self.all_models:
            self.model_combo.setCurrentIndex(0)
    
    def _load_model_info(self, model: str):
        """Model bilgisini yükle"""
        if not model or not self.hf_api or not self.hf_api.token:
            self.info_label.setText("Model bilgisi yüklenemiyor (token gerekli)")
            return
        
        self.info_label.setText("Yükleniyor...")
        
        # Async olarak yükle (basit yaklaşım)
        try:
            info = self.hf_api.get_model_info(model)
            if info:
                downloads = info.get("downloads", 0)
                tags = ", ".join(info.get("tags", [])[:5])
                self.info_label.setText(
                    f"İndirmeler: {downloads:,} | Etiketler: {tags}"
                )
            else:
                self.info_label.setText(f"Model: {model}")
        except Exception as e:
            self.info_label.setText(f"Model: {model} (bilgi yüklenemedi)")
    
    def get_selected_model(self) -> str:
        """Seçili modeli al"""
        return self.model_combo.currentText()
    
    def set_model(self, model: str):
        """Modeli ayarla"""
        index = self.model_combo.findText(model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
        else:
            self.model_combo.setCurrentText(model)

