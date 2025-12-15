"""
HuggingFace Serverless Inference API client
"""
import requests
import time
import base64
from typing import Optional, Dict, Any, List
from pathlib import Path

from ..utils.constants import HF_API_BASE_URL


class HuggingFaceAPI:
    """HuggingFace API client sınıfı"""
    
    def __init__(self, token: str, timeout: int = 60, max_retries: int = 3):
        self.token = token
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_url = HF_API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        # HuggingFace Hub InferenceClient kullan (daha güncel)
        if HF_HUB_AVAILABLE and token:
            try:
                self.inference_client = InferenceClient(token=token, timeout=timeout)
            except Exception:
                self.inference_client = None
        else:
            self.inference_client = None
    
    def _make_request(self, model: str, payload: Dict[str, Any], is_image: bool = False) -> Optional[Dict[str, Any]]:
        """API isteği yap"""
        # Router API için URL formatı kontrolü
        # Eğer router API kullanılıyorsa, format farklı olabilir
        if "router.huggingface.co" in self.base_url:
            # Router API için alternatif format denemeleri
            # Önce standart formatı dene
            url = f"{self.base_url}/{model}"
        else:
            # Eski Inference API formatı
            url = f"{self.base_url}/{model}"
        
        if is_image:
            self.headers["Content-Type"] = "application/json"
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 503:
                    # Model yükleniyor, bekle
                    wait_time = response.headers.get("X-Wait-For-Model", "10")
                    print(f"Model yükleniyor, {wait_time} saniye bekleniyor...")
                    time.sleep(int(wait_time))
                    continue
                elif response.status_code == 410:
                    # Eski endpoint kullanılıyor, router API'ye geç
                    error_msg = response.text
                    if "router.huggingface.co" in error_msg.lower():
                        # Router API'ye geçiş önerisi
                        return {"error": "API endpoint değişti. Lütfen programı güncelleyin veya ayarlardan endpoint'i kontrol edin.", "status_code": 410}
                    return {"error": error_msg, "status_code": response.status_code}
                elif response.status_code == 404:
                    # Model bulunamadı - router API formatını dene
                    if "router.huggingface.co" in self.base_url:
                        # Router API için farklı format dene
                        # Bazı modeller için farklı endpoint gerekebilir
                        return {"error": f"Model bulunamadı: {model}. Model adını kontrol edin veya Inference Endpoints kullanmayı deneyin.", "status_code": 404}
                    return {"error": f"Model bulunamadı: {model}", "status_code": 404}
                else:
                    error_msg = response.text
                    print(f"API hatası ({response.status_code}): {error_msg}")
                    return {"error": error_msg, "status_code": response.status_code}
            
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    print(f"Timeout, tekrar deneniyor ({attempt + 1}/{self.max_retries})...")
                    time.sleep(2)
                    continue
                return {"error": "Request timeout"}
            
            except Exception as e:
                print(f"İstek hatası: {e}")
                return {"error": str(e)}
        
        return {"error": "Max retries exceeded"}
    
    def _encode_image(self, image_path: str) -> str:
        """Resmi base64'e çevir"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Resim kodlama hatası: {e}")
            return ""
    
    def generate_text(self, model: str, prompt: str, parameters: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """Metin üretimi"""
        if not self.token:
            return {"error": "HuggingFace token gerekli"}
        
        # Önce InferenceClient ile dene (daha güncel)
        if self.inference_client:
            try:
                if parameters:
                    result = self.inference_client.text_generation(
                        prompt,
                        model=model,
                        max_new_tokens=parameters.get("max_new_tokens", 250),
                        temperature=parameters.get("temperature", 0.7),
                        top_p=parameters.get("top_p", 0.95),
                    )
                else:
                    result = self.inference_client.text_generation(prompt, model=model)
                
                return {"generated_text": result}
            except Exception as e:
                # InferenceClient başarısız olursa eski yönteme dön
                print(f"InferenceClient hatası, eski API deneniyor: {e}")
        
        # Eski API yöntemi
        payload = {
            "inputs": prompt,
        }
        
        if parameters:
            payload["parameters"] = parameters
        
        return self._make_request(model, payload)
    
    def generate_with_image(self, model: str, prompt: str, image_path: str, parameters: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """Resim ile metin üretimi (multimodal)"""
        if not self.token:
            return {"error": "HuggingFace token gerekli"}
        
        image_base64 = self._encode_image(image_path)
        if not image_base64:
            return {"error": "Resim kodlanamadı"}
        
        payload = {
            "inputs": {
                "image": image_base64,
                "text": prompt
            }
        }
        
        if parameters:
            payload["parameters"] = parameters
        
        return self._make_request(model, payload, is_image=True)
    
    def chat_completion(self, model: str, messages: List[Dict[str, str]], parameters: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """Chat completion formatında istek"""
        # Chat formatını düz metne çevir
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                prompt += f"System: {content}\n\n"
            elif role == "user":
                prompt += f"User: {content}\n\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n\n"
        
        prompt += "Assistant:"
        
        return self.generate_text(model, prompt, parameters)
    
    def search_models(self, query: str = "", task: str = "") -> List[Dict[str, Any]]:
        """Model arama (HuggingFace Hub API)"""
        if not self.token:
            return []
        
        try:
            url = "https://huggingface.co/api/models"
            params = {
                "search": query,
                "sort": "downloads",
                "direction": -1,
                "limit": 50
            }
            
            if task:
                params["pipeline_tag"] = task
            
            response = requests.get(
                url,
                headers={"Authorization": f"Bearer {self.token}"},
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Model arama hatası: {response.status_code}")
                return []
        
        except Exception as e:
            print(f"Model arama hatası: {e}")
            return []
    
    def get_model_info(self, model: str) -> Optional[Dict[str, Any]]:
        """Model bilgisi al"""
        if not self.token:
            return None
        
        try:
            url = f"https://huggingface.co/api/models/{model}"
            response = requests.get(
                url,
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
        
        except Exception as e:
            print(f"Model bilgisi alma hatası: {e}")
            return None

