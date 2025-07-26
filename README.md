# 📦 Stok Takip Sistemi

Modern ve kullanıcı dostu masaüstü stok takip uygulaması. Python Tkinter ile geliştirilmiş, SQLite veritabanı kullanan tam fonksiyonel bir envanter yönetim sistemi.

## ✨ Öne Çıkan Özellikler

🎯 **Kolay Kullanım**: Sezgisel arayüz tasarımı ile hızlı öğrenme  
🔄 **Gerçek Zamanlı**: Anlık stok güncellemeleri ve uyarılar  
📊 **Kapsamlı Raporlar**: Excel export ve yazdırma desteği  
🔍 **Akıllı Arama**: Ürün adı, barkod ve kategoriye göre filtreleme  
⚡ **Hızlı İşlem**: Tek tıkla stok giriş/çıkış işlemleri  

## 🚀 Detaylı Özellikler

### 📋 Ürün Yönetimi
- ✅ **Ürün Ekleme/Düzenleme**: Kapsamlı ürün bilgi formu
- ✅ **Akıllı Barkod**: 13 haneli EAN-13 formatında otomatik barkod üretimi
- ✅ **Kategori Sistemi**: Esnek kategori yapısı ile ürün organizasyonu
- ✅ **Minimum Stok**: Kişiselleştirilebilir minimum stok seviyeleri
- ✅ **Görsel Uyarılar**: Düşük stoklu ürünler için renk kodlaması
- ✅ **Hızlı Arama**: Gerçek zamanlı arama ve filtreleme
- ✅ **Sağ Tık Menü**: Hızlı düzenleme ve silme işlemleri

### 📊 Stok İşlemleri
- ✅ **Giriş/Çıkış Kayıtları**: Detaylı stok hareket takibi
- ✅ **Otomatik Hesaplama**: Birim fiyat × miktar = toplam tutar
- ✅ **Stok Kontrolü**: Yetersiz stok durumunda otomatik uyarı
- ✅ **İşlem Geçmişi**: Tüm stok hareketlerinin kronolojik kaydı
- ✅ **Renk Kodlaması**: Giriş (yeşil) ve çıkış (kırmızı) işlemleri
- ✅ **Not Sistemi**: Her işlem için açıklama alanı
- ✅ **Düşük Stok Uyarıları**: Kritik seviyedeki ürünler için popup uyarı

### 📈 Gelişmiş Raporlama
- ✅ **Stok Özet Raporu**: Tüm ürünlerin detaylı durumu
- ✅ **Stok Hareketleri**: Tarih bazlı işlem geçmişi
- ✅ **Düşük Stok Analizi**: Kritik seviyedeki ürünler ve maliyet hesabı
- ✅ **Değer Analizi**: En değerli ürünler ve kategori bazlı analiz
- ✅ **Tarih Filtreleme**: Bugün, bu hafta, bu ay seçenekleri
- ✅ **Özet Kartları**: Görsel dashboard ile hızlı bilgi
- ✅ **Excel Export**: Profesyonel XLSX formatında raporlar
- ✅ **Yazdırma**: HTML formatında yazdırma desteği
- ✅ **Detaylı Analiz**: Öneriler ve istatistiksel bilgiler

## 🛠️ Teknoloji Altyapısı

| Teknoloji | Versiyon | Kullanım Alanı |
|-----------|----------|----------------|
| **Python** | 3.6+ | Ana programlama dili |
| **Tkinter/ttk** | Built-in | Modern GUI framework |
| **SQLite** | 3.x | Hafif veritabanı sistemi |
| **openpyxl** | 3.x | Excel dosya işlemleri |
| **HTML/CSS** | - | Yazdırma ve raporlama |

### 🏗️ Mimari Yapı
- **MVC Pattern**: Model-View-Controller tasarım deseni
- **Modüler Yapı**: Her özellik ayrı modülde organize
- **Database Layer**: Veritabanı işlemleri için ayrı katman
- **Error Handling**: Kapsamlı hata yönetimi sistemi

## 📁 Proje Yapısı

```
Stok Takibi/
│
├── 📄 main.py              # Ana uygulama ve GUI koordinatörü
├── 🗄️ database.py          # SQLite veritabanı yönetimi ve sorguları
├── 📦 product_manager.py   # Ürün CRUD işlemleri ve arayüzü
├── 📊 stock_manager.py     # Stok giriş/çıkış işlemleri
├── 📈 report_manager.py    # Raporlama ve analiz modülü
├── 🗃️ stok_takip.db       # SQLite veritabanı dosyası (otomatik oluşur)
├── 📚 README.md           # Proje dokümantasyonu
└── 📁 __pycache__/        # Python cache dosyaları
```

### 🔧 Modül Detayları

