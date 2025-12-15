"""
Web arama modülü - DuckDuckGo entegrasyonu
"""
from typing import List, Dict, Optional
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS


class WebSearch:
    """Web arama sınıfı"""
    
    def __init__(self):
        self.ddgs = DDGS()
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Web araması yap"""
        try:
            results = []
            search_results = self.ddgs.text(query, max_results=max_results)
            
            for result in search_results:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "")
                })
            
            return results
        
        except Exception as e:
            print(f"Web arama hatası: {e}")
            return []
    
    def format_results(self, results: List[Dict[str, str]]) -> str:
        """Arama sonuçlarını formatla"""
        if not results:
            return "Arama sonucu bulunamadı."
        
        formatted = "Web Arama Sonuçları:\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. {result['title']}\n"
            formatted += f"   URL: {result['url']}\n"
            formatted += f"   {result['snippet']}\n\n"
        
        return formatted
    
    def get_sources(self, results: List[Dict[str, str]]) -> List[str]:
        """Kaynak URL'lerini al"""
        return [result['url'] for result in results if result.get('url')]

