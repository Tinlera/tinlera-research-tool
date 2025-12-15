"""
Ana pencere - Main window
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QMenuBar, QStatusBar, QSplitter,
                             QMessageBox, QFileDialog, QDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QFont

from .model_selector import ModelSelector
from .file_uploader import FileUploader
from .chat_widget import ChatWidget
from .settings_dialog import SettingsDialog
from ..core.hf_api import HuggingFaceAPI
from ..core.file_processor import FileProcessor
from ..core.web_search import WebSearch
from ..core.history_manager import HistoryManager
from ..core.export_manager import ExportManager
from ..utils.config_manager import ConfigManager


class ResearchThread(QThread):
    """Araştırma thread'i"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, hf_api, model, prompt, files, web_search_enabled):
        super().__init__()
        self.hf_api = hf_api
        self.model = model
        self.prompt = prompt
        self.files = files
        self.web_search_enabled = web_search_enabled
        self.file_processor = FileProcessor()
        self.web_search = WebSearch()
    
    def run(self):
        """Thread çalıştır"""
        try:
            # Dosyaları işle
            processed_files = []
            image_files = []
            
            if self.files:
                file_results = self.file_processor.process_multiple_files(self.files)
                for result in file_results:
                    if result.get("success"):
                        if result.get("type") == "image":
                            image_files.append(result.get("path"))
                        else:
                            processed_files.append(result)
            
            # Prompt'u hazırla
            final_prompt = self.prompt
            if processed_files:
                final_prompt = self.file_processor.format_for_prompt(processed_files, self.prompt)
            
            # Web arama (opsiyonel)
            web_results = []
            if self.web_search_enabled and not image_files:
                search_results = self.web_search.search(self.prompt, max_results=5)
                if search_results:
                    web_results = search_results
                    search_text = self.web_search.format_results(search_results)
                    final_prompt = f"{final_prompt}\n\nWeb Arama Sonuçları:\n{search_text}"
            
            # API çağrısı
            if image_files:
                # Multimodal model kullan
                if len(image_files) == 1:
                    response = self.hf_api.generate_with_image(
                        self.model,
                        final_prompt,
                        image_files[0]
                    )
                else:
                    # İlk resmi kullan
                    response = self.hf_api.generate_with_image(
                        self.model,
                        final_prompt,
                        image_files[0]
                    )
            else:
                # Text generation
                messages = [{"role": "user", "content": final_prompt}]
                response = self.hf_api.chat_completion(self.model, messages)
            
            if response and "error" not in response:
                # Response'u çıkar
                if isinstance(response, list) and len(response) > 0:
                    result_text = response[0].get("generated_text", str(response))
                elif isinstance(response, dict):
                    result_text = response.get("generated_text", response.get("text", str(response)))
                else:
                    result_text = str(response)
                
                self.finished.emit(result_text)
            else:
                error_msg = response.get("error", "Bilinmeyen hata") if isinstance(response, dict) else "API hatası"
                self.error.emit(error_msg)
        
        except Exception as e:
            self.error.emit(f"Hata: {str(e)}")


