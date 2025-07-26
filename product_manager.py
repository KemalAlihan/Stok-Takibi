import tkinter as tk
from tkinter import ttk, messagebox
import random

class ProductManager:
    def __init__(self, database):
        self.db = database
        self.stock_manager = None
        self.report_manager = None
    
    def set_other_managers(self, stock_manager, report_manager):
        """Diğer manager'lara referans ekle"""
        self.stock_manager = stock_manager
        self.report_manager = report_manager
        
    def create_interface(self, parent):
        # Ana frame
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sol panel - Ürün ekleme formu
        left_frame = ttk.LabelFrame(main_frame, text="Yeni Ürün Ekle", padding=10)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Form alanları
        ttk.Label(left_frame, text="Ürün Adı:").grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry = ttk.Entry(left_frame, width=25)
        self.name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(left_frame, text="Barkod:").grid(row=1, column=0, sticky='w', pady=5)
        self.barcode_frame = ttk.Frame(left_frame)
        self.barcode_frame.grid(row=1, column=1, pady=5)
        
        # Barkod entry'si - maksimum 13 karakter
        self.barcode_entry = ttk.Entry(self.barcode_frame, width=20)
        self.barcode_entry.pack(side='left')
        
        # Karakter sayısı sınırlandırması
        self.barcode_entry.bind('<KeyPress>', self.validate_barcode_length)
        self.barcode_entry.bind('<KeyRelease>', self.update_barcode_counter)
        
        ttk.Button(self.barcode_frame, text="Oluştur", 
                  command=self.generate_barcode, width=8).pack(side='left', padx=(5, 0))
        
        # Karakter sayacı label'ı
        self.barcode_counter = ttk.Label(left_frame, text="0/13", font=('Arial', 8), foreground='gray')
        self.barcode_counter.grid(row=2, column=1, sticky='w', pady=(0, 5))
        
        ttk.Label(left_frame, text="Kategori:").grid(row=3, column=0, sticky='w', pady=5)
        self.category_combo = ttk.Combobox(left_frame, width=22, state='readonly')
        self.category_combo.grid(row=3, column=1, pady=5)
        
        ttk.Label(left_frame, text="Birim Fiyat:").grid(row=4, column=0, sticky='w', pady=5)
        self.price_entry = ttk.Entry(left_frame, width=25)
        self.price_entry.grid(row=4, column=1, pady=5)
        
        ttk.Label(left_frame, text="Min. Stok:").grid(row=5, column=0, sticky='w', pady=5)
        self.min_stock_entry = ttk.Entry(left_frame, width=25)
        self.min_stock_entry.grid(row=5, column=1, pady=5)
        self.min_stock_entry.insert(0, "5")
        
        ttk.Label(left_frame, text="Açıklama:").grid(row=6, column=0, sticky='w', pady=5)
        self.description_text = tk.Text(left_frame, width=25, height=3)
        self.description_text.grid(row=6, column=1, pady=5)
        
        # Butonlar
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Ürün Ekle", 
                  command=self.add_product).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Temizle", 
                  command=self.clear_form).pack(side='left', padx=5)
        
        # Sağ panel - Ürün listesi
        right_frame = ttk.LabelFrame(main_frame, text="Ürün Listesi", padding=10)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Arama çubuğu
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(search_frame, text="Ara:").pack(side='left')
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side='left', padx=(5, 0))
        self.search_entry.bind('<KeyRelease>', self.search_products)
        
        ttk.Button(search_frame, text="Yenile", 
                  command=self.refresh_product_list).pack(side='right')
        
        # Ürün tablosu
        columns = ('ID', 'Ürün Adı', 'Barkod', 'Kategori', 'Fiyat', 'Stok', 'Min.Stok')
        self.product_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        
        # Sütun başlıkları
        for col in columns:
            self.product_tree.heading(col, text=col)
            if col == 'ID':
                self.product_tree.column(col, width=50)
            elif col in ['Fiyat', 'Stok', 'Min.Stok']:
                self.product_tree.column(col, width=80)
            else:
                self.product_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)
        
        self.product_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Sağ tık menüsü
        self.context_menu = tk.Menu(self.product_tree, tearoff=0)
        self.context_menu.add_command(label="Düzenle", command=self.edit_product)
        self.context_menu.add_command(label="Sil", command=self.delete_product)
        
        self.product_tree.bind("<Button-3>", self.show_context_menu)
        
        # Başlangıçta verileri yükle
        self.load_categories()
        self.refresh_product_list()
    
    def validate_barcode_length(self, event):
        """Barkod karakter sayısını sınırlandır"""
        # Özel tuşları (Backspace, Delete, Tab, Enter, Arrow keys) geçir
        special_keys = ['BackSpace', 'Delete', 'Tab', 'Return', 'Left', 'Right', 'Up', 'Down']
        if event.keysym in special_keys:
            return True
        
        current_text = self.barcode_entry.get()
        if len(current_text) >= 13:
            return "break"
        
        # Sadece rakam girişine izin ver
        if not event.char.isdigit():
            return "break"
    
    def update_barcode_counter(self, event=None):
        """Barkod karakter sayacını güncelle"""
        current_length = len(self.barcode_entry.get())
        self.barcode_counter.config(text=f"{current_length}/13")
        
        # Renk kodlaması
        if current_length == 0:
            self.barcode_counter.config(foreground='gray')
        elif current_length < 13:
            self.barcode_counter.config(foreground='orange')
        else:
            self.barcode_counter.config(foreground='green')
    
    def generate_barcode(self):
        """Rastgele barkod oluştur (EAN-13 formatında)"""
        barcode = "869" + "".join([str(random.randint(0, 9)) for _ in range(10)])
        self.barcode_entry.delete(0, tk.END)
        self.barcode_entry.insert(0, barcode)
        self.update_barcode_counter()  # Sayacı güncelle
    
    def load_categories(self):
        """Kategorileri combobox'a yükle"""
        categories = self.db.get_all_categories()
        category_list = [f"{cat[1]}" for cat in categories]
        self.category_combo['values'] = category_list
        if category_list:
            self.category_combo.set(category_list[0])
    
    def add_product(self):
        """Yeni ürün ekle"""
        try:
            name = self.name_entry.get().strip()
            barcode = self.barcode_entry.get().strip()
            category_text = self.category_combo.get()
            price = float(self.price_entry.get())
            min_stock = int(self.min_stock_entry.get())
            description = self.description_text.get(1.0, tk.END).strip()
            
            if not name or not barcode:
                messagebox.showerror("Hata", "Ürün adı ve barkod zorunludur!")
                return
            
            # Kategori ID'sini bul
            categories = self.db.get_all_categories()
            category_id = None
            for cat in categories:
                if cat[1] == category_text:
                    category_id = cat[0]
                    break
            
            if not category_id:
                messagebox.showerror("Hata", "Geçerli bir kategori seçin!")
                return
            
            # Ürünü ekle
            self.db.add_product(name, barcode, category_id, price, min_stock, description)
            
            messagebox.showinfo("Başarılı", "Ürün başarıyla eklendi!")
            self.clear_form()
            self.refresh_product_list()
            
            # Diğer modüllerdeki ürün listelerini de yenile
            self.refresh_other_modules()
            
        except ValueError:
            messagebox.showerror("Hata", "Fiyat ve minimum stok sayısal değer olmalıdır!")
        except Exception as e:
            messagebox.showerror("Hata", f"Ürün eklenirken hata oluştu: {str(e)}")
    
    def clear_form(self):
        """Formu temizle"""
        self.name_entry.delete(0, tk.END)
        self.barcode_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.min_stock_entry.delete(0, tk.END)
        self.min_stock_entry.insert(0, "5")
        self.description_text.delete(1.0, tk.END)
    
    def refresh_product_list(self):
        """Ürün listesini yenile"""
        # Mevcut verileri temizle
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # Yeni verileri yükle
        products = self.db.get_all_products()
        for product in products:
            # Düşük stoklu ürünleri kırmızı renkte göster
            tags = ()
            if product[5] <= product[6]:  # current_stock <= min_stock
                tags = ('low_stock',)
            
            self.product_tree.insert('', 'end', values=product, tags=tags)
        
        # Düşük stok için renk ayarı
        self.product_tree.tag_configure('low_stock', background='#ffcccc')
    
    def search_products(self, event):
        """Ürün ara"""
        search_term = self.search_entry.get().lower()
        
        # Mevcut verileri temizle
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # Filtrelenmiş verileri yükle
        products = self.db.get_all_products()
        for product in products:
            if (search_term in product[1].lower() or  # ürün adı
                search_term in str(product[2]).lower() or  # barkod
                search_term in str(product[3]).lower()):  # kategori
                
                tags = ()
                if product[5] <= product[6]:
                    tags = ('low_stock',)
                
                self.product_tree.insert('', 'end', values=product, tags=tags)
        
        self.product_tree.tag_configure('low_stock', background='#ffcccc')
    
    def show_context_menu(self, event):
        """Sağ tık menüsünü göster"""
        item = self.product_tree.selection()[0] if self.product_tree.selection() else None
        if item:
            self.context_menu.post(event.x_root, event.y_root)
    
    def edit_product(self):
        """Ürün düzenle"""
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Düzenlemek için bir ürün seçin!")
            return
        
        # Seçili ürünün bilgilerini al
        item = self.product_tree.item(selected[0])
        product_data = item['values']
        product_id = product_data[0]
        
        # Düzenleme penceresi oluştur
        self.show_edit_dialog(product_id, product_data)
    
    def delete_product(self):
        """Ürün sil"""
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Silmek için bir ürün seçin!")
            return
        
        # Seçili ürünün bilgilerini al
        item = self.product_tree.item(selected[0])
        product_data = item['values']
        product_id = product_data[0]
        product_name = product_data[1]
        
        # Onay mesajı
        if messagebox.askyesno("Ürün Silme Onayı", 
                              f"'{product_name}' ürünü kalıcı olarak silinecek!\n\n"
                              f"Bu işlem geri alınamaz.\n"
                              f"Devam etmek istediğinizden emin misiniz?"):
            
            try:
                # Önce bu ürünle ilgili stok hareketlerini kontrol et
                movements = self.db.execute_query(
                    "SELECT COUNT(*) FROM stock_movements WHERE product_id = ?", 
                    (product_id,)
                )
                
                movement_count = movements[0][0] if movements else 0
                
                if movement_count > 0:
                    # Stok hareketi varsa kullanıcıya sor
                    if not messagebox.askyesno("Stok Hareketleri Mevcut", 
                                             f"Bu ürün için {movement_count} adet stok hareketi kaydı bulundu.\n\n"
                                             f"Ürün silinirse bu kayıtlar da silinecek.\n"
                                             f"Yine de devam etmek istiyor musunuz?"):
                        return
                    
                    # Önce stok hareketlerini sil
                    self.db.execute_query(
                        "DELETE FROM stock_movements WHERE product_id = ?", 
                        (product_id,)
                    )
                
                # Ürünü sil
                result = self.db.execute_query(
                    "DELETE FROM products WHERE id = ?", 
                    (product_id,)
                )
                
                if result > 0:
                    messagebox.showinfo("Başarılı", f"'{product_name}' ürünü başarıyla silindi!")
                    self.refresh_product_list()
                    # Diğer modüllerdeki ürün listelerini de yenile
                    self.refresh_other_modules()
                else:
                    messagebox.showerror("Hata", "Ürün silinemedi!")
                    
            except Exception as e:
                messagebox.showerror("Hata", f"Ürün silinirken hata oluştu:\n{str(e)}")
    
    def show_edit_dialog(self, product_id, product_data):
        """Ürün düzenleme dialog'u"""
        dialog = tk.Toplevel()
        dialog.title("Ürün Düzenle")
        dialog.geometry("400x500")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.product_tree.winfo_toplevel())
        dialog.grab_set()
        
        # Başlık
        title_label = tk.Label(dialog, text=f"Ürün Düzenle: {product_data[1]}", 
                              font=('Arial', 14, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Form frame
        form_frame = ttk.Frame(dialog)
        form_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Form alanları
        ttk.Label(form_frame, text="Ürün Adı:").grid(row=0, column=0, sticky='w', pady=5)
        name_entry = ttk.Entry(form_frame, width=30)
        name_entry.insert(0, product_data[1])
        name_entry.grid(row=0, column=1, pady=5, sticky='ew')
        
        ttk.Label(form_frame, text="Barkod:").grid(row=1, column=0, sticky='w', pady=5)
        barcode_entry = ttk.Entry(form_frame, width=30)
        barcode_entry.insert(0, product_data[2])
        barcode_entry.grid(row=1, column=1, pady=5, sticky='ew')
        
        ttk.Label(form_frame, text="Kategori:").grid(row=2, column=0, sticky='w', pady=5)
        category_combo = ttk.Combobox(form_frame, width=27, state='readonly')
        categories = self.db.get_all_categories()
        category_list = [cat[1] for cat in categories]
        category_combo['values'] = category_list
        category_combo.set(product_data[3])
        category_combo.grid(row=2, column=1, pady=5, sticky='ew')
        
        ttk.Label(form_frame, text="Birim Fiyat:").grid(row=3, column=0, sticky='w', pady=5)
        price_entry = ttk.Entry(form_frame, width=30)
        price_entry.insert(0, str(product_data[4]))
        price_entry.grid(row=3, column=1, pady=5, sticky='ew')
        
        ttk.Label(form_frame, text="Min. Stok:").grid(row=4, column=0, sticky='w', pady=5)
        min_stock_entry = ttk.Entry(form_frame, width=30)
        min_stock_entry.insert(0, str(product_data[6]))
        min_stock_entry.grid(row=4, column=1, pady=5, sticky='ew')
        
        ttk.Label(form_frame, text="Açıklama:").grid(row=5, column=0, sticky='w', pady=5)
        description_text = tk.Text(form_frame, width=30, height=4)
        description_text.insert(1.0, product_data[7] if len(product_data) > 7 else "")
        description_text.grid(row=5, column=1, pady=5, sticky='ew')
        
        form_frame.columnconfigure(1, weight=1)
        
        # Butonlar
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def save_changes():
            try:
                name = name_entry.get().strip()
                barcode = barcode_entry.get().strip()
                category_text = category_combo.get()
                price = float(price_entry.get())
                min_stock = int(min_stock_entry.get())
                description = description_text.get(1.0, tk.END).strip()
                
                if not name or not barcode:
                    messagebox.showerror("Hata", "Ürün adı ve barkod zorunludur!")
                    return
                
                # Kategori ID'sini bul
                category_id = None
                for cat in categories:
                    if cat[1] == category_text:
                        category_id = cat[0]
                        break
                
                if not category_id:
                    messagebox.showerror("Hata", "Geçerli bir kategori seçin!")
                    return
                
                # Ürünü güncelle
                result = self.db.execute_query(
                    """UPDATE products 
                       SET name=?, barcode=?, category_id=?, unit_price=?, min_stock=?, description=?
                       WHERE id=?""",
                    (name, barcode, category_id, price, min_stock, description, product_id)
                )
                
                if result > 0:
                    messagebox.showinfo("Başarılı", "Ürün başarıyla güncellendi!")
                    self.refresh_product_list()
                    # Diğer modüllerdeki ürün listelerini de yenile
                    self.refresh_other_modules()
                    dialog.destroy()
                else:
                    messagebox.showerror("Hata", "Ürün güncellenemedi!")
                    
            except ValueError:
                messagebox.showerror("Hata", "Fiyat ve minimum stok sayısal değer olmalıdır!")
            except Exception as e:
                messagebox.showerror("Hata", f"Ürün güncellenirken hata oluştu:\n{str(e)}")
        
        ttk.Button(button_frame, text="Kaydet", command=save_changes).pack(side='left', padx=5)
        ttk.Button(button_frame, text="İptal", command=dialog.destroy).pack(side='left', padx=5)
    
    def refresh_other_modules(self):
        """Diğer modüllerdeki ürün listelerini yenile"""
        try:
            # Stok yönetimi modülündeki ürün listesini yenile
            if self.stock_manager and hasattr(self.stock_manager, 'load_products'):
                self.stock_manager.load_products()
            
            # Rapor modülündeki verileri yenile (gerekirse)
            if self.report_manager and hasattr(self.report_manager, 'refresh_data'):
                self.report_manager.refresh_data()
                
        except Exception as e:
            print(f"Diğer modüller yenilenirken hata: {e}")