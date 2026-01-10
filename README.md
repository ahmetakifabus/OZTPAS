# 📊 Sınav-Karne Analiz Platformu

Modern ve interaktif bir web uygulaması ile öğrenci sınav ve karne notları arasındaki ilişkiyi analiz edin. Gelişmiş istatistiksel yöntemler ve görsel analizlerle eğitim verilerinizi anlayın.

## ✨ Özellikler

### 📈 İstatistiksel Analizler
- **Basit Regresyon Analizi**: Her ders için tekli değişken analizi
- **Çoklu Regresyon Analizi**: Tüm dersleri birlikte değerlendirerek gelişmiş tahminler
- **T-Puanı Dönüşümü**: Standartlaştırılmış puanlarla adil karşılaştırma
- **R² ve RMSE Metrikleri**: Model performansını ölçün

### 📊 Görselleştirmeler
- **İnteraktif Grafikler**: Plotly.js ile dinamik scatter plot'lar
- **Bar Chart'lar**: Katsayı analizi ve karşılaştırmalar
- **Gerçek Zamanlı Güncellemeler**: Anında sonuç görüntüleme
- **Responsive Tasarım**: Tüm cihazlarda mükemmel görünüm

### 💾 Veri Yönetimi
- **CSV Dosya Desteği**: Kolay veri yükleme
- **Sonuç İndirme**: Analiz sonuçlarını CSV olarak kaydedin
- **Tarayıcı Tabanlı**: Sunucu gerektirmez, tüm işlemler istemci tarafında

### 🎨 Modern Arayüz
- **Gradient Tasarım**: Göz alıcı renkler ve geçişler
- **Smooth Animasyonlar**: Akıcı kullanıcı deneyimi
- **Dark Mode Hazır**: Koyu tema desteği
- **Emoji İkonlar**: Görsel zenginlik

## 🚀 Hızlı Başlangıç

### GitHub Pages ile Yayınlama

1. **Repository Oluşturun**
   ```bash
   git clone https://github.com/KULLANICI_ADINIZ/sinav-karne-analiz.git
   cd sinav-karne-analiz
   ```

2. **Dosyaları Ekleyin**
   - `index.html` dosyasını root dizine yerleştirin
   - CSV örnek dosyalarınızı `data/` klasörüne ekleyin (opsiyonel)

3. **GitHub'a Yükleyin**
   ```bash
   git add .
   git commit -m "İlk commit: Analiz platformu eklendi"
   git push origin main
   ```

4. **GitHub Pages'i Aktif Edin**
   - Repository > Settings > Pages
   - Source: `Deploy from a branch`
   - Branch: `main` / `root`
   - Save

5. **Siteniz Hazır!**
   - `https://KULLANICI_ADINIZ.github.io/sinav-karne-analiz/`

### Lokal Kullanım

Basitçe `index.html` dosyasını tarayıcınızda açın:

```bash
# Dosyayı doğrudan açın
open index.html

# veya basit bir HTTP sunucu başlatın
python -m http.server 8000
# Tarayıcıda: http://localhost:8000
```

## 📁 CSV Dosya Formatı

### Sınav Dosyası (sinav.csv)
```csv
RUMUZ;TDS;MDS;FDS;SDS;DDS
OGR001;85;90;78;88;92
OGR002;75;82;85;79;88
OGR003;92;88;90;85;90
```

**Sütunlar:**
- `RUMUZ`: Öğrenci kimlik numarası
- `TDS`: Türkçe sınav puanı
- `MDS`: Matematik sınav puanı
- `FDS`: Fen sınav puanı
- `SDS`: Sosyal sınav puanı
- `DDS`: Din sınav puanı

### Karne Dosyası (karne.csv)
```csv
RUMUZ;TURKCE;MAT;FEN;SOSYAL;DIN
OGR001;4,5;4,8;4,2;4,6;4,9
OGR002;3,8;4,1;4,3;3,9;4,4
OGR003;4,7;4,5;4,6;4,3;4,6
```

**Sütunlar:**
- `RUMUZ`: Öğrenci kimlik numarası (sınav dosyası ile eşleşmeli)
- `TURKCE`: Türkçe karne notu
- `MAT`: Matematik karne notu
- `FEN`: Fen karne notu
- `SOSYAL`: Sosyal karne notu
- `DIN`: Din karne notu

