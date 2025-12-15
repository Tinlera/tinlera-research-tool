#!/bin/bash
# GitHub repo oluşturma scripti

REPO_NAME="tinlera-research-tool"
DESCRIPTION="HuggingFace modelleri ile kapsamlı araştırma yapmanızı sağlayan PyQt6 tabanlı masaüstü uygulaması"

echo "GitHub token'ınızı girin (gizli olarak):"
read -s GITHUB_TOKEN

if [ -z "$GITHUB_TOKEN" ]; then
    echo "Hata: GitHub token gerekli!"
    exit 1
fi

# GitHub API ile repo oluştur
echo "GitHub'da repo oluşturuluyor..."
RESPONSE=$(curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$REPO_NAME\",\"description\":\"$DESCRIPTION\",\"public\":true}")

# Repo URL'ini çıkar
REPO_URL=$(echo $RESPONSE | grep -o '"clone_url":"[^"]*' | cut -d'"' -f4)

if [ -z "$REPO_URL" ]; then
    echo "Hata: Repo oluşturulamadı. Response:"
    echo $RESPONSE
    exit 1
fi

echo "✓ Repo başarıyla oluşturuldu: $REPO_URL"

# Remote ekle
git remote add origin $REPO_URL 2>/dev/null || git remote set-url origin $REPO_URL

# Branch'i main olarak değiştir
git branch -M main

# Push yap
echo "Kod GitHub'a gönderiliyor..."
git push -u origin main

echo ""
echo "✓ Tamamlandı! Repo: $REPO_URL"
echo "GitHub'da görüntülemek için: https://github.com/$(echo $REPO_URL | cut -d'/' -f4)/$REPO_NAME"

