"""
Dosya işleme modülü - PDF, TXT, kod, resim okuma
"""
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import PyPDF2
import pdfplumber
from PIL import Image
import io


class FileProcessor:
    """Dosya işleme sınıfı"""
    
    def __init__(self):
        self.supported_extensions = {
            ".pdf": self._read_pdf,
            ".txt": self._read_text,
            ".md": self._read_text,
            ".py": self._read_text,
            ".js": self._read_text,
            ".java": self._read_text,
            ".cpp": self._read_text,
            ".c": self._read_text,
            ".h": self._read_text,
            ".hpp": self._read_text,
            ".cs": self._read_text,
            ".go": self._read_text,
            ".rs": self._read_text,
            ".rb": self._read_text,
            ".php": self._read_text,
            ".html": self._read_text,
            ".css": self._read_text,
            ".json": self._read_text,
            ".xml": self._read_text,
            ".yaml": self._read_text,
            ".yml": self._read_text,
            ".jpg": self._is_image,
            ".jpeg": self._is_image,
            ".png": self._is_image,
            ".gif": self._is_image,
            ".bmp": self._is_image,
            ".webp": self._is_image,
        }
    
    def _read_pdf(self, file_path: str) -> Tuple[str, Optional[str]]:
        """PDF dosyasını oku"""
        try:
            # Önce pdfplumber ile dene (daha iyi)
            with pdfplumber.open(file_path) as pdf:
                text_parts = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
                return "\n\n".join(text_parts), None
        except Exception as e1:
            try:
                # PyPDF2 ile dene
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text_parts = []
                    for page in pdf_reader.pages:
                        text = page.extract_text()
                        if text:
                            text_parts.append(text)
                    return "\n\n".join(text_parts), None
            except Exception as e2:
                return "", f"PDF okuma hatası: {e1}, {e2}"
    
    def _read_text(self, file_path: str) -> Tuple[str, Optional[str]]:
        """Metin dosyasını oku"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(), None
        except Exception as e:
            return "", f"Metin okuma hatası: {e}"
    
    def _is_image(self, file_path: str) -> Tuple[str, Optional[str]]:
        """Resim dosyası kontrolü"""
        try:
            img = Image.open(file_path)
            img.verify()
            return file_path, None  # Resim yolu döndür
        except Exception as e:
            return "", f"Resim okuma hatası: {e}"
    
    def process_file(self, file_path: str) -> Dict[str, any]:
        """Dosyayı işle ve içeriği döndür"""
        path = Path(file_path)
        if not path.exists():
            return {
                "success": False,
                "error": "Dosya bulunamadı",
                "type": None,
                "content": None,
                "path": file_path
            }
        
        ext = path.suffix.lower()
        
        if ext not in self.supported_extensions:
            return {
                "success": False,
                "error": f"Desteklenmeyen dosya formatı: {ext}",
                "type": None,
                "content": None,
                "path": file_path
            }
        
        reader_func = self.supported_extensions[ext]
        content, error = reader_func(str(path))
        
        if error:
            return {
                "success": False,
                "error": error,
                "type": "image" if ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"] else "text",
                "content": None,
                "path": file_path
            }
        
        # Dosya tipini belirle
        file_type = "image" if ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"] else "text"
        
        return {
            "success": True,
            "error": None,
            "type": file_type,
            "content": content,
            "path": file_path,
            "name": path.name,
            "size": path.stat().st_size
        }
    
    def process_multiple_files(self, file_paths: List[str]) -> List[Dict[str, any]]:
        """Birden fazla dosyayı işle"""
        results = []
        for file_path in file_paths:
            result = self.process_file(file_path)
            results.append(result)
        return results
    
    def format_for_prompt(self, files: List[Dict[str, any]], user_prompt: str) -> str:
        """Dosya içeriklerini prompt formatına çevir"""
        prompt_parts = [user_prompt]
        
        for file_info in files:
            if not file_info.get("success"):
                continue
            
            file_name = file_info.get("name", "Unknown")
            file_type = file_info.get("type")
            
            if file_type == "text":
                content = file_info.get("content", "")
                prompt_parts.append(f"\n\n--- {file_name} ---\n{content}\n--- End of {file_name} ---")
            elif file_type == "image":
                prompt_parts.append(f"\n\n[Resim eklendi: {file_name}]")
        
        return "\n".join(prompt_parts)

