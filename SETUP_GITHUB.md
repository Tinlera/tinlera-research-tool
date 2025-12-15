# GitHub Repo Oluşturma Rehberi

## GitHub Token Oluşturma

1. GitHub'a giriş yapın: https://github.com
2. Sağ üst köşedeki profil resminize tıklayın
3. **Settings** (Ayarlar) seçeneğine tıklayın
4. Sol menüden **Developer settings** seçeneğine tıklayın
5. **Personal access tokens** → **Tokens (classic)** seçeneğine tıklayın
6. **Generate new token** → **Generate new token (classic)** seçeneğine tıklayın
7. Token için bir isim verin (örn: "Tinlera Research Tool")
8. Süre seçin (örn: "No expiration" veya belirli bir süre)
9. **repo** scope'unu işaretleyin (tüm alt seçenekler otomatik seçilir)
10. **Generate token** butonuna tıklayın
11. **ÖNEMLİ**: Token'ı kopyalayın ve güvenli bir yere kaydedin (bir daha gösterilmeyecek!)

## Repo Oluşturma

### Yöntem 1: Script ile (Önerilen)

```bash
./create_repo.sh
```

Script çalıştığında:
1. GitHub token'ınızı isteyecek (gizli olarak)
2. Repo'yu oluşturacak
3. Kodu GitHub'a gönderecek

### Yöntem 2: Manuel (GitHub CLI ile)

Eğer GitHub CLI kuruluysa:

```bash
gh repo create tinlera-research-tool --public --description "HuggingFace modelleri ile kapsamlı araştırma yapmanızı sağlayan PyQt6 tabanlı masaüstü uygulaması" --source=. --remote=origin --push
```

### Yöntem 3: Manuel (GitHub Web Arayüzü)

1. GitHub'a giriş yapın
2. Sağ üst köşedeki **+** butonuna tıklayın
3. **New repository** seçeneğine tıklayın
4. Repository name: `tinlera-research-tool`
5. Description: `HuggingFace modelleri ile kapsamlı araştırma yapmanızı sağlayan PyQt6 tabanlı masaüstü uygulaması`
6. **Public** seçeneğini işaretleyin
7. **Create repository** butonuna tıklayın
8. Sonra şu komutları çalıştırın:

```bash
git remote add origin https://github.com/KULLANICI_ADI/tinlera-research-tool.git
git branch -M main
git push -u origin main
```

## Repo URL'ini Güncelleme

Repo oluşturulduktan sonra, README.md dosyasındaki repo URL'lerini güncelleyin:

```bash
# README.md içinde şu satırı bulun:
git clone https://github.com/kullanici-adi/tinlera-research-tool.git

# Kendi kullanıcı adınızla değiştirin:
git clone https://github.com/SIZIN_KULLANICI_ADINIZ/tinlera-research-tool.git
```

## Sorun Giderme

### "Authentication failed" hatası
- Token'ın doğru kopyalandığından emin olun
- Token'ın `repo` scope'una sahip olduğundan emin olun
- Token'ın süresinin dolmadığından emin olun

### "Repository already exists" hatası
- Repo zaten varsa, remote URL'i kontrol edin:
  ```bash
  git remote -v
  ```
- Veya mevcut repo'ya push yapın:
  ```bash
  git push -u origin main
  ```

### "Permission denied" hatası
- Token'ın yeterli yetkilere sahip olduğundan emin olun
- Token'ın `repo` scope'unun tam olarak seçildiğinden emin olun

