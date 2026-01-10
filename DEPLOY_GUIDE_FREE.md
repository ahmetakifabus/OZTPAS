# Disk Alanı Sorunu Çözümü (PythonAnywhere)

"Disk quota exceeded" hatası aldınız çünkü kütüphaneler çok yer kaplıyor. Ücretsiz hesapta alan kısıtlıdır.

**Çözüm: PythonAnywhere'in hazır kütüphanelerini kullanacağız (Yükleme yapmadan).**

1.  **Temizlik Yapın (Konsolda)**:
    *   Siyah ekrana (Bash) şu komutu yazıp Enter'a basın (Yarım kalan her şeyi siler):
        `rm -rf mysite`

2.  **Kodları Tekrar Çekin**:
    *   `git clone https://github.com/KULLANICIADINIZ/OZTPBS.git mysite`
    *   *(KULLANICIADINIZ kısmını düzeltmeyi unutmayın)*

3.  **YÜKLEME YAPMAYIN (ÖNEMLİ)**:
    *   `pip install`, `venv` vb. komutları **KULLANMAYACAĞIZ**.
    *   PythonAnywhere içinde Flask, Pandas, Matplotlib zaten yüklü geliyor. Onları kullanacağız.

4.  **Web Ayarları**:
    *   Sol üstten **Web** sekmesine gidin.
    *   **Source code:** kısmına `/home/SİZİN_KULLANICI_ADINIZ/mysite` yazın.
    *   **Virtualenv:** kısmını **BOŞ BIRAKIN** (Silin).

5.  **WSGI Dosyasını Ayarlayın**:
    *   **WSGI configuration file** linkine tıklayın.
    *   İçini temizleyip şunu yapıştırın (Kullanıcı adınızı düzeltin):
        ```python
        import sys
        import os
        
        # Proje yolunu ekle
        path = '/home/SİZİN_KULLANICI_ADINIZ/mysite'
        if path not in sys.path:
            sys.path.append(path)
            
        from app import app as application
        ```
    *   **Save** butonuna basın.

6.  **Başlatın**:
    *   Web sekmesine dönüp **Reload** butonuna basın.

Bu yöntemle hiç disk alanı harcamazsınız! 🚀