| Dosya | Satır Sayısı | Ana Fonksiyonlar |
|-------|--------------|------------------|
| `main.py` | ~100 | Uygulama başlatma, tab yönetimi |
| `database.py` | ~200 | Veritabanı bağlantısı, CRUD işlemleri |
| `product_manager.py` | ~500 | Ürün ekleme/düzenleme/silme, arama |
| `stock_manager.py` | ~300 | Stok hareketleri, uyarı sistemi |
| `report_manager.py` | ~1000 | Raporlama, Excel export, yazdırma |

## 🚀 Kurulum ve Çalıştırma

### ⚙️ Sistem Gereksinimleri
- **İşletim Sistemi**: Windows 10/11, macOS 10.14+, Linux Ubuntu 18.04+
- **Python**: 3.6 veya üzeri (önerilen: 3.8+)
- **RAM**: Minimum 512 MB (önerilen: 1 GB)
- **Disk Alanı**: 50 MB boş alan

### 📦 Hızlı Kurulum

#### 1. Python Kontrolü
```bash
python --version
# veya
python3 --version
```

#### 2. Gerekli Kütüphane
```bash
pip install openpyxl
```

#### 3. Uygulamayı Çalıştır
```bash
# Proje klasörüne git
cd "Stok Takibi"

# Uygulamayı başlat
python main.py
```

### 🐍 Alternatif Kurulum (Virtual Environment)
```bash
# Virtual environment oluştur
python -m venv stok_env

# Aktifleştir (Windows)
stok_env\Scripts\activate

# Aktifleştir (macOS/Linux)
source stok_env/bin/activate

# Kütüphane yükle
pip install openpyxl

# Uygulamayı çalıştır
python main.py
```

### 🔧 Sorun Giderme
- **Tkinter hatası**: `sudo apt-get install python3-tk` (Linux)
- **openpyxl hatası**: `pip install --upgrade openpyxl`
- **Encoding hatası**: Dosyaları UTF-8 formatında kaydedin

## 📖 Detaylı Kullanım Kılavuzu

### 🎯 İlk Çalıştırma
Uygulama ilk kez çalıştırıldığında:
- ✅ SQLite veritabanı (`stok_takip.db`) otomatik oluşturulur
- ✅ Tüm tablolar ve indeksler kurulur

### 📦 Ürün Yönetimi Rehberi

#### ➕ Yeni Ürün Ekleme
1. **Ürün Yönetimi** sekmesine gidin
2. Sol paneldeki formu doldurun:
   - **Ürün Adı**: Benzersiz ürün ismi
   - **Barkod**: Manuel girin veya "Oluştur" ile otomatik EAN-13
   - **Kategori**: Dropdown'dan seçin
   - **Birim Fiyat**: Satış fiyatı (₺)
   - **Min. Stok**: Uyarı seviyesi (varsayılan: 5)
   - **Açıklama**: Opsiyonel detay bilgi
3. **"Ürün Ekle"** butonuna tıklayın

#### 🔍 Ürün Arama ve Filtreleme
- **Hızlı Arama**: Sağ üstteki arama kutusuna yazın
- **Arama Kriterleri**: Ürün adı, barkod, kategori
- **Gerçek Zamanlı**: Yazdıkça sonuçlar güncellenir
- **Renk Kodları**: 🔴 Kırmızı = Düşük stok

#### ✏️ Ürün Düzenleme/Silme
- **Sağ Tık**: Ürün üzerinde sağ tıklayın
- **Düzenle**: Tüm bilgileri güncelleyebilirsiniz
- **Sil**: Onay ile birlikte kalıcı silme (stok hareketleri dahil)

### 📊 Stok İşlemleri Rehberi

#### 📥 Stok Girişi (Alım)
1. **Stok İşlemleri** sekmesine gidin
2. **Ürün Seç**: Dropdown'dan ürünü seçin
3. **İşlem Tipi**: "Stok Girişi" seçili olsun
4. **Miktar**: Giriş yapılacak adet
5. **Birim Fiyat**: Otomatik dolar, değiştirilebilir
6. **Not**: Tedarikçi, fatura no vb. (opsiyonel)
7. **"İşlemi Kaydet"** butonuna tıklayın

#### 📤 Stok Çıkışı (Satış)
1. **İşlem Tipi**: "Stok Çıkışı" seçin
2. Diğer adımlar giriş ile aynı
3. **Otomatik Kontrol**: Yetersiz stok uyarısı
4. **Stok Güncelleme**: Otomatik azaltma

#### ⚠️ Düşük Stok Uyarıları
- **"Düşük Stok Uyarıları"** butonuna tıklayın
- Kritik seviyedeki tüm ürünleri görün
- Minimum stok seviyesinin altındaki ürünler listelenir

### 📈 Raporlama Sistemi

#### 📋 Rapor Türleri
1. **Stok Özeti**: Tüm ürünlerin mevcut durumu
2. **Stok Hareketleri**: Giriş/çıkış işlem geçmişi  
3. **Düşük Stok**: Kritik seviyedeki ürünler
4. **Değer Analizi**: En değerli ürünler ve oranlar

