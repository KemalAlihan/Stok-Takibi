import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class StockManager:
    def __init__(self, database):
        self.db = database
        
    def create_interface(self, parent):
        # Ana frame
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Üst panel - Stok işlem formu
        top_frame = ttk.LabelFrame(main_frame, text="Stok İşlemi", padding=10)
        top_frame.pack(fill='x', pady=(0, 10))
        
        # Form alanları - 2 sütunlu düzen
        form_frame = ttk.Frame(top_frame)
        form_frame.pack(fill='x')
        
        # Sol sütun
        left_col = ttk.Frame(form_frame)
        left_col.pack(side='left', fill='x', expand=True, padx=(0, 20))
        
        ttk.Label(left_col, text="Ürün Seç:").grid(row=0, column=0, sticky='w', pady=5)
        self.product_combo = ttk.Combobox(left_col, width=30, state='readonly')
        self.product_combo.grid(row=0, column=1, pady=5, sticky='ew')
        self.product_combo.bind('<<ComboboxSelected>>', self.on_product_select)
        
        ttk.Label(left_col, text="İşlem Tipi:").grid(row=1, column=0, sticky='w', pady=5)
        self.operation_combo = ttk.Combobox(left_col, width=30, state='readonly')
        self.operation_combo['values'] = ('Stok Girişi', 'Stok Çıkışı')
        self.operation_combo.set('Stok Girişi')
        self.operation_combo.grid(row=1, column=1, pady=5, sticky='ew')
        
        ttk.Label(left_col, text="Miktar:").grid(row=2, column=0, sticky='w', pady=5)
        self.quantity_entry = ttk.Entry(left_col, width=30)
        self.quantity_entry.grid(row=2, column=1, pady=5, sticky='ew')
        
        left_col.columnconfigure(1, weight=1)
        
        # Sağ sütun
        right_col = ttk.Frame(form_frame)
        right_col.pack(side='right', fill='x', expand=True)
        
        ttk.Label(right_col, text="Birim Fiyat:").grid(row=0, column=0, sticky='w', pady=5)
        self.unit_price_entry = ttk.Entry(right_col, width=30)
        self.unit_price_entry.grid(row=0, column=1, pady=5, sticky='ew')
        
        ttk.Label(right_col, text="Toplam Fiyat:").grid(row=1, column=0, sticky='w', pady=5)
        self.total_price_label = ttk.Label(right_col, text="0.00 ₺", 
                                          font=('Arial', 10, 'bold'), foreground='blue')
        self.total_price_label.grid(row=1, column=1, pady=5, sticky='w')
        
        ttk.Label(right_col, text="Not:").grid(row=2, column=0, sticky='w', pady=5)
        self.note_entry = ttk.Entry(right_col, width=30)
        self.note_entry.grid(row=2, column=1, pady=5, sticky='ew')
        
        right_col.columnconfigure(1, weight=1)
        
        # Miktar ve fiyat değişikliklerini dinle
        self.quantity_entry.bind('<KeyRelease>', self.calculate_total)
        self.unit_price_entry.bind('<KeyRelease>', self.calculate_total)
        
        # Butonlar
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="İşlemi Kaydet", 
                  command=self.save_stock_movement).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Formu Temizle", 
                  command=self.clear_form).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Düşük Stok Uyarıları", 
                  command=self.show_low_stock_alert).pack(side='left', padx=5)
        
        # Alt panel - Stok hareketleri listesi
        bottom_frame = ttk.LabelFrame(main_frame, text="Son Stok Hareketleri", padding=10)
        bottom_frame.pack(fill='both', expand=True)
        
        # Hareket tablosu
        columns = ('Tarih', 'Ürün', 'İşlem', 'Miktar', 'Birim Fiyat', 'Toplam', 'Not')
        self.movement_tree = ttk.Treeview(bottom_frame, columns=columns, show='headings', height=15)
        
        # Sütun başlıkları ve genişlikleri
        column_widths = {'Tarih': 120, 'Ürün': 200, 'İşlem': 80, 'Miktar': 80, 
                        'Birim Fiyat': 100, 'Toplam': 100, 'Not': 150}
        
        for col in columns:
            self.movement_tree.heading(col, text=col)
            self.movement_tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbar
        movement_scrollbar = ttk.Scrollbar(bottom_frame, orient='vertical', 
                                         command=self.movement_tree.yview)
        self.movement_tree.configure(yscrollcommand=movement_scrollbar.set)
        
        self.movement_tree.pack(side='left', fill='both', expand=True)
        movement_scrollbar.pack(side='right', fill='y')
        
        # Başlangıçta verileri yükle
        self.load_products()
        self.refresh_movements()
    
    def load_products(self):
        """Ürünleri combobox'a yükle"""
        products = self.db.get_all_products()
        product_list = [f"{product[0]} - {product[1]} (Stok: {product[5]})" for product in products]
        self.product_combo['values'] = product_list
    
    def on_product_select(self, event):
        """Ürün seçildiğinde fiyat bilgisini otomatik doldur"""
        selected = self.product_combo.get()
        if selected:
            product_id = int(selected.split(' - ')[0])
            products = self.db.get_all_products()
            for product in products:
                if product[0] == product_id:
                    self.unit_price_entry.delete(0, tk.END)
                    self.unit_price_entry.insert(0, str(product[4]))  # unit_price
                    break
    
    def calculate_total(self, event=None):
        """Toplam fiyatı hesapla"""
        try:
            quantity = float(self.quantity_entry.get() or 0)
            unit_price = float(self.unit_price_entry.get() or 0)
            total = quantity * unit_price
            self.total_price_label.config(text=f"{total:.2f} ₺")
        except ValueError:
            self.total_price_label.config(text="0.00 ₺")
    
    def save_stock_movement(self):
        try:
            # Form verilerini al
            selected_product = self.product_combo.get()
            if not selected_product:
                messagebox.showerror("Hata", "Lütfen bir ürün seçin!")
                return
            
            product_id = int(selected_product.split(' - ')[0])
            operation = self.operation_combo.get()
            quantity = int(self.quantity_entry.get())
            unit_price = float(self.unit_price_entry.get())
            note = self.note_entry.get().strip()
            
            if quantity <= 0:
                messagebox.showerror("Hata", "Miktar 0'dan büyük olmalıdır!")
                return
            
            # İşlem tipini belirle
            movement_type = 'IN' if operation == 'Stok Girişi' else 'OUT'
            
            # Mevcut stok miktarını al
            products = self.db.get_all_products()
            current_stock = 0
            for product in products:
                if product[0] == product_id:
                    current_stock = product[5]
                    break
            
            # Stok çıkışında yeterli stok kontrolü
            if movement_type == 'OUT' and quantity > current_stock:
                messagebox.showerror("Hata", f"Yetersiz stok! Mevcut stok: {current_stock}")
                return
            
            # Yeni stok miktarını hesapla
            if movement_type == 'IN':
                new_stock = current_stock + quantity
            else:
                new_stock = current_stock - quantity
            
            # Veritabanı işlemleri
            self.db.add_stock_movement(product_id, movement_type, quantity, unit_price, note)
            self.db.update_product_stock(product_id, new_stock)
            
            messagebox.showinfo("Başarılı", "Stok hareketi başarıyla kaydedildi!")
            
            # Formu temizle ve listeleri yenile
            self.clear_form()
            self.load_products()
            self.refresh_movements()
            
        except ValueError:
            messagebox.showerror("Hata", "Miktar ve fiyat alanları sayısal değer olmalıdır!")
        except Exception as e:
            messagebox.showerror("Hata", f"İşlem kaydedilirken hata oluştu: {str(e)}")
    
    def clear_form(self):
        """Formu temizle"""
        self.product_combo.set('')
        self.operation_combo.set('Stok Girişi')
        self.quantity_entry.delete(0, tk.END)
        self.unit_price_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)
        self.total_price_label.config(text="0.00 ₺")
    
    def refresh_movements(self):
        """Stok hareketleri listesini yenile"""
        # Mevcut verileri temizle
        for item in self.movement_tree.get_children():
            self.movement_tree.delete(item)
        
        # Son hareketleri getir
        query = '''
            SELECT sm.movement_date, p.name, sm.movement_type, sm.quantity, 
                   sm.unit_price, sm.total_price, sm.note
            FROM stock_movements sm
            JOIN products p ON sm.product_id = p.id
            ORDER BY sm.movement_date DESC
            LIMIT 100
        '''
        movements = self.db.execute_query(query)
        
        for movement in movements:
            # Tarihi formatla
            date_str = movement[0][:16] if movement[0] else ''
            
            # İşlem tipini Türkçe'ye çevir
            operation_text = 'Giriş' if movement[2] == 'IN' else 'Çıkış'
            
            # Renk kodlaması için tag
            tags = ('stock_in',) if movement[2] == 'IN' else ('stock_out',)
            
            values = (date_str, movement[1], operation_text, movement[3], 
                     f"{movement[4]:.2f} ₺", f"{movement[5]:.2f} ₺", movement[6] or '')
            
            self.movement_tree.insert('', 'end', values=values, tags=tags)
        
        # Renk ayarları
        self.movement_tree.tag_configure('stock_in', background='#e8f5e8')
        self.movement_tree.tag_configure('stock_out', background='#ffe8e8')
    
    def show_low_stock_alert(self):
        """Düşük stok uyarılarını göster"""
        low_stock_products = self.db.get_low_stock_products()
        
        if not low_stock_products:
            messagebox.showinfo("Bilgi", "Düşük stoklu ürün bulunmuyor!")
            return
        
        # Uyarı penceresi oluştur
        alert_window = tk.Toplevel()
        alert_window.title("Düşük Stok Uyarıları")
        alert_window.geometry("600x400")
        alert_window.configure(bg='#fff3cd')
        
        # Başlık
        title_label = tk.Label(alert_window, text="⚠️ DÜŞÜK STOK UYARISI", 
                              font=('Arial', 16, 'bold'), 
                              bg='#fff3cd', fg='#856404')
        title_label.pack(pady=10)
        
        # Uyarı tablosu
        columns = ('Ürün Adı', 'Kategori', 'Mevcut Stok', 'Min. Stok')
        alert_tree = ttk.Treeview(alert_window, columns=columns, show='headings', height=15)
        
        for col in columns:
            alert_tree.heading(col, text=col)
            alert_tree.column(col, width=140)
        
        # Verileri ekle
        for product in low_stock_products:
            alert_tree.insert('', 'end', values=(product[1], product[4], product[2], product[3]))
        
        alert_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Kapat butonu
        ttk.Button(alert_window, text="Kapat", 
                  command=alert_window.destroy).pack(pady=10)