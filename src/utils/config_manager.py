"""
Ayarlar yönetimi - JSON tabanlı config sistemi
"""
import json
import os
from pathlib import Path
from cryptography.fernet import Fernet
import base64
import hashlib

from .constants import DEFAULT_SETTINGS


class ConfigManager:
    """Ayarlar yönetim sınıfı"""
    
    def __init__(self, config_path: str = "config/settings.json"):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._key = self._get_or_create_key()
        self._cipher = Fernet(self._key)
        
    def _get_or_create_key(self) -> bytes:
        """Şifreleme anahtarı oluştur veya yükle"""
        key_file = self.config_path.parent / ".key"
        if key_file.exists():
            return key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            key_file.write_bytes(key)
            key_file.chmod(0o600)  # Sadece kullanıcı okuyabilir
            return key
    
    def _encrypt_token(self, token: str) -> str:
        """Token'ı şifrele"""
        if not token:
            return ""
        return self._cipher.encrypt(token.encode()).decode()
    
    def _decrypt_token(self, encrypted_token: str) -> str:
        """Token'ı çöz"""
        if not encrypted_token:
            return ""
        try:
            return self._cipher.decrypt(encrypted_token.encode()).decode()
        except Exception:
            return ""
    
    def load_config(self) -> dict:
        """Ayarları yükle"""
        if not self.config_path.exists():
            return DEFAULT_SETTINGS.copy()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Token'ı çöz
            if "hf_token_encrypted" in config:
                config["hf_token"] = self._decrypt_token(config["hf_token_encrypted"])
                del config["hf_token_encrypted"]
            
            # Eksik ayarları varsayılanlarla doldur
            for key, value in DEFAULT_SETTINGS.items():
                if key not in config:
                    config[key] = value
            
            return config
        except Exception as e:
            print(f"Config yükleme hatası: {e}")
            return DEFAULT_SETTINGS.copy()
    
    def save_config(self, config: dict):
        """Ayarları kaydet"""
        config_copy = config.copy()
        
        # Token'ı şifrele ve kaydet
        if "hf_token" in config_copy:
            token = config_copy.pop("hf_token")
            config_copy["hf_token_encrypted"] = self._encrypt_token(token)
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_copy, f, indent=2, ensure_ascii=False)
            
            # Dosya izinlerini kısıtla
            self.config_path.chmod(0o600)
        except Exception as e:
            print(f"Config kaydetme hatası: {e}")
    
    def get_token(self) -> str:
        """HuggingFace token'ı al"""
        config = self.load_config()
        return config.get("hf_token", "")
    
    def set_token(self, token: str):
        """HuggingFace token'ı ayarla"""
        config = self.load_config()
        config["hf_token"] = token
        self.save_config(config)
    
    def get_feature_enabled(self, feature: str) -> bool:
        """Özellik durumunu kontrol et"""
        config = self.load_config()
        return config.get("features", {}).get(feature, False)
    
    def set_feature_enabled(self, feature: str, enabled: bool):
        """Özellik durumunu ayarla"""
        config = self.load_config()
        if "features" not in config:
            config["features"] = {}
        config["features"][feature] = enabled
        self.save_config(config)
    
    def get_default_model(self) -> str:
        """Varsayılan modeli al"""
        config = self.load_config()
        return config.get("default_model", DEFAULT_SETTINGS["default_model"])
    
    def set_default_model(self, model: str):
        """Varsayılan modeli ayarla"""
        config = self.load_config()
        config["default_model"] = model
        self.save_config(config)

