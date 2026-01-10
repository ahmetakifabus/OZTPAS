# 📁 Proje Yapısı

Bu dosya, projenizin klasör ve dosya yapısını gösterir.

## 🗂️ Dizin Yapısı

```
sinav-karne-analiz/
│
├── index.html                 # Ana web sayfası
├── README.md                  # Proje açıklaması ve dokümantasyon
├── LICENSE                    # MIT Lisans dosyası
├── .gitignore                # Git'in göz ardı edeceği dosyalar
├── PROJE_YAPISI.md           # Bu dosya
│
├── data/                     # Örnek veri dosyaları
│   ├── examples/             # Örnek CSV dosyaları
│   │   ├── sinav_ornek.csv
│   │   └── karne_ornek.csv
│   └── templates/            # Boş şablon dosyaları
│       ├── sinav_template.csv
│       └── karne_template.csv
│
├── docs/                     # Dokümantasyon
│   ├── kullanim-kilavuzu.md
│   ├── csv-format.md
│   └── analiz-yontemleri.md
│
├── screenshots/              # Ekran görüntüleri (README için)
│   ├── hero.png
│   ├── upload.png
│   ├── simple-regression.png
│   ├── multiple-regression.png
│   └── comparison.png
│
└── assets/                   # Ek kaynaklar (opsiyonel)
    ├── logo.png
    └── favicon.ico
```

## 📄 Dosya Açıklamaları

### Ana Dosyalar

- **index.html**: Tüm uygulamayı içeren tek HTML dosyası. CSS ve JavaScript dahil.
- **README.md**: Projenin kapsamlı açıklaması, kullanım talimatları ve özellikler.
- **LICENSE**: MIT lisans metni.
- **.gitignore**: Git'in takip etmeyeceği dosya ve klasörlerin listesi.

### Data Klasörü

#### examples/
Kullanıcılara örnek olması için hazır veri setleri:

**sinav_ornek.csv** (30 öğrenci):
```csv
RUMUZ;TDS;MDS;FDS;SDS;DDS
OGR001;85;90;78;88;92
OGR002;75;82;85;79;88
OGR003;92;88;90;85;90
...
```

**karne_ornek.csv** (30 öğrenci):
```csv
RUMUZ;TURKCE;MAT;FEN;SOSYAL;DIN
OGR001;4,5;4,8;4,2;4,6;4,9
OGR002;3,8;4,1;4,3;3,9;4,4
OGR003;4,7;4,5;4,6;4,3;4,6
...
```

#### templates/
Kullanıcıların kendi verilerini girebilmeleri için boş şablonlar:

**sinav_template.csv**:
```csv
RUMUZ;TDS;MDS;FDS;SDS;DDS
OGR001;;;;;;;
OGR002;;;;;;;
```

**karne_template.csv**:
```csv
RUMUZ;TURKCE;MAT;FEN;SOSYAL;DIN
OGR001;;;;;;;
OGR002;;;;;;;
```

### Docs Klasörü

Detaylı dokümantasyon dosyaları:

- **kullanim-kilavuzu.md**: Adım adım kullanım talimatları
- **csv-format.md**: CSV dosya formatı detayları
- **analiz-yontemleri.md**: İstatistiksel yöntemlerin açıklaması

### Screenshots Klasörü

README.md dosyasında kullanılacak ekran görüntüleri:

- **hero.png**: Ana sayfa görünümü
- **upload.png**: Dosya yükleme ekranı
- **simple-regression.png**: Basit regresyon analizi
- **multiple-regression.png**: Çoklu regresyon analizi
- **comparison.png**: Karşılaştırma tablosu

### Assets Klasörü (Opsiyonel)

Ek görsel kaynaklar:

- **logo.png**: Proje logosu
- **favicon.ico**: Tarayıcı sekmesi ikonu

## 🚀 Kurulum Adımları

### 1. Repository Oluşturma

```bash
# GitHub'da yeni repo oluşturun
# Sonra local'de:

mkdir sinav-karne-analiz
cd sinav-karne-analiz
git init
```

### 2. Dosyaları Ekleme

```bash
# Ana dosyaları ekleyin
touch index.html README.md LICENSE .gitignore

# Klasörleri oluşturun
mkdir -p data/examples data/templates docs screenshots assets

# Örnek dosyaları oluşturun
touch data/examples/sinav_ornek.csv
touch data/examples/karne_ornek.csv
touch data/templates/sinav_template.csv
touch data/templates/karne_template.csv

# Dokümantasyon dosyaları
touch docs/kullanim-kilavuzu.md
touch docs/csv-format.md
touch docs/analiz-yontemleri.md
```