class MainWindow(QMainWindow):
    """Ana pencere"""
    
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.hf_api = None
        self.file_processor = FileProcessor()
        self.web_search = WebSearch()
        self.history_manager = HistoryManager()
        self.export_manager = ExportManager()
        
        self.current_files = []
        self.web_search_enabled = True
        self.history_enabled = True
        self.export_enabled = True
        
        self.init_ui()
        self.load_config()
        self.setWindowTitle("Tinlera Research Tool")
        self.setMinimumSize(1000, 700)
    
    def init_ui(self):
        """UI oluştur"""
        # Menü çubuğu
        menubar = self.menuBar()
        
        # Dosya menüsü
        file_menu = menubar.addMenu("Dosya")
        
        export_action = QAction("Export", self)
        export_action.triggered.connect(self._export_research)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Çıkış", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Ayarlar menüsü
        settings_menu = menubar.addMenu("Ayarlar")
        
        settings_action = QAction("Ayarlar", self)
        settings_action.triggered.connect(self._show_settings)
        settings_menu.addAction(settings_action)
        
        # Geçmiş menüsü
        history_menu = menubar.addMenu("Geçmiş")
        
        view_history_action = QAction("Geçmişi Görüntüle", self)
        view_history_action.triggered.connect(self._view_history)
        history_menu.addAction(view_history_action)
        
        clear_history_action = QAction("Geçmişi Temizle", self)
        clear_history_action.triggered.connect(self._clear_history)
        history_menu.addAction(clear_history_action)
        
        # Yardım menüsü
        help_menu = menubar.addMenu("Yardım")
        
        about_action = QAction("Hakkında", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
        # Merkezi widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Özellik toggle butonları
        toggle_layout = QHBoxLayout()
        
        self.web_search_toggle = QPushButton("🔍 Web Arama: Açık")
        self.web_search_toggle.setCheckable(True)
        self.web_search_toggle.setChecked(True)
        self.web_search_toggle.clicked.connect(self._toggle_web_search)
        toggle_layout.addWidget(self.web_search_toggle)
        
        self.history_toggle = QPushButton("📝 Geçmiş: Açık")
        self.history_toggle.setCheckable(True)
        self.history_toggle.setChecked(True)
        self.history_toggle.clicked.connect(self._toggle_history)
        toggle_layout.addWidget(self.history_toggle)
        
        self.export_toggle = QPushButton("💾 Export: Açık")
        self.export_toggle.setCheckable(True)
        self.export_toggle.setChecked(True)
        self.export_toggle.clicked.connect(self._toggle_export)
        toggle_layout.addWidget(self.export_toggle)
        
        toggle_layout.addStretch()
        main_layout.addLayout(toggle_layout)
        
        # Splitter (yan yana)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Sol panel
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Model seçici (placeholder, sonra gerçek widget eklenecek)
        self.model_selector = ModelSelector(None, self)
        left_layout.addWidget(self.model_selector)
        
        # Dosya yükleyici
        self.file_uploader = FileUploader(self)
        self.file_uploader.files_changed.connect(self._on_files_changed)
        left_layout.addWidget(self.file_uploader)
        
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(400)
        splitter.addWidget(left_panel)
        
        # Sağ panel (sohbet)
        self.chat_widget = ChatWidget(self)
        self.chat_widget.message_sent.connect(self._on_message_sent)
        splitter.addWidget(self.chat_widget)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar().showMessage("Hazır")
    
    def load_config(self):
        """Config yükle"""
        token = self.config_manager.get_token()
        if token:
            self.hf_api = HuggingFaceAPI(token)
            self.model_selector.hf_api = self.hf_api
        
        self.web_search_enabled = self.config_manager.get_feature_enabled("web_search")
        self.history_enabled = self.config_manager.get_feature_enabled("history")
        self.export_enabled = self.config_manager.get_feature_enabled("export")
        
        self.web_search_toggle.setChecked(self.web_search_enabled)
        self.history_toggle.setChecked(self.history_enabled)
        self.export_toggle.setChecked(self.export_enabled)
        
        self._update_toggle_buttons()
    
    def _update_toggle_buttons(self):
        """Toggle butonlarını güncelle"""
        self.web_search_toggle.setText(
            f"🔍 Web Arama: {'Açık' if self.web_search_enabled else 'Kapalı'}"
        )
        self.history_toggle.setText(
            f"📝 Geçmiş: {'Açık' if self.history_enabled else 'Kapalı'}"
        )
        self.export_toggle.setText(
            f"💾 Export: {'Açık' if self.export_enabled else 'Kapalı'}"
        )
    
    def _toggle_web_search(self):
        """Web arama toggle"""
        self.web_search_enabled = self.web_search_toggle.isChecked()
        self.config_manager.set_feature_enabled("web_search", self.web_search_enabled)
        self._update_toggle_buttons()
    
    def _toggle_history(self):
        """Geçmiş toggle"""
        self.history_enabled = self.history_toggle.isChecked()
        self.config_manager.set_feature_enabled("history", self.history_enabled)
        self._update_toggle_buttons()
    
    def _toggle_export(self):
        """Export toggle"""
        self.export_enabled = self.export_toggle.isChecked()
        self.config_manager.set_feature_enabled("export", self.export_enabled)
        self._update_toggle_buttons()
    
    def _on_files_changed(self, files):
        """Dosyalar değiştiğinde"""
        self.current_files = files
    
    def _on_message_sent(self, message: str):
        """Mesaj gönderildiğinde"""
        if not self.hf_api or not self.hf_api.token:
            QMessageBox.warning(
                self,
                "Uyarı",
                "Lütfen önce HuggingFace token'ınızı ayarlardan girin."
            )
            return
        
        model = self.model_selector.get_selected_model()
        if not model:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir model seçin.")
            return
        
        # Thread başlat
        self.statusBar().showMessage("Araştırma yapılıyor...")
        self.chat_widget.send_btn.setEnabled(False)
        
        self.research_thread = ResearchThread(
            self.hf_api,
            model,
            message,
            self.current_files,
            self.web_search_enabled
        )
        self.research_thread.finished.connect(self._on_research_finished)
        self.research_thread.error.connect(self._on_research_error)
        self.research_thread.start()
    
    def _on_research_finished(self, response: str):
        """Araştırma tamamlandığında"""
        self.chat_widget.add_assistant_message(response)
        self.statusBar().showMessage("Hazır")
        self.chat_widget.send_btn.setEnabled(True)
        
        # Geçmişe kaydet
        if self.history_enabled:
            model = self.model_selector.get_selected_model()
            web_results = []
            if self.web_search_enabled:
                web_results = self.web_search.search(self.chat_widget.messages[-2]["content"], max_results=5)
            
            self.history_manager.add_entry(
                model,
                self.chat_widget.messages[-2]["content"],
                response,
                self.current_files,
                web_results
            )
    
    def _on_research_error(self, error: str):
        """Araştırma hatası"""
        self.chat_widget.add_system_message(f"Hata: {error}")
        self.statusBar().showMessage("Hata oluştu")
        self.chat_widget.send_btn.setEnabled(True)
    
    def _show_settings(self):
        """Ayarlar penceresini göster"""
        dialog = SettingsDialog(self.config_manager, self)
        if dialog.exec():
            # Config'i yeniden yükle
            self.load_config()
    
    def _view_history(self):
        """Geçmişi görüntüle"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QTextEdit, QPushButton
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Geçmiş")
        dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        
        # Liste
        history_list = QListWidget()
        entries = self.history_manager.get_all_entries()
        for entry in entries:
            timestamp = entry.get("timestamp", "")[:19]  # İlk 19 karakter
            model = entry.get("model", "Unknown")
            prompt = entry.get("prompt", "")[:50]  # İlk 50 karakter
            history_list.addItem(f"{timestamp} | {model} | {prompt}...")
        
        layout.addWidget(history_list)
        
        # Detay
        detail_text = QTextEdit()
        detail_text.setReadOnly(True)
        layout.addWidget(detail_text)
        
        def show_detail():
            current = history_list.currentRow()
            if current >= 0:
                entry = entries[current]
                detail = f"Tarih: {entry.get('timestamp')}\n"
                detail += f"Model: {entry.get('model')}\n\n"
                detail += f"Soru:\n{entry.get('prompt')}\n\n"
                detail += f"Yanıt:\n{entry.get('response')}"
                detail_text.setPlainText(detail)
        
        history_list.currentRowChanged.connect(show_detail)
        
        # Butonlar
        btn_layout = QHBoxLayout()
        load_btn = QPushButton("Yükle")
        load_btn.clicked.connect(lambda: self._load_from_history(entries[history_list.currentRow()] if history_list.currentRow() >= 0 else None))
        btn_layout.addWidget(load_btn)
        
        btn_layout.addStretch()
        close_btn = QPushButton("Kapat")
        close_btn.clicked.connect(dialog.close)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def _load_from_history(self, entry):
        """Geçmişten yükle"""
        if not entry:
            return
        
        # Mesajları yükle
        messages = [
            {"role": "user", "content": entry.get("prompt", "")},
            {"role": "assistant", "content": entry.get("response", "")}
        ]
        self.chat_widget.set_messages(messages)
        
        # Dosyaları yükle
        files = entry.get("files", [])
        if files:
            self.file_uploader._add_file_paths(files)
    
    def _clear_history(self):
        """Geçmişi temizle"""
        reply = QMessageBox.question(
            self,
            "Onay",
            "Tüm geçmişi silmek istediğinize emin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.history_manager.clear_history()
            QMessageBox.information(self, "Başarılı", "Geçmiş temizlendi.")
    
    def _export_research(self):
        """Araştırmayı export et"""
        if not self.export_enabled:
            QMessageBox.warning(self, "Uyarı", "Export özelliği kapalı.")
            return
        
        if not self.chat_widget.messages:
            QMessageBox.warning(self, "Uyarı", "Export edilecek mesaj yok.")
            return
        
        # Son mesajı export et
        if len(self.chat_widget.messages) >= 2:
            user_msg = self.chat_widget.messages[-2]
            assistant_msg = self.chat_widget.messages[-1]
            
            # Geçmişten web search sonuçlarını al
            web_results = []
            if self.history_manager.history:
                last_entry = self.history_manager.history[-1]
                web_results = last_entry.get("web_search_results", [])
            
            entry = {
                "timestamp": self.history_manager.history[-1]["timestamp"] if self.history_manager.history else "",
                "model": self.model_selector.get_selected_model(),
                "prompt": user_msg.get("content", ""),
                "response": assistant_msg.get("content", ""),
                "files": self.current_files,
                "web_search_results": web_results
            }
            
            # Format seç dialog
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
            
            format_dialog = QDialog(self)
            format_dialog.setWindowTitle("Export Formatı Seç")
            format_dialog.setMinimumWidth(300)
            
            layout = QVBoxLayout()
            layout.addWidget(QLabel("Export formatını seçin:"))
            
            selected_format = {"format": "txt"}
            
            def select_txt():
                selected_format["format"] = "txt"
                format_dialog.accept()
            
            def select_md():
                selected_format["format"] = "markdown"
                format_dialog.accept()
            
            def select_docx():
                selected_format["format"] = "docx"
                format_dialog.accept()
            
            txt_btn = QPushButton("TXT (Metin Dosyası)")
            txt_btn.clicked.connect(select_txt)
            layout.addWidget(txt_btn)
            
            md_btn = QPushButton("Markdown")
            md_btn.clicked.connect(select_md)
            layout.addWidget(md_btn)
            
            docx_btn = QPushButton("DOCX (Word Belgesi)")
            docx_btn.clicked.connect(select_docx)
            layout.addWidget(docx_btn)
            
            cancel_btn = QPushButton("İptal")
            cancel_btn.clicked.connect(format_dialog.reject)
            layout.addWidget(cancel_btn)
            
            format_dialog.setLayout(layout)
            
            if format_dialog.exec():
                format_type = selected_format["format"]
                try:
                    if format_type == "txt":
                        filepath = self.export_manager.export_to_txt(entry)
                    elif format_type == "markdown":
                        filepath = self.export_manager.export_to_markdown(entry)
                    else:
                        filepath = self.export_manager.export_to_docx(entry)
                    
                    QMessageBox.information(
                        self,
                        "Başarılı",
                        f"Dosya kaydedildi:\n{filepath}"
                    )
                except Exception as e:
                    QMessageBox.critical(self, "Hata", f"Export hatası: {str(e)}")
    
    def _show_about(self):
        """Hakkında"""
        QMessageBox.about(
            self,
            "Hakkında",
            "Tinlera Research Tool\n\n"
            "Bu program HuggingFace modelleri ile kapsamlı araştırma yapmanızı sağlar.\n\n"
            "Özellikler:\n"
            "- Model seçimi ve arama\n"
            "- Dosya ve resim yükleme\n"
            "- Web arama entegrasyonu\n"
            "- Geçmiş kayıtları\n"
            "- Export özellikleri"
        )

