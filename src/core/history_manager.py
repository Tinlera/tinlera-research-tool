"""
Geçmiş yönetimi - JSON tabanlı kayıt sistemi
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class HistoryManager:
    """Geçmiş yönetim sınıfı"""
    
    def __init__(self, history_dir: str = "data/history"):
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.history_dir / "history.json"
        self._load_history()
    
    def _load_history(self):
        """Geçmişi yükle"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"Geçmiş yükleme hatası: {e}")
                self.history = []
        else:
            self.history = []
    
    def _save_history(self):
        """Geçmişi kaydet"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Geçmiş kaydetme hatası: {e}")
    
    def add_entry(self, model: str, prompt: str, response: str, files: List[str] = None, web_search_results: List[Dict] = None) -> str:
        """Yeni kayıt ekle"""
        entry = {
            "id": f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.history)}",
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "prompt": prompt,
            "response": response,
            "files": files or [],
            "web_search_results": web_search_results or []
        }
        
        self.history.append(entry)
        self._save_history()
        return entry["id"]
    
    def get_entry(self, entry_id: str) -> Optional[Dict]:
        """Kayıt al"""
        for entry in self.history:
            if entry.get("id") == entry_id:
                return entry
        return None
    
    def get_all_entries(self) -> List[Dict]:
        """Tüm kayıtları al"""
        return self.history.copy()
    
    def search_entries(self, query: str) -> List[Dict]:
        """Kayıtları ara"""
        query_lower = query.lower()
        results = []
        
        for entry in self.history:
            if (query_lower in entry.get("prompt", "").lower() or 
                query_lower in entry.get("response", "").lower()):
                results.append(entry)
        
        return results
    
    def filter_by_model(self, model: str) -> List[Dict]:
        """Modele göre filtrele"""
        return [entry for entry in self.history if entry.get("model") == model]
    
    def filter_by_date(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Tarihe göre filtrele"""
        results = []
        
        for entry in self.history:
            timestamp = entry.get("timestamp", "")
            if not timestamp:
                continue
            
            if start_date and timestamp < start_date:
                continue
            if end_date and timestamp > end_date:
                continue
            
            results.append(entry)
        
        return results
    
    def delete_entry(self, entry_id: str) -> bool:
        """Kayıt sil"""
        for i, entry in enumerate(self.history):
            if entry.get("id") == entry_id:
                del self.history[i]
                self._save_history()
                return True
        return False
    
    def clear_history(self):
        """Tüm geçmişi temizle"""
        self.history = []
        self._save_history()
    
    def get_statistics(self) -> Dict:
        """İstatistikler"""
        if not self.history:
            return {
                "total_entries": 0,
                "models_used": [],
                "total_files": 0
            }
        
        models = set()
        total_files = 0
        
        for entry in self.history:
            models.add(entry.get("model", "Unknown"))
            total_files += len(entry.get("files", []))
        
        return {
            "total_entries": len(self.history),
            "models_used": list(models),
            "total_files": total_files
        }

