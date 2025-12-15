"""
Sohbet arayüzü widget - Mesaj gönderme/alma, markdown render
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QPushButton, QScrollArea, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QTextCursor
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
import re


class ChatWidget(QWidget):
    """Sohbet widget"""
    
    message_sent = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.messages = []
        self.init_ui()
    
    def init_ui(self):
        """UI oluştur"""
        layout = QVBoxLayout()
        
        # Mesaj alanı (scrollable)
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setFont(QFont("Consolas", 10))
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.chat_area)
        
        # Input alanı
        input_layout = QVBoxLayout()
        
        self.input_area = QTextEdit()
        self.input_area.setMaximumHeight(100)
        self.input_area.setPlaceholderText("Mesajınızı yazın... (Ctrl+Enter ile gönder)")
        self.input_area.setFont(QFont("Arial", 10))
        input_layout.addWidget(self.input_area)
        
        # Enter tuşu ile gönderme için custom event
        class CustomTextEdit(QTextEdit):
            def __init__(self, parent_widget):
                super().__init__()
                self.parent_widget = parent_widget
            
            def keyPressEvent(self, event):
                if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                    self.parent_widget._send_message()
                else:
                    super().keyPressEvent(event)
        
        # Yeni widget oluştur ve eskiyi değiştir
        old_input = self.input_area
        self.input_area = CustomTextEdit(self)
        self.input_area.setMaximumHeight(100)
        self.input_area.setPlaceholderText("Mesajınızı yazın... (Ctrl+Enter ile gönder)")
        self.input_area.setFont(QFont("Arial", 10))
        input_layout.removeWidget(old_input)
        old_input.deleteLater()
        input_layout.insertWidget(0, self.input_area)
        
        # Butonlar
        btn_layout = QHBoxLayout()
        
        self.send_btn = QPushButton("Gönder")
        self.send_btn.clicked.connect(self._send_message)
        self.send_btn.setStyleSheet("""
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
        btn_layout.addWidget(self.send_btn)
        
        self.clear_btn = QPushButton("Temizle")
        self.clear_btn.clicked.connect(self._clear_chat)
        btn_layout.addWidget(self.clear_btn)
        
        btn_layout.addStretch()
        input_layout.addLayout(btn_layout)
        layout.addLayout(input_layout)
        
        self.setLayout(layout)
    
    
    def _send_message(self):
        """Mesaj gönder"""
        text = self.input_area.toPlainText().strip()
        if not text:
            return
        
        self.add_user_message(text)
        self.input_area.clear()
        self.message_sent.emit(text)
    
    def add_user_message(self, text: str):
        """Kullanıcı mesajı ekle"""
        self.messages.append({"role": "user", "content": text})
        self._append_message("Kullanıcı", text, "#2196F3")
    
    def add_assistant_message(self, text: str):
        """AI mesajı ekle"""
        self.messages.append({"role": "assistant", "content": text})
        self._append_message("Asistan", text, "#4CAF50")
    
    def add_system_message(self, text: str):
        """Sistem mesajı ekle"""
        self._append_message("Sistem", text, "#FF9800")
    
    def _append_message(self, role: str, text: str, color: str):
        """Mesaj ekle (formatlanmış)"""
        cursor = self.chat_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Role başlığı
        format_role = QTextCharFormat()
        format_role.setForeground(QColor(color))
        format_role.setFontWeight(QFont.Weight.Bold)
        format_role.setFontPointSize(11)
        
        cursor.insertText(f"\n{role}:\n", format_role)
        
        # Mesaj içeriği (basit markdown desteği)
        formatted_text = self._format_text(text)
        cursor.insertHtml(formatted_text)
        
        # Scroll to bottom
        self.chat_area.setTextCursor(cursor)
        self.chat_area.ensureCursorVisible()
    
    def _format_text(self, text: str) -> str:
        """Metni formatla (basit markdown ve kod desteği)"""
        # Kod bloklarını işle
        code_pattern = r'```(\w+)?\n(.*?)```'
        
        def replace_code(match):
            lang = match.group(1) or ""
            code = match.group(2)
            
            try:
                if lang:
                    lexer = get_lexer_by_name(lang, stripall=True)
                else:
                    lexer = guess_lexer_for_filename("temp.py", code)
                formatter = HtmlFormatter(style='default', nowrap=True)
                highlighted = highlight(code, lexer, formatter)
                return f'<div style="background-color: #f4f4f4; padding: 10px; border-radius: 5px; margin: 5px 0;"><pre style="margin: 0;">{highlighted}</pre></div>'
            except:
                return f'<div style="background-color: #f4f4f4; padding: 10px; border-radius: 5px; margin: 5px 0;"><pre style="margin: 0;">{code}</pre></div>'
        
        text = re.sub(code_pattern, replace_code, text, flags=re.DOTALL)
        
        # Basit markdown
        text = text.replace('\n', '<br>')
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        text = re.sub(r'`(.*?)`', r'<code style="background-color: #f0f0f0; padding: 2px 4px; border-radius: 3px;">\1</code>', text)
        
        return text
    
    def _clear_chat(self):
        """Sohbeti temizle"""
        self.chat_area.clear()
        self.messages = []
        self.add_system_message("Sohbet temizlendi.")
    
    def get_messages(self) -> list:
        """Mesajları al"""
        return self.messages.copy()
    
    def set_messages(self, messages: list):
        """Mesajları ayarla"""
        self._clear_chat()
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                self.add_user_message(content)
            elif role == "assistant":
                self.add_assistant_message(content)