**Not:** Karne notları ondalık ayırıcı olarak virgül (`,`) kullanır.

## 🎯 Kullanım

1. **Dosya Yükleme**
   - Sınav CSV dosyanızı yükleyin
   - Karne CSV dosyanızı yükleyin
   - Her iki dosya yüklendikten sonra "Analizi Başlat" butonu aktif olur

2. **Analiz**
   - "Analizi Başlat" butonuna tıklayın
   - Platform otomatik olarak T-puanı dönüşümü yapar
   - Basit ve çoklu regresyon analizleri hesaplanır

3. **Sonuçları İnceleme**
   - **Basit Regresyon**: Her ders için scatter plot ve R² değerleri
   - **Çoklu Regresyon**: Tüm derslerin birlikte değerlendirilmesi, katsayı grafikleri
   - **Karşılaştırma**: Detaylı tablo ve karşılaştırma grafikleri

4. **Sonuç İndirme**
   - "Sonuçları İndir (CSV)" butonu ile analiz sonuçlarını kaydedin
   - Excel'de açıp daha detaylı incelemeler yapın

## 🛠️ Teknolojiler

- **HTML5**: Yapı ve içerik
- **Tailwind CSS**: Modern ve responsive tasarım
- **Vanilla JavaScript**: Tüm hesaplamalar ve mantık
- **Plotly.js**: İnteraktif grafikler ve görselleştirmeler
- **No Backend**: Tamamen istemci tabanlı, sunucu gerektirmez

## 📊 Analiz Yöntemleri

### T-Puanı Dönüşümü
Farklı ölçeklerdeki notları standartlaştırır:
```
T = 50 + 10 * ((X - μ) / σ)
```
- μ: Ortalama
- σ: Standart sapma
- Sonuç: Ortalama 50, standart sapma 10

### Basit Lineer Regresyon
Her ders için:
```
Y = β₀ + β₁X + ε
```
- Y: Karne T-puanı
- X: Sınav T-puanı
- β₀: Kesme noktası
- β₁: Eğim

### Çoklu Lineer Regresyon
Tüm dersler birlikte:
```
Y = β₀ + β₁X₁ + β₂X₂ + ... + β₅X₅ + ε
```
- X₁...X₅: Tüm derslerin sınav T-puanları

### Model Değerlendirme
- **R²**: Modelin açıkladığı varyans oranı (0-1)
- **RMSE**: Ortalama hata (düşük = iyi)

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen şu adımları izleyin:

1. Bu repo'yu fork edin
2. Feature branch oluşturun (`git checkout -b feature/harika-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Harika özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/harika-ozellik`)
5. Pull Request açın

### Geliştirme Fikirleri
- [ ] Excel dosya desteği ekle
- [ ] PDF rapor oluşturma
- [ ] Daha fazla istatistiksel test
- [ ] Veri filtreleme ve arama
- [ ] Koyu tema seçeneği
- [ ] Çoklu dil desteği
- [ ] Öğrenci bazlı detaylı analiz
- [ ] Zaman serisi analizi

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👨‍💻 Geliştirici

**Projeniz** - [GitHub Profiliniz](https://github.com/KULLANICI_ADINIZ)

## 🙏 Teşekkürler

- [Tailwind CSS](https://tailwindcss.com/) - Harika CSS framework'ü için
- [Plotly.js](https://plotly.com/javascript/) - Güçlü görselleştirme kütüphanesi için
- [Google Fonts](https://fonts.google.com/) - Inter font ailesi için

## 📞 İletişim

Sorularınız veya önerileriniz için:
- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/KULLANICI_ADINIZ/sinav-karne-analiz/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/KULLANICI_ADINIZ/sinav-karne-analiz/discussions)

## 📸 Ekran Görüntüleri

### Ana Sayfa
![Hero Section](screenshots/hero.png)

### Dosya Yükleme
![Upload Section](screenshots/upload.png)

### Basit Regresyon Analizi
![Simple Regression](screenshots/simple-regression.png)

### Çoklu Regresyon Analizi
![Multiple Regression](screenshots/multiple-regression.png)

### Karşılaştırma Tablosu
![Comparison](screenshots/comparison.png)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

**Yapım: 2025 | Eğitimde Veri Analizi**
