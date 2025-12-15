# Tinlera Research Tool

**Tinlera Research Tool**, HuggingFace modelleri ile kapsamlı araştırma yapmanızı sağlayan, PyQt6 tabanlı modern bir masaüstü uygulamasıdır. Dosya yükleme, web arama, geçmiş kayıtları ve export özellikleri ile profesyonel araştırma deneyimi sunar.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 İçindekiler

- [Ne İşe Yarar?](#ne-işe-yarar)
- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Ekran Görüntüleri](#ekran-görüntüleri)
- [Teknik Detaylar](#teknik-detaylar)
- [Katkıda Bulunma](#katkıda-bulunma)
- [Lisans](#lisans)

## 🎯 Ne İşe Yarar?

Tinlera Research Tool, araştırmacılar, öğrenciler ve profesyoneller için tasarlanmış kapsamlı bir araştırma asistanıdır:

- **AI Destekli Araştırma**: HuggingFace'in güçlü modelleri ile sorularınıza detaylı yanıtlar alın
- **Dosya Analizi**: PDF, kod dosyaları, metin belgeleri ve resimleri yükleyip analiz ettirin
- **Web Entegrasyonu**: Gerçek zamanlı web araması ile güncel bilgilere erişin
- **Geçmiş Yönetimi**: Tüm araştırmalarınızı kaydedin, görüntüleyin ve tekrar kullanın
- **Export Özellikleri**: Araştırma sonuçlarınızı TXT, Markdown veya DOCX formatında export edin

## ✨ Özellikler

### 🤖 Model Seçimi
- **Dropdown Menü**: Popüler HuggingFace modellerini kolayca seçin
- **Arama Özelliği**: Tüm HuggingFace modellerini arayın ve filtreleyin
- **Model Bilgisi**: Seçtiğiniz model hakkında detaylı bilgi görüntüleyin

### 📄 Dosya Yükleme
- **Drag & Drop**: Dosyaları sürükleyip bırakarak yükleyin
- **Çoklu Format Desteği**:
  - **PDF**: Araştırma makaleleri, raporlar
  - **Metin**: TXT, Markdown dosyaları
  - **Kod**: Python, JavaScript, Java, C++, Go, Rust ve daha fazlası
  - **Resim**: JPG, PNG, GIF, WebP (multimodal modeller için)
- **Önizleme**: Yüklenen dosyaları görüntüleyin ve yönetin

### 🔍 Web Arama
- **DuckDuckGo Entegrasyonu**: Gerçek zamanlı web araması
- **Otomatik Özetleme**: Arama sonuçları otomatik olarak özetlenir
- **Kaynak Referansları**: Tüm kaynaklar export edilir

### 📝 Geçmiş Yönetimi
- **Otomatik Kayıt**: Tüm araştırmalarınız otomatik kaydedilir
- **Arama ve Filtreleme**: Geçmişte arama yapın
- **Devam Etme**: Önceki araştırmalarınızdan devam edin

### 💾 Export
- **TXT**: Düz metin formatı
- **Markdown**: Markdown formatı (GitHub uyumlu)
- **DOCX**: Microsoft Word belgesi
- **Kaynak Referansları**: Tüm kaynaklar export edilir

### ⚙️ Özelleştirilebilir
- **Toggle Özellikler**: Web arama, geçmiş ve export özelliklerini açıp kapatın
- **Güvenli Token Saklama**: HuggingFace token'ları şifrelenmiş olarak saklanır
- **Modern Arayüz**: Kullanıcı dostu, modern PyQt6 arayüzü

## 🚀 Kurulum

### Gereksinimler

- Python 3.9 veya üzeri
- pip (Python paket yöneticisi)
- Git (repo'yu klonlamak için)
- HuggingFace API Token ([Almak için tıklayın](https://huggingface.co/settings/tokens))

### Adım 1: Repo'yu Klonlayın

```bash
git clone https://github.com/Tinlera/tinlera-research-tool.git
cd tinlera-research-tool
```

### Adım 2: Virtual Environment Oluşturun

Sistem Python'unuzu korumak için virtual environment kullanmanız önerilir:

```bash
python3 -m venv venv
```

### Adım 3: Virtual Environment'ı Aktifleştirin

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Adım 4: Bağımlılıkları Yükleyin

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Adım 5: Programı Çalıştırın

**Linux/macOS:**
```bash
./run.sh
```

veya

```bash
python main.py
```

**Windows:**
```bash
python main.py
```

## 📖 Kullanım

### İlk Kurulum

1. **Programı Başlatın**: `./run.sh` veya `python main.py` komutu ile programı başlatın

2. **HuggingFace Token'ınızı Girin**:
   - Menü çubuğundan **Ayarlar** → **Ayarlar** seçeneğine tıklayın
   - "HuggingFace Ayarları" bölümüne token'ınızı girin
   - Token'ı [HuggingFace](https://huggingface.co/settings/tokens) adresinden alabilirsiniz
   - Token genellikle `hf_` ile başlar

3. **Özellikleri Yapılandırın**:
   - Web Arama, Geçmiş ve Export özelliklerini açıp kapatabilirsiniz
   - Ayarlar penceresinden veya üst kısımdaki toggle butonlardan kontrol edebilirsiniz

### Model Seçimi

1. Sol paneldeki **Model Seçimi** bölümünden bir model seçin
2. Dropdown menüden popüler modellerden birini seçebilirsiniz
3. Veya arama kutusuna model adını yazarak arama yapabilirsiniz
4. "Model Listesini Yenile" butonu ile popüler modelleri tekrar yükleyebilirsiniz

**Önerilen Modeller:**
- `meta-llama/Llama-3.1-8B-Instruct` - Genel amaçlı, güçlü
- `mistralai/Mistral-7B-Instruct-v0.2` - Hızlı ve verimli
- `Qwen/Qwen2.5-7B-Instruct` - Çok dilli destek
- `llava-hf/llava-1.5-7b-hf` - Resim analizi için

### Dosya Yükleme

1. **Drag & Drop**: Dosyaları sol paneldeki "Dosya Yükleme" bölümüne sürükleyip bırakın
2. **Dosya Ekle Butonu**: "Dosya Ekle" butonuna tıklayarak dosya seçin
3. **Çoklu Dosya**: Birden fazla dosya seçebilirsiniz
4. **Dosya Kaldırma**: Listeden bir dosyayı seçip "Seçiliyi Kaldır" butonuna tıklayın
5. **Temizleme**: "Tümünü Temizle" butonu ile tüm dosyaları kaldırın

**Desteklenen Formatlar:**
- PDF: `.pdf`
- Metin: `.txt`, `.md`
- Kod: `.py`, `.js`, `.java`, `.cpp`, `.c`, `.h`, `.hpp`, `.cs`, `.go`, `.rs`, `.rb`, `.php`, `.html`, `.css`, `.json`, `.xml`, `.yaml`, `.yml`
- Resim: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`

### Araştırma Yapma

1. **Sorunuzu Yazın**: Alt kısımdaki mesaj alanına sorunuzu yazın
2. **Gönder**: "Gönder" butonuna tıklayın veya **Ctrl+Enter** tuşlarına basın
3. **Bekleyin**: AI yanıtını bekleyin (model yükleniyorsa biraz zaman alabilir)
4. **Sonuçları Görün**: Yanıt sohbet alanında görüntülenecektir

**İpuçları:**
- Dosya yüklediyseniz, AI dosya içeriğini analiz edecektir
- Web arama açıksa, gerçek zamanlı web sonuçları da eklenecektir
- Uzun yanıtlar için biraz sabırlı olun

### Web Arama Kullanımı

1. Üst kısımdaki **"🔍 Web Arama: Açık"** butonuna tıklayarak web aramayı açın/kapatın
2. Web arama açıkken, sorularınız için otomatik olarak web sonuçları aranır
3. Arama sonuçları yanıtla birlikte gösterilir
4. Export edildiğinde kaynak referansları da dahil edilir

### Geçmiş Yönetimi

1. **Geçmişi Görüntüleme**:
   - Menü çubuğundan **Geçmiş** → **Geçmişi Görüntüle** seçeneğine tıklayın
   - Tüm araştırmalarınızı liste halinde görüntüleyin
   - Bir kaydı seçerek detaylarını görüntüleyin

2. **Geçmişten Devam Etme**:
   - Geçmiş penceresinde bir kaydı seçin
   - "Yükle" butonuna tıklayın
   - Sohbet ve dosyalar otomatik olarak yüklenecektir

3. **Geçmişi Temizleme**:
   - Menü çubuğundan **Geçmiş** → **Geçmişi Temizle** seçeneğine tıklayın
   - Onaylayın

### Export İşlemleri

1. Bir araştırma yaptıktan sonra, menü çubuğundan **Dosya** → **Export** seçeneğine tıklayın
2. Format seçin:
   - **TXT**: Düz metin dosyası
   - **Markdown**: Markdown formatı (GitHub uyumlu)
   - **DOCX**: Microsoft Word belgesi
3. Dosya otomatik olarak `data/exports/` klasörüne kaydedilir
4. Dosya yolu bir mesaj kutusunda gösterilir

**Export İçeriği:**
- Tarih ve saat
- Kullanılan model
- Soru/Prompt
- Eklenen dosyalar listesi
- Web arama sonuçları (varsa)
- AI yanıtı
- Kaynak referansları

### Özellik Toggle'ları

Üst kısımdaki butonlarla özellikleri açıp kapatabilirsiniz:

- **🔍 Web Arama**: Web arama özelliğini aç/kapa
- **📝 Geçmiş**: Geçmiş kayıtlarını aç/kapa
- **💾 Export**: Export özelliklerini aç/kapa

Bu ayarlar otomatik olarak kaydedilir ve bir sonraki açılışta hatırlanır.

## 🖼️ Ekran Görüntüleri

*(Ekran görüntüleri eklenecek)*

## 🔧 Teknik Detaylar

### Mimari

Program modüler bir yapıda tasarlanmıştır:

```
Research/
├── main.py                 # Ana giriş noktası
├── src/
│   ├── ui/                 # UI bileşenleri
│   │   ├── main_window.py
│   │   ├── model_selector.py
│   │   ├── file_uploader.py
│   │   ├── chat_widget.py
│   │   └── settings_dialog.py
│   ├── core/               # Core modüller
│   │   ├── hf_api.py       # HuggingFace API client
│   │   ├── file_processor.py
│   │   ├── web_search.py
│   │   ├── history_manager.py
│   │   └── export_manager.py
│   └── utils/              # Yardımcı modüller
│       ├── config_manager.py
│       └── constants.py
└── data/                   # Veri klasörleri
    ├── history/
    └── exports/
```

### Bağımlılıklar

- **PyQt6**: Modern GUI framework
- **requests**: HTTP istekleri
- **huggingface_hub**: HuggingFace entegrasyonu
- **PyPDF2/pdfplumber**: PDF işleme
- **Pillow**: Resim işleme
- **python-docx**: DOCX export
- **ddgs**: Web arama
- **cryptography**: Token şifreleme
- **markdown**: Markdown işleme
- **Pygments**: Kod syntax highlighting

### Güvenlik

- HuggingFace token'ları şifrelenmiş olarak saklanır (Fernet encryption)
- Token'lar hiçbir yerde plain text olarak gösterilmez
- Config dosyaları kısıtlı izinlerle saklanır (600)

### Performans

- Async işlemler için QThread kullanılır
- Model yükleme sırasında kullanıcı bilgilendirilir
- Retry mekanizması ile hata toleransı

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 📞 Destek

Sorularınız veya sorunlarınız için:
- GitHub Issues açın
- Dokümantasyonu inceleyin
- Community forumlarına katılın

## 🙏 Teşekkürler

- [HuggingFace](https://huggingface.co/) - Harika modeller ve API
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Güçlü GUI framework
- Tüm açık kaynak topluluğu

---

**Tinlera Research Tool** ile verimli araştırmalar dileriz! 🚀
