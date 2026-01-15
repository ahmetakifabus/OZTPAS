# 📊 Sinav-Karne Analiz Platformu

Modern ve interaktif bir web uygulamasi ile ogrenci sinav ve karne notlari arasindaki iliskiyi analiz edin. Gelismis istatistiksel yontemler ve gorsel analizlerle egitim verilerinizi anlayin.

## ✨ Ozellikler

### 📈 Istatistiksel Analizler
- **Basit Regresyon Analizi**: Her ders icin tekli degisken analizi
- **Coklu Regresyon Analizi**: Tum dersleri birlikte degerlendirerek gelismis tahminler
- **T-Puani Donusumu**: Standartlastirilmis puanlarla adil karsilastirma
- **R2 ve RMSE Metrikleri**: Model performansini olcun

### 🎨 Gorsellestirmeler
- **Interaktif Grafikler**: Plotly.js ile dinamik scatter plot'lar
- **Bar Chart'lar**: Katsayi analizi ve karsilastirmalar
- **Gercek Zamanli Guncellemeler**: Aninda sonuc goruntuleme
- **Responsive Tasarim**: Tum cihazlarda mukemmel gorunum

### 📁 Veri Yonetimi
- **CSV Dosya Destegi**: Kolay veri yukleme
- **Sonuc Indirme**: Analiz sonuclarini CSV olarak kaydedin
- **Tarayici Tabanli**: Sunucu gerektirmez, tum islemler istemci tarafinda

### 💻 Modern Arayuz
- **Gradient Tasarim**: Goz alici renkler ve gecisler
- **Smooth Animasyonlar**: Akici kullanici deneyimi
- **Dark Mode Hazir**: Koyu tema destegi

## 🚀 Hizli Baslangic

## 📄 CSV Dosya Formati

### Sinav Dosyasi (sinav.csv)
```csv
RUMUZ;TDS;MDS;FDS;SDS;DDS
OGR001;85;90;78;88;92
OGR002;75;82;85;79;88
OGR003;92;88;90;85;90
```

**Sutunlar:**
- `RUMUZ`: Ogrenci kimlik numarasi
- `TDS`: Turkce sinav puani
- `MDS`: Matematik sinav puani
- `FDS`: Fen sinav puani
- `SDS`: Sosyal sinav puani
- `DDS`: Din sinav puani

### Karne Dosyasi (karne.csv)
```csv
RUMUZ;TURKCE;MAT;FEN;SOSYAL;DIN
OGR001;4,5;4,8;4,2;4,6;4,9
OGR002;3,8;4,1;4,3;3,9;4,4
OGR003;4,7;4,5;4,6;4,3;4,6
```

**Sutunlar:**
- `RUMUZ`: Ogrenci kimlik numarasi (sinav dosyasi ile eslesmeli)
- `TURKCE`: Turkce karne notu
- `MAT`: Matematik karne notu
- `FEN`: Fen karne notu
- `SOSYAL`: Sosyal karne notu
- `DIN`: Din karne notu

**Not:** Karne notlari ondalik ayirici olarak virgul (`,`) kullanir.

## 🛠️ Kullanim

1. **Dosya Yukleme**
   - Sinav CSV dosyanizi yukleyin
   - Karne CSV dosyanizi yukleyin
   - Her iki dosya yuklendikten sonra "Analizi Baslat" butonu aktif olur

2. **Analiz**
   - "Analizi Baslat" butonuna tiklayin
   - Platform otomatik olarak T-puani donusumu yapar
   - Basit ve coklu regresyon analizleri hesaplanir

3. **Sonuclari Inceleme**
   - **Basit Regresyon**: Her ders icin scatter plot ve R2 degerleri
   - **Coklu Regresyon**: Tum derslerin birlikte degerlendirilmesi, katsayi grafikleri
   - **Karsilastirma**: Detayli tablo ve karsilastirma grafikleri

4. **Sonuc Indirme**
   - "Sonuclari Indir (CSV)" butonu ile analiz sonuclarini kaydedin
   - Excel'de acip daha detayli incelemeler yapin

## 🔧 Teknolojiler

- **HTML5**: Yapi ve icerik
- **Tailwind CSS**: Modern ve responsive tasarim
- **Vanilla JavaScript**: Tum hesaplamalar ve mantik
- **Plotly.js**: Interaktif grafikler ve gorsellestirmeler

## 🧠 Analiz Yontemleri

### T-Puani Donusumu
Farkli olceklerdeki notlari standartlastirir:
```
T = 50 + 10 * ((X - mu) / sigma)
```
- mu: Ortalama
- sigma: Standart sapma
- Sonuc: Ortalama 50, standart sapma 10

### Basit Lineer Regresyon
Her ders icin:
```
Y = beta0 + beta1X + epsilon
```
- Y: Karne T-puani
- X: Sinav T-puani
- beta0: Kesme noktasi
- beta1: Egim

### Coklu Lineer Regresyon
Tum dersler birlikte:
```
Y = beta0 + beta1X1 + beta2X2 + ... + beta5X5 + epsilon
```
- X1...X5: Tum derslerin sinav T-puanlari

### Model Degerlendirme
- **R2**: Modelin acikladigi varyans orani (0-1)
- **RMSE**: Ortalama hata (dusuk = iyi)

## 🤝 Katkida Bulunma

Katkilarinizi bekliyoruz! Lutfen su adimlari izleyin:

1. Bu repo'yu fork edin
2. Feature branch olusturun (`git checkout -b feature/harika-ozellik`)
3. Degisikliklerinizi commit edin (`git commit -m 'Harika ozellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/harika-ozellik`)
5. Pull Request acin

### 💡 Gelistirme Fikirleri
- [ ] Excel dosya destegi ekle
- [ ] PDF rapor olusturma
- [ ] Daha fazla istatistiksel test
- [ ] Veri filtreleme ve arama
- [ ] Koyu tema secenegi
- [ ] Coklu dil destegi
- [ ] Ogrenci bazli detayli analiz
- [ ] Zaman serisi analizi

## 📜 Lisans

Bu proje MIT Lisansi altinda lisanslanmistir - detaylar icin [LICENSE](LICENSE) dosyasina bakin.

## 👤 Gelistirici

**Proje:** - (https://github.com/ahmetakifabus)

## 🙏 Tesekkurler

- [Tailwind CSS](https://tailwindcss.com/) - Harika CSS framework'u icin
- [Plotly.js](https://plotly.com/javascript/) - Guclu gorsellestirme kutuphanesi icin
- [Google Fonts](https://fonts.google.com/) - Inter font ailesi icin

## 📞 Iletisim

Sorulariniz veya onerileriniz icin:
- Email: ahmetakifabus91@proton.me, rmzucar@gmail.com, bozdemiryusuf@gmail.com

---

Bu projeyi begendiyseniz yildiz vermeyi unutmayin!

**Yapim: 2025 | AAIHL 🏗️**