#### 📅 Tarih Filtreleme
- **Tümü**: Tüm kayıtlar
- **Bugün**: Sadece bugünkü işlemler
- **Bu Hafta**: Son 7 gün
- **Bu Ay**: Son 30 gün

#### 📄 Export ve Yazdırma
- **Excel Export**: Profesyonel XLSX formatı
- **Yazdırma**: HTML formatında çıktı
- **Otomatik Açma**: Export sonrası dosyayı açma seçeneği

### 💡 İpuçları ve Püf Noktaları

#### 🎯 Verimli Kullanım
- **Klavye Kısayolları**: Tab ile form alanları arası geçiş
- **Hızlı Barkod**: "Oluştur" butonu ile anında EAN-13 kodu
- **Toplu İşlem**: Aynı ürün için birden fazla stok hareketi
- **Düzenli Yedekleme**: `stok_takip.db` dosyasını yedekleyin

#### 🔧 Bakım ve Optimizasyon
- **Veritabanı Boyutu**: Eski kayıtları periyodik temizleyin
- **Performans**: 1000+ ürün için indeksleme otomatik
- **Yedekleme**: Önemli işlemler öncesi DB yedekleyin

## 🗄️ Veritabanı Yapısı

### 📊 Tablo Şeması

#### `products` - Ürünler
| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | INTEGER | Birincil anahtar (otomatik artan) |
| `name` | TEXT | Ürün adı (zorunlu) |
| `barcode` | TEXT | Benzersiz barkod (13 haneli) |
| `category_id` | INTEGER | Kategori referansı |
| `unit_price` | REAL | Birim satış fiyatı |
| `current_stock` | INTEGER | Mevcut stok miktarı |
| `min_stock` | INTEGER | Minimum stok seviyesi |
| `description` | TEXT | Ürün açıklaması |
| `created_date` | TIMESTAMP | Oluşturulma tarihi |

#### `categories` - Kategoriler
| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | INTEGER | Birincil anahtar |
| `name` | TEXT | Kategori adı (benzersiz) |
| `description` | TEXT | Kategori açıklaması |
| `created_date` | TIMESTAMP | Oluşturulma tarihi |

#### `stock_movements` - Stok Hareketleri
| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | INTEGER | Birincil anahtar |
| `product_id` | INTEGER | Ürün referansı |
| `movement_type` | TEXT | 'IN' (Giriş) veya 'OUT' (Çıkış) |
| `quantity` | INTEGER | Hareket miktarı |
| `unit_price` | REAL | İşlem anındaki birim fiyat |
| `total_price` | REAL | Toplam tutar (miktar × fiyat) |
| `note` | TEXT | İşlem notu |
| `movement_date` | TIMESTAMP | İşlem tarihi |

#### `suppliers` - Tedarikçiler (Gelecek versiyon)
| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | INTEGER | Birincil anahtar |
| `name` | TEXT | Tedarikçi adı |
| `contact_person` | TEXT | İletişim kişisi |
| `phone` | TEXT | Telefon numarası |
| `email` | TEXT | E-posta adresi |
| `address` | TEXT | Adres bilgisi |

## 🔧 Gelişmiş Özellikler

### 🎨 Kullanıcı Arayüzü
- **Modern Tasarım**: ttk (themed tkinter) bileşenleri
- **Responsive Layout**: Pencere boyutuna uyum
- **Renk Kodlaması**: Durum bazlı görsel ipuçları
- **Tab Sistemi**: Organize edilmiş modül erişimi
- **Context Menu**: Sağ tık ile hızlı işlemler

### 📊 Raporlama Özellikleri
- **Dinamik Tablolar**: Sıralanabilir sütunlar
- **Excel Entegrasyonu**: openpyxl ile profesyonel formatlar
- **Yazdırma Sistemi**: HTML/CSS ile özelleştirilebilir çıktı
- **Grafik Desteği**: Değer analizi ve trend gösterimi
- **Export Seçenekleri**: XLSX, HTML, CSV formatları

### 🔍 Arama ve Filtreleme
- **Gerçek Zamanlı Arama**: Keystroke bazlı filtreleme
- **Çoklu Kriter**: Ad, barkod, kategori araması
- **Regex Desteği**: Gelişmiş arama kalıpları
- **Tarih Aralığı**: Esnek tarih filtreleme seçenekleri

### 🔔 Uyarı Sistemi
- **Düşük Stok**: Minimum seviye altı uyarıları
- **Kritik Seviye**: Sıfır stok uyarıları
- **Popup Bildirimleri**: Önemli işlemler için onay
- **Renk Kodları**: Görsel durum göstergeleri


### 📧 İletişim
- **Geliştirici**: [Kemal Alihan Ölmez]
- **E-posta**: [alihanolmz@gmail.com]
- **GitHub**: [github.com/KemalAlihan]

## 🙏 Teşekkürler

**📦 Stok Takip Sistemi** - Modern, güvenilir ve kullanıcı dostu envanter yönetimi çözümü.