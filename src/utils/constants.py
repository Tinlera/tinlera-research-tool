"""
Sabitler ve varsayılan değerler
"""

# Popüler HuggingFace modelleri
POPULAR_MODELS = [
    "meta-llama/Llama-3.1-8B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.2",
    "google/gemma-7b-it",
    "Qwen/Qwen2.5-7B-Instruct",
    "microsoft/Phi-3-mini-4k-instruct",
    "meta-llama/Llama-3-8B-Instruct",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "google/gemma-2b-it",
    "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
    "HuggingFaceH4/zephyr-7b-beta",
]

# Multimodal modeller
MULTIMODAL_MODELS = [
    "llava-hf/llava-1.5-7b-hf",
    "microsoft/kosmos-2-patch14-224",
    "Salesforce/blip-image-captioning-base",
]

# Vision modelleri
VISION_MODELS = [
    "google/vit-base-patch16-224",
    "microsoft/swin-base-patch4-window7-224",
]

# Desteklenen dosya formatları
SUPPORTED_FILE_EXTENSIONS = {
    "text": [".txt", ".md", ".py", ".js", ".java", ".cpp", ".c", ".h", ".hpp", ".cs", ".go", ".rs", ".rb", ".php", ".html", ".css", ".json", ".xml", ".yaml", ".yml"],
    "pdf": [".pdf"],
    "image": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
}

# HuggingFace API endpoint
HF_API_BASE_URL = "https://router.huggingface.co/models"

# Varsayılan ayarlar
DEFAULT_SETTINGS = {
    "hf_token": "",
    "default_model": "meta-llama/Llama-3.1-8B-Instruct",
    "features": {
        "web_search": True,
        "history": True,
        "export": True,
    },
    "api_timeout": 60,
    "max_retries": 3,
}

