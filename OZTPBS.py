import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import argparse
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (20, 14)
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'


class SinavKarneAnaliz:
    
    DERSLER = {
        "TÜRKÇE": ("TDS", "TURKCE", "#FF6B9D", ""),
        "MATEMATİK": ("MDS", "MAT", "#4ECDC4", ""),
        "FEN": ("FDS", "FEN", "#45B7D1", ""),
        "SOSYAL": ("SDS", "SOSYAL", "#FFA07A", ""),
        "DİN": ("DDS", "DIN", "#DDA0DD", "")
    }
    
    def __init__(self, sinav_dosya=None, karne_dosya=None):
        self.sinav_dosya = sinav_dosya
        self.karne_dosya = karne_dosya
        self.sinav_data = None
        self.karne_data = None
        self.veri = None
        self.sonuclar = {}
        
    def veri_yukle(self):
        print("📂 Veriler yükleniyor...")
        
        try:
            self.sinav_data = pd.read_csv(self.sinav_dosya, sep=";")
            self.sinav_data.columns = self.sinav_data.columns.str.replace("\n", " ").str.replace(" ", "")
            print(f"✅ Sınav verisi yüklendi: {len(self.sinav_data)} öğrenci")
            
            self.karne_data = pd.read_csv(self.karne_dosya, sep=";")
            self.karne_data.columns = self.karne_data.columns.str.replace(" ", "")
            
            for col in self.karne_data.columns:
                if col != "RUMUZ":
                    self.karne_data[col] = (
                        self.karne_data[col]
                        .astype(str)
                        .str.replace(",", ".")
                        .astype(float)
                    )
            
            print(f"✅ Karne verisi yüklendi: {len(self.karne_data)} öğrenci")
            return True
            
        except FileNotFoundError as e:
            print(f"Hata: Dosya bulunamadı - {e}")
            return False
        except Exception as e:
            print(f"Hata: {e}")
            return False
    
    @staticmethod
    def t_puan_hesapla(series):
        return 50 + 10 * ((series - series.mean()) / series.std(ddof=0))
    
    def t_puanlarini_ekle(self):
        print("\nT-puanları hesaplanıyor...")
        
        for ders, (sinav_col, karne_col, _, _) in self.DERSLER.items():
            self.sinav_data[f"{ders}_T"] = self.t_puan_hesapla(self.sinav_data[sinav_col])
            self.karne_data[f"{ders}_T"] = self.t_puan_hesapla(self.karne_data[karne_col])
        
        print("✅ T-puanları hesaplandı")
    
    def verileri_birlestir(self):
        print("\nVeriler birleştiriliyor...")
        
        sinav_cols = ["RUMUZ"] + [f"{d}_T" for d in self.DERSLER]
        karne_cols = ["RUMUZ"] + [f"{d}_T" for d in self.DERSLER]
        
        self.veri = pd.merge(
            self.sinav_data[sinav_cols],
            self.karne_data[karne_cols],
            on="RUMUZ",
            suffixes=("_SINAV", "_KARNE")
        ).dropna()
        
        print(f"✅ {len(self.veri)} öğrenci birleştirildi")
    
    def basit_regresyon(self, x, y):
        model = LinearRegression()
        model.fit(x.reshape(-1, 1), y)
        y_pred = model.predict(x.reshape(-1, 1))
        
        return {
            "model": model,
            "y_pred": y_pred,
            "r2": r2_score(y, y_pred),
            "rmse": np.sqrt(mean_squared_error(y, y_pred)),
            "slope": model.coef_[0],
            "intercept": model.intercept_
        }
    
    def coklu_regresyon(self, X, y):
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        
        return {
            "model": model,
            "y_pred": y_pred,
            "r2": r2_score(y, y_pred),
            "rmse": np.sqrt(mean_squared_error(y, y_pred)),
            "katsayilar": model.coef_,
            "intercept": model.intercept_
        }
    
    def analiz_yap(self):
        print("\nAnalizler yapılıyor...\n")
        
        for ders in self.DERSLER:
            x = self.veri[f"{ders}_T_SINAV"].values
            y = self.veri[f"{ders}_T_KARNE"].values
            
            basit = self.basit_regresyon(x, y)
            self.sonuclar[ders] = {"basit": basit}
            
            print(f"  ✓ {ders:12} - Basit R²: {basit['r2']:.4f}, RMSE: {basit['rmse']:.3f}")
        
        print()
        
        X_coklu = self.veri[[f"{d}_T_SINAV" for d in self.DERSLER]].values
        
        for ders in self.DERSLER:
            y = self.veri[f"{ders}_T_KARNE"].values
            coklu = self.coklu_regresyon(X_coklu, y)
            self.sonuclar[ders]["coklu"] = coklu
            
            iyilesme = (coklu['r2'] - self.sonuclar[ders]['basit']['r2']) * 100
            print(f"  ✓ {ders:12} - Çoklu R²: {coklu['r2']:.4f}, RMSE: {coklu['rmse']:.3f} (+{iyilesme:.1f}%)")
        
        print("\n✅ Tüm analizler tamamlandı!")
    
    def grafik_olustur(self, output_dir="output"):
        print(f"\nGrafikler oluşturuluyor ({output_dir}/)...")
        
        # Output klasörünü oluştur
        Path(output_dir).mkdir(exist_ok=True)
        
        fig = plt.figure(figsize=(22, 16), facecolor='#f8f9fa')
        fig.suptitle('SINAV-KARNE REGRESYON ANALİZİ', 
                     fontsize=28, fontweight='bold', y=0.98)
        
        for i, (ders, (_, _, color, emoji)) in enumerate(self.DERSLER.items()):
            basit = self.sonuclar[ders]['basit']
            coklu = self.sonuclar[ders]['coklu']
            
            x = self.veri[f"{ders}_T_SINAV"].values
            y = self.veri[f"{ders}_T_KARNE"].values
            
            ax1 = plt.subplot(3, 5, i + 1)
            ax1.scatter(x, y, color=color, alpha=0.6, s=80, edgecolors='white', linewidth=1.5)
            ax1.plot(x, basit['y_pred'], color='#2c3e50', linewidth=3, alpha=0.8)
            ax1.set_title(f'{emoji} {ders}\nBasit Regresyon', fontsize=13, fontweight='bold', pad=15)
            ax1.text(0.05, 0.95, f"R² = {basit['r2']:.3f}\nRMSE = {basit['rmse']:.2f}",
                    transform=ax1.transAxes, fontsize=10, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor=color, alpha=0.3))
            ax1.set_xlabel('Sınav T-Puanı', fontweight='bold')
            ax1.set_ylabel('Karne T-Puanı', fontweight='bold')
            ax1.grid(True, alpha=0.3)
            
            ax2 = plt.subplot(3, 5, i + 6)
            ax2.scatter(y, coklu['y_pred'], color=color, alpha=0.6, s=80, 
                       edgecolors='white', linewidth=1.5)
            lims = [min(y.min(), coklu['y_pred'].min()) - 2,
                    max(y.max(), coklu['y_pred'].max()) + 2]
            ax2.plot(lims, lims, 'k--', alpha=0.5, linewidth=2.5, label='İdeal')
            ax2.set_title(f'{emoji} {ders}\nÇoklu Regresyon', fontsize=13, fontweight='bold', pad=15)
            ax2.text(0.05, 0.95, f"R² = {coklu['r2']:.3f}\nRMSE = {coklu['rmse']:.2f}",
                    transform=ax2.transAxes, fontsize=10, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor=color, alpha=0.3))
            ax2.set_xlabel('Gerçek Karne T-Puanı', fontweight='bold')
            ax2.set_ylabel('Tahmin', fontweight='bold')
            ax2.legend(loc='lower right')
            ax2.grid(True, alpha=0.3)
            
            ax3 = plt.subplot(3, 5, i + 11)
            katsayilar = coklu['katsayilar']
            colors = [self.DERSLER[d][2] for d in self.DERSLER]
            bars = ax3.bar(range(len(self.DERSLER)), katsayilar, color=colors, 
                          alpha=0.8, edgecolor='white', linewidth=2)
            ax3.axhline(y=0, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.7)
            
            for bar, val in zip(bars, katsayilar):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{val:.2f}', ha='center', 
                        va='bottom' if val > 0 else 'top',
                        fontsize=10, fontweight='bold')
            
            ax3.set_title(f'{emoji} {ders}\nKatsayılar', fontsize=13, fontweight='bold', pad=15)
            ax3.set_ylabel('Katsayı', fontweight='bold')
            ax3.set_xticks(range(len(self.DERSLER)))
            ax3.set_xticklabels([d.split()[0] for d in self.DERSLER.keys()], 
                               rotation=0, fontsize=10, fontweight='bold')
            ax3.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        
        grafik_dosya = Path(output_dir) / "regresyon_analizi.png"
        plt.savefig(grafik_dosya, dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
        print(f"  ✓ Grafik kaydedildi: {grafik_dosya}")
        
        plt.show()
    
    def rapor_olustur(self, output_dir="output"):
        print(f"\nRapor oluşturuluyor ({output_dir}/)...")
        
        Path(output_dir).mkdir(exist_ok=True)
        
        print("\n" + "=" * 90)
        print(" " * 25 + "REGRESYON ANALİZİ RAPORU")
        print("=" * 90 + "\n")
        
        print("BASİT REGRESYON SONUÇLARI")
        print("-" * 90)
        basit_data = []
        for ders in self.DERSLER:
            basit = self.sonuclar[ders]['basit']
            basit_data.append({
                'Ders': ders,
                'R²': f"{basit['r2']:.4f}",
                'RMSE': f"{basit['rmse']:.3f}",
                'Eğim': f"{basit['slope']:.3f}",
                'Kesim': f"{basit['intercept']:.3f}"
            })
        
        basit_df = pd.DataFrame(basit_data)
        print(basit_df.to_string(index=False))
        
        print("\n\nÇOKLU REGRESYON SONUÇLARI")
        print("-" * 90)
        coklu_data = []
        for ders in self.DERSLER:
            basit = self.sonuclar[ders]['basit']
            coklu = self.sonuclar[ders]['coklu']
            coklu_data.append({
                'Ders': ders,
                'R²': f"{coklu['r2']:.4f}",
                'RMSE': f"{coklu['rmse']:.3f}",
                'R² Artışı': f"{coklu['r2'] - basit['r2']:.4f}",
                'İyileşme %': f"{(coklu['r2'] - basit['r2']) * 100:.1f}%"
            })
        
        coklu_df = pd.DataFrame(coklu_data)
        print(coklu_df.to_string(index=False))
        
        print("\n\nÖZET İSTATİSTİKLER")
        print("-" * 90)
        print(f"Toplam Öğrenci Sayısı:    {len(self.veri)}")
        print(f"Analiz Edilen Ders:       {len(self.DERSLER)}")
        
        avg_r2_basit = np.mean([self.sonuclar[d]['basit']['r2'] for d in self.DERSLER])
        avg_r2_coklu = np.mean([self.sonuclar[d]['coklu']['r2'] for d in self.DERSLER])
        
        print(f"Ortalama Basit R²:        {avg_r2_basit:.4f}")
        print(f"Ortalama Çoklu R²:        {avg_r2_coklu:.4f}")
        print(f"Ortalama İyileşme:        +{(avg_r2_coklu - avg_r2_basit) * 100:.1f}%")
        
        en_iyi = max(self.DERSLER.keys(), 
                    key=lambda d: self.sonuclar[d]['coklu']['r2'])
        print(f"En İyi Tahmin:            {en_iyi} (R²={self.sonuclar[en_iyi]['coklu']['r2']:.4f})")
        
        print("\n" + "=" * 90 + "\n")
        
        karsilastirma = pd.DataFrame([{
            'Ders': ders,
            'Basit_R2': self.sonuclar[ders]['basit']['r2'],
            'Basit_RMSE': self.sonuclar[ders]['basit']['rmse'],
            'Coklu_R2': self.sonuclar[ders]['coklu']['r2'],
            'Coklu_RMSE': self.sonuclar[ders]['coklu']['rmse'],
            'R2_Artisi': self.sonuclar[ders]['coklu']['r2'] - self.sonuclar[ders]['basit']['r2']
        } for ders in self.DERSLER])
        
        csv_dosya = Path(output_dir) / "regresyon_karsilastirma.csv"
        karsilastirma.to_csv(csv_dosya, index=False)
        print(f"  ✓ CSV rapor kaydedildi: {csv_dosya}")
        
        detayli_dosya = Path(output_dir) / "detayli_sonuclar.csv"
        detayli_data = []
        
        for _, row in self.veri.iterrows():
            for ders in self.DERSLER:
                detayli_data.append({
                    'RUMUZ': row['RUMUZ'],
                    'Ders': ders,
                    'Sinav_T': row[f"{ders}_T_SINAV"],
                    'Karne_T': row[f"{ders}_T_KARNE"],
                    'Tahmin_Basit': self.sonuclar[ders]['basit']['model'].predict(
                        [[row[f"{ders}_T_SINAV"]]])[0],
                    'Tahmin_Coklu': self.sonuclar[ders]['coklu']['y_pred'][_]
                })
        
        pd.DataFrame(detayli_data).to_csv(detayli_dosya, index=False)
        print(f"  ✓ Detaylı sonuçlar kaydedildi: {detayli_dosya}")
    
    def calistir(self, output_dir="output", grafik_goster=True):
        if not self.veri_yukle():
            return False
        
        self.t_puanlarini_ekle()
        self.verileri_birlestir()
        self.analiz_yap()
        
        if grafik_goster:
            self.grafik_olustur(output_dir)
        
        self.rapor_olustur(output_dir)
        
        print("\n✅ Analiz tamamlandı!")
        return True


def demo_veri_olustur():
    print("Demo veriler oluşturuluyor...")
    
    np.random.seed(42)
    n = 30
    
    sinav = pd.DataFrame({
        'RUMUZ': [f'OGR{i:03d}' for i in range(1, n + 1)],
        'TDS': np.random.randint(60, 100, n),
        'MDS': np.random.randint(60, 100, n),
        'FDS': np.random.randint(60, 100, n),
        'SDS': np.random.randint(60, 100, n),
        'DDS': np.random.randint(60, 100, n)
    })
    
    karne = pd.DataFrame({
        'RUMUZ': [f'OGR{i:03d}' for i in range(1, n + 1)],
        'TURKCE': (sinav['TDS'] / 20 + np.random.normal(0, 0.2, n)).round(1),
        'MAT': (sinav['MDS'] / 20 + np.random.normal(0, 0.2, n)).round(1),
        'FEN': (sinav['FDS'] / 20 + np.random.normal(0, 0.2, n)).round(1),
        'SOSYAL': (sinav['SDS'] / 20 + np.random.normal(0, 0.2, n)).round(1),
        'DIN': (sinav['DDS'] / 20 + np.random.normal(0, 0.2, n)).round(1)
    })
    
    Path("demo_data").mkdir(exist_ok=True)
    sinav.to_csv('demo_data/sinav_demo.csv', sep=';', index=False)
    karne.to_csv('demo_data/karne_demo.csv', sep=';', index=False, decimal=',')
    
    print("✅ Demo veriler oluşturuldu: demo_data/")
    return 'demo_data/sinav_demo.csv', 'demo_data/karne_demo.csv'


def main():
    parser = argparse.ArgumentParser(
        description='Sınav-Karne Regresyon Analizi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python analiz.py --sinav sinav.csv --karne karne.csv
  python analiz.py --sinav sinav.csv --karne karne.csv --output results/
  python analiz.py --demo
  python analiz.py --demo --no-plot
        """
    )
    
    parser.add_argument('--sinav', type=str, help='Sınav CSV dosyası')
    parser.add_argument('--karne', type=str, help='Karne CSV dosyası')
    parser.add_argument('--output', type=str, default='output', 
                       help='Çıktı klasörü (varsayılan: output)')
    parser.add_argument('--demo', action='store_true', 
                       help='Demo verilerle çalıştır')
    parser.add_argument('--no-plot', action='store_true', 
                       help='Grafikleri gösterme')
    
    args = parser.parse_args()
    
    print("\n" + "="*90)
    print(" " * 20 + "SINAV-KARNE ANALİZ PLATFORMU")
    print("="*90 + "\n")
    
    if args.demo:
        sinav_dosya, karne_dosya = demo_veri_olustur()
    elif args.sinav and args.karne:
        sinav_dosya = args.sinav
        karne_dosya = args.karne
    else:
        parser.print_help()
        sys.exit(1)
    
    analiz = SinavKarneAnaliz(sinav_dosya, karne_dosya)
    analiz.calistir(args.output, not args.no_plot)


if __name__ == "__main__":
    main()