### 3. Git İşlemleri

```bash
# Dosyaları stage'e ekle
git add .

# Commit
git commit -m "İlk commit: Proje yapısı oluşturuldu"

# Remote repo ekle
git remote add origin https://github.com/KULLANICI_ADINIZ/sinav-karne-analiz.git

# Push
git push -u origin main
```

### 4. GitHub Pages Aktivasyonu

1. GitHub repo sayfanıza gidin
2. Settings > Pages
3. Source: "Deploy from a branch" seçin
4. Branch: "main" ve "/ (root)" seçin
5. Save'e tıklayın
6. 2-3 dakika bekleyin
7. `https://KULLANICI_ADINIZ.github.io/sinav-karne-analiz/` adresinde siteniz yayında!

## 📝 Örnek Veri Setleri Oluşturma

### Python ile Otomatik Veri Üretme

```python
import pandas as pd
import numpy as np

# Sınav verileri
np.random.seed(42)
n_students = 30

sinav_data = {
    'RUMUZ': [f'OGR{i:03d}' for i in range(1, n_students + 1)],
    'TDS': np.random.randint(60, 100, n_students),
    'MDS': np.random.randint(60, 100, n_students),
    'FDS': np.random.randint(60, 100, n_students),
    'SDS': np.random.randint(60, 100, n_students),
    'DDS': np.random.randint(60, 100, n_students)
}

sinav_df = pd.DataFrame(sinav_data)
sinav_df.to_csv('data/examples/sinav_ornek.csv', sep=';', index=False)

# Karne verileri (sınav ile korelasyonlu)
karne_data = {
    'RUMUZ': [f'OGR{i:03d}' for i in range(1, n_students + 1)],
    'TURKCE': (sinav_df['TDS'] / 20 + np.random.normal(0, 0.2, n_students)).round(1),
    'MAT': (sinav_df['MDS'] / 20 + np.random.normal(0, 0.2, n_students)).round(1),
    'FEN': (sinav_df['FDS'] / 20 + np.random.normal(0, 0.2, n_students)).round(1),
    'SOSYAL': (sinav_df['SDS'] / 20 + np.random.normal(0, 0.2, n_students)).round(1),
    'DIN': (sinav_df['DDS'] / 20 + np.random.normal(0, 0.2, n_students)).round(1)
}

karne_df = pd.DataFrame(karne_data)
karne_df.to_csv('data/examples/karne_ornek.csv', sep=';', index=False, decimal=',')

print("✅ Örnek veriler oluşturuldu!")
```

## 🎯 Minimum Gerekli Dosyalar

GitHub Pages'de yayınlamak için sadece şu dosyalar yeterlidir:

```
sinav-karne-analiz/
├── index.html      # ZORUNLU
├── README.md       # Önerilen
└── LICENSE         # Önerilen
```

Diğer tüm dosyalar ve klasörler opsiyoneldir!

## 📊 Gelişmiş Yapı (Gelecek Geliştirmeler İçin)

```
sinav-karne-analiz/
├── src/
│   ├── js/
│   │   ├── analysis.js
│   │   ├── charts.js
│   │   └── utils.js
│   ├── css/
│   │   └── custom.css
│   └── components/
│       ├── header.js
│       └── footer.js
├── tests/
│   └── analysis.test.js
└── package.json
```

## 🔄 Güncelleme Süreci

```bash
# Değişiklik yap
git add .
git commit -m "Yeni özellik: ..."
git push origin main

# GitHub Pages otomatik güncellenir (30-60 saniye)
```

## ✨ Pro İpuçları

1. **Branches Kullanın**: Ana kodunuzu `main`'de tutun, yeni özellikler için `feature` branch'leri oluşturun
2. **Issues Açın**: Her geliştirme için GitHub issue oluşturun
3. **Pull Request**: Değişiklikleri PR ile merge edin
4. **README Güncel Tutun**: Her yeni özellik eklendiğinde README'yi güncelleyin
5. **Screenshots Ekleyin**: Görsel dokümantasyon kullanıcı deneyimini artırır

---

Bu yapı ile projeniz profesyonel ve organize görünecek! 🚀
