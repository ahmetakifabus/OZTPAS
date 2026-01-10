# 📖 Python Script Kullanım Kılavuzu

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
# Repository'yi klonlayın
git clone https://github.com/KULLANICI_ADINIZ/sinav-karne-analiz.git
cd sinav-karne-analiz

# Virtual environment oluşturun (önerilen)
python -m venv venv

# Virtual environment'ı aktif edin
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Gereksinimleri yükleyin
pip install -r requirements.txt
```

### 2. Demo ile Test

```bash
# Demo verilerle hızlı test
python analiz.py --demo

# Demo veri oluşturulur ve analiz yapılır
# Çıktılar: demo_data/ ve output/ klasörlerinde
```

### 3. Kendi Verilerinizle Kullanım

```bash
# Temel kullanım
python analiz.py --sinav sinav.csv --karne karne.csv

# Özel çıktı klasörü
python analiz.py --sinav sinav.csv --karne karne.csv --output sonuclar/

# Grafik göstermeden (sunucularda)
python analiz.py --sinav sinav.csv --karne karne.csv --no-plot
```

## 📊 Çıktılar

Script çalıştırıldığında şu dosyalar oluşur:

### 1. Grafikler (`output/regresyon_analizi.png`)
- **15 adet grafik** (5 ders × 3 görünüm)
- Basit regresyon scatter plot'ları
- Çoklu regresyon tahmin vs gerçek
- Katsayı bar chart'ları
- Yüksek çözünürlük (300 DPI)

### 2. CSV Raporları

**`output/regresyon_karsilastirma.csv`**
```csv
Ders,Basit_R2,Basit_RMSE,Coklu_R2,Coklu_RMSE,R2_Artisi
TÜRKÇE,0.8234,3.456,0.8891,2.987,0.0657
MATEMATİK,0.7892,4.123,0.8543,3.567,0.0651
...
```

**`output/detayli_sonuclar.csv`**
```csv
RUMUZ,Ders,Sinav_T,Karne_T,Tahmin_Basit,Tahmin_Coklu
OGR001,TÜRKÇE,52.34,54.12,53.45,53.89
OGR001,MATEMATİK,48.23,49.87,49.12,50.01
...
```

### 3. Konsol Raporu
Terminalde detaylı analiz raporu gösterilir:
- Basit regresyon sonuçları
- Çoklu regresyon sonuçları
- Performans karşılaştırmaları
- Özet istatistikler

## 🎯 Gelişmiş Kullanım

### Python Scriptinden Kullanım

```python
from analiz import SinavKarneAnaliz

# Analiz nesnesi oluştur
analiz = SinavKarneAnaliz(
    sinav_dosya="sinav.csv",
    karne_dosya="karne.csv"
)

# Adım adım analiz
analiz.veri_yukle()
analiz.t_puanlarini_ekle()
analiz.verileri_birlestir()
analiz.analiz_yap()

# Sonuçları al
for ders in analiz.DERSLER:
    basit = analiz.sonuclar[ders]['basit']
    coklu = analiz.sonuclar[ders]['coklu']
    print(f"{ders}:")
    print(f"  Basit R² = {basit['r2']:.4f}")
    print(f"  Çoklu R² = {coklu['r2']:.4f}")

# Grafik ve rapor oluştur
analiz.grafik_olustur("my_output")
analiz.rapor_olustur("my_output")
```

### Özelleştirilmiş Analiz

```python
import pandas as pd
from analiz import SinavKarneAnaliz

# Verileri önceden filtrele
sinav = pd.read_csv("sinav.csv", sep=";")
karne = pd.read_csv("karne.csv", sep=";")

# Sadece belirli öğrencileri analiz et
sinav_filtre = sinav[sinav['RUMUZ'].str.startswith('OGR1')]
karne_filtre = karne[karne['RUMUZ'].str.startswith('OGR1')]

# Geçici dosyalar oluştur
sinav_filtre.to_csv("temp_sinav.csv", sep=";", index=False)
karne_filtre.to_csv("temp_karne.csv", sep=";", index=False)

# Analiz yap
analiz = SinavKarneAnaliz("temp_sinav.csv", "temp_karne.csv")
analiz.calistir("filtered_output")
```

## 🔧 Sorun Giderme

### Problem: ModuleNotFoundError

```bash
# Çözüm: Gereksinimleri yeniden yükleyin
pip install -r requirements.txt --upgrade
```

### Problem: UnicodeDecodeError (CSV okuma hatası)

```python
# CSV dosyanızın encoding'ini kontrol edin
# analiz.py içinde şu satırı bulun:
pd.read_csv(self.sinav_dosya, sep=";")

# Şu şekilde değiştirin:
pd.read_csv(self.sinav_dosya, sep=";", encoding='utf-8-sig')
# veya
pd.read_csv(self.sinav_dosya, sep=";", encoding='latin-1')
```

### Problem: Grafik gösterilmiyor

```bash
# Linux'ta backend problemi
sudo apt-get install python3-tk

# Mac'te
brew install python-tk

