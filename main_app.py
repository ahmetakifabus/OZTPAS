
import os
import shutil
import uuid
import zipfile
import hashlib
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file, session
import traceback
import matplotlib
matplotlib.use('Agg') # Set backend to non-interactive

# Import the existing analysis class
# We need to ensure OZTPBS.py is in the same directory or python path
try:
    from OZTPBS import SinavKarneAnaliz
except ImportError:
    print("Error: OZTPBS.py not found. Make sure it is in the same directory.")
    SinavKarneAnaliz = None

app = Flask(__name__)

# Ensure upload root exists
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.secret_key = os.environ.get('SECRET_KEY', 'oztpbs-secret-key-123')

class InitializedAnaliz(SinavKarneAnaliz):
    """Subclass to override methods for web usage"""
    def grafik_olustur(self, output_dir="output"):
        # Copy of original method but without plt.show()
        import matplotlib.pyplot as plt
        from pathlib import Path
        
        # We assume data is already processed
        print(f"Grafikler web için oluşturuluyor ({output_dir})...")
        Path(output_dir).mkdir(exist_ok=True, parents=True)
        
        fig = plt.figure(figsize=(22, 16), facecolor='#f8f9fa')
        fig.suptitle('SINAV-KARNE REGRESYON ANALİZİ', fontsize=28, fontweight='bold', y=0.98)
        
        for i, (ders, (_, _, color, emoji)) in enumerate(self.DERSLER.items()):
            basit = self.sonuclar[ders]['basit']
            coklu = self.sonuclar[ders]['coklu']
            
            x = self.veri[f"{ders}_T_SINAV"].values
            y = self.veri[f"{ders}_T_KARNE"].values
            
            # 1. Basit Regresyon Grafiği
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
            
            # 2. Çoklu Regresyon Grafiği
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
            
            # 3. Katsayılar Grafiği
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
        plt.close(fig) # Close explicitly
        return str(grafik_dosya)

def get_user_dir():
    # Use session for stable user directory across requests
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    user_id = session['user_id']
    user_path = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    return user_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'sinav' not in request.files or 'karne' not in request.files:
        return jsonify({'error': 'Dosyalar eksik'}), 400
    
    sinav_file = request.files['sinav']
    karne_file = request.files['karne']
    
    if sinav_file.filename == '' or karne_file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi'}), 400

    user_path = get_user_dir()
    
    # Save files
    sinav_path = os.path.join(user_path, 'sinav.csv')
    karne_path = os.path.join(user_path, 'karne.csv')
    sinav_file.save(sinav_path)
    karne_file.save(karne_path)
    
    # Run Analysis
    try:
        analiz = InitializedAnaliz(sinav_path, karne_path)
        # Manually run pipeline to skip plt.show in calistir
        if not analiz.veri_yukle():
             return jsonify({'error': 'Veri yükleme başarısız. Dosyaları kontrol edin.'}), 500
        
        analiz.t_puanlarini_ekle()
        analiz.verileri_birlestir()
        analiz.analiz_yap()
        
        # Override output dir to user path
        img_path = analiz.grafik_olustur(user_path)
        analiz.rapor_olustur(user_path)
        
        # Prepare response
        return jsonify({
            'status': 'success',
            'image_url': f'/results/regresyon_analizi.png?t={uuid.uuid4()}',
            'csv_url': f'/results/regresyon_karsilastirma.csv?t={uuid.uuid4()}',
            'detail_url': f'/results/detayli_sonuclar.csv?t={uuid.uuid4()}'
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Analiz hatası: {str(e)}'}), 500

@app.route('/results/<filename>')
def serve_result(filename):
    user_path = get_user_dir()
    return send_from_directory(user_path, filename)

@app.route('/download_zip')
def download_zip():
    try:
        user_path = get_user_dir()
        zip_path = os.path.join(user_path, 'sonuclar.zip')
        
        if os.path.exists(zip_path):
            os.remove(zip_path) # Remove old if exists
            
        with zipfile.ZipFile(zip_path, 'w') as zf:
            added = False
            for f in ['regresyon_analizi.png', 'regresyon_karsilastirma.csv', 'detayli_sonuclar.csv']:
                full_path = os.path.join(user_path, f)
                if os.path.exists(full_path):
                    zf.write(full_path, f)
                    added = True
            
            if not added:
                 zf.writestr('info.txt', 'Analiz sonuclari bulunamadi. Lütfen tekrar analiz yapın.')
                    
        return send_file(zip_path, as_attachment=True)
    except Exception as e:
        traceback.print_exc()
        return str(e), 500

@app.route('/cleanup', methods=['POST'])
def cleanup():
    user_path = get_user_dir()
    try:
        # Instead of deleting immediately, we could also use a timer 
        # but for this simple version, let's just make it a conscious action
        if os.path.exists(user_path):
            # Only remove if specifically asked or on next upload
            shutil.rmtree(user_path)
        return jsonify({'status': 'cleaned'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import webbrowser
    from threading import Timer
    
    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5000")
        
    Timer(1, open_browser).start()
    app.run(debug=True, port=5000)
