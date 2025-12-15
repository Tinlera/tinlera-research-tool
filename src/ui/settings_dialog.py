"""
Ayarlar penceresi - Token girişi, özellik kontrolü
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QCheckBox, QGroupBox,
                             QMessageBox, QFormLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ..utils.config_manager import ConfigManager


class SettingsDialog(QDialog):
    """Ayarlar dialog"""
    
    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setWindowTitle("Ayarlar")
        self.setMinimumWidth(500)
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """UI oluştur"""
        layout = QVBoxLayout()
        
        # HuggingFace Token
        token_group = QGroupBox("HuggingFace Ayarları")
        token_layout = QFormLayout()
        
        self.token_input = QLineEdit()
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_input.setPlaceholderText("hf_...")
        token_layout.addRow("API Token:", self.token_input)
        
        self.show_token_btn = QPushButton("Göster")
        self.show_token_btn.setCheckable(True)
        self.show_token_btn.clicked.connect(self._toggle_token_visibility)
        token_layout.addRow("", self.show_token_btn)
        
        token_group.setLayout(token_layout)
        layout.addWidget(token_group)
        
        # Özellikler
        features_group = QGroupBox("Özellikler")
        features_layout = QVBoxLayout()
        
        self.web_search_cb = QCheckBox("Web Arama")
        self.web_search_cb.setToolTip("Web arama özelliğini etkinleştir/devre dışı bırak")
        features_layout.addWidget(self.web_search_cb)
        
        self.history_cb = QCheckBox("Geçmiş Kayıtları")
        self.history_cb.setToolTip("Sohbet geçmişini kaydet")
        features_layout.addWidget(self.history_cb)
        
        self.export_cb = QCheckBox("Export Özellikleri")
        self.export_cb.setToolTip("Araştırma sonuçlarını export et")
        features_layout.addWidget(self.export_cb)
        
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        # Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.save_btn = QPushButton("Kaydet")
        self.save_btn.clicked.connect(self._save_settings)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        btn_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("İptal")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def _toggle_token_visibility(self):
        """Token görünürlüğünü değiştir"""
        if self.show_token_btn.isChecked():
            self.token_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_token_btn.setText("Gizle")
        else:
            self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_token_btn.setText("Göster")
    
    def load_settings(self):
        """Ayarları yükle"""
        token = self.config_manager.get_token()
        self.token_input.setText(token)
        
        self.web_search_cb.setChecked(
            self.config_manager.get_feature_enabled("web_search")
        )
        self.history_cb.setChecked(
            self.config_manager.get_feature_enabled("history")
        )
        self.export_cb.setChecked(
            self.config_manager.get_feature_enabled("export")
        )
    
    def _save_settings(self):
        """Ayarları kaydet"""
        token = self.token_input.text().strip()
        
        if token and not token.startswith("hf_"):
            QMessageBox.warning(
                self,
                "Uyarı",
                "HuggingFace token'ı genellikle 'hf_' ile başlar. Lütfen kontrol edin."
            )
        
        self.config_manager.set_token(token)
        self.config_manager.set_feature_enabled("web_search", self.web_search_cb.isChecked())
        self.config_manager.set_feature_enabled("history", self.history_cb.isChecked())
        self.config_manager.set_feature_enabled("export", self.export_cb.isChecked())
        
        QMessageBox.information(self, "Başarılı", "Ayarlar kaydedildi!")
        self.accept()