# Veya grafik göstermeden çalıştırın
python analiz.py --sinav sinav.csv --karne karne.csv --no-plot
```

### Problem: Matplotlib hatası (sunucu/SSH)

```python
# analiz.py başına ekleyin:
import matplotlib
matplotlib.use('Agg')  # GUI gerektirmeyen backend
```

## 📈 Performans İpuçları

### Büyük Veri Setleri

```python
# Chunk'lar halinde okuma
def veri_yukle_buyuk(self, chunk_size=1000):
    chunks = []
    for chunk in pd.read_csv(self.sinav_dosya, sep=";", chunksize=chunk_size):
        chunks.append(chunk)
    self.sinav_data = pd.concat(chunks, ignore_index=True)
```

### Paralel İşlem

```python
from joblib import Parallel, delayed

# Paralel regresyon analizi
def paralel_analiz(self):
    results = Parallel(n_jobs=-1)(
        delayed(self.basit_regresyon)(
            self.veri[f"{ders}_T_SINAV"].values,
            self.veri[f"{ders}_T_KARNE"].values
        )
        for ders in self.DERSLER
    )
```

## 🎨 Grafik Özelleştirme

### Renkleri Değiştirme

```python
# analiz.py içinde DERSLER sözlüğünü düzenleyin
DERSLER = {
    "TÜRKÇE": ("TDS", "TURKCE", "#FF0000", "📚"),  # Kırmızı
    "MATEMATİK": ("MDS", "MAT", "#00FF00", "🔢"),  # Yeşil
    # ...
}
```

### Grafik Boyutunu Ayarlama

```python
# grafik_olustur metodunda
fig = plt.figure(figsize=(30, 20), facecolor='#f8f9fa')  # Daha büyük
# veya
fig = plt.figure(figsize=(15, 10), facecolor='#f8f9fa')  # Daha küçük
```

### DPI Ayarlama (Çözünürlük)

```python
plt.savefig(grafik_dosya, dpi=150)  # Düşük (hızlı)
plt.savefig(grafik_dosya, dpi=300)  # Normal
plt.savefig(grafik_dosya, dpi=600)  # Yüksek (yayın kalitesi)
```

## 🔄 Batch İşleme

Birden fazla dosya çiftini analiz etmek için:

```bash
# batch_analiz.sh oluşturun
#!/bin/bash

for year in 2021 2022 2023 2024
do
    echo "Analiz ediliyor: $year"
    python analiz.py \
        --sinav "data/sinav_${year}.csv" \
        --karne "data/karne_${year}.csv" \
        --output "output_${year}" \
        --no-plot
done

echo "Tüm yıllar analiz edildi!"
```

```bash
chmod +x batch_analiz.sh
./batch_analiz.sh
```

## 📊 Excel Desteği (Gelecek Özellik)

```python
# Excel dosyalarını okuma için:
pip install openpyxl

# Kod değişikliği (analiz.py):
def veri_yukle(self):
    # CSV yerine Excel
    self.sinav_data = pd.read_excel(self.sinav_dosya)
    self.karne_data = pd.read_excel(self.karne_dosya)
```

## 🎓 Eğitim Amaçlı Kullanım

### Jupyter Notebook ile

```bash
# Jupyter kurulumu
pip install jupyter

# Notebook başlat
jupyter notebook
```

```python
# Notebook'ta
from analiz import SinavKarneAnaliz
import matplotlib.pyplot as plt

%matplotlib inline

analiz = SinavKarneAnaliz("sinav.csv", "karne.csv")
analiz.calistir("output", grafik_goster=True)
```

### Öğrencilere Gösterim

```python
# Adım adım gösterim modu
analiz = SinavKarneAnaliz("sinav.csv", "karne.csv")

print("1️⃣ Veriler yükleniyor...")
analiz.veri_yukle()
input("Devam etmek için Enter'a basın...")

print("2️⃣ T-puanları hesaplanıyor...")
analiz.t_puanlarini_ekle()
input("Devam etmek için Enter'a basın...")

# ...
```

## 🐛 Debugging

### Verbose Mod

```python
# Detaylı log için
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# analiz.py içinde
logger.debug(f"Veri boyutu: {len(self.veri)}")
logger.debug(f"Sütunlar: {self.veri.columns.tolist()}")
```

### Veri Kontrolü

```python
# Analiz öncesi veri kalitesi kontrolü
def veri_kontrol(self):
    print("Eksik değerler:")
    print(self.veri.isnull().sum())
    
    print("\nVeri tipleri:")
    print(self.veri.dtypes)
    
    print("\nİstatistikler:")
    print(self.veri.describe())
```

## 💡 İpuçları

1. **Virtual Environment Kullanın**: Paket çakışmalarını önler
2. **Git Kullanın**: Her önemli değişikliği commit edin
3. **Dokümante Edin**: Kodunuza yorum ekleyin
4. **Test Edin**: Her değişiklikten sonra demo ile test edin
5. **Yedekleyin**: Önemli verilerinizi yedekleyin

## 📞 Yardım

Sorularınız için:
- 📧 Email: your.email@example.com
- 🐛 GitHub Issues
- 💬 Discussions

---

**Happy Analyzing! 📊✨**
