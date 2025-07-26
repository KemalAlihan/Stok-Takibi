import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from product_manager import ProductManager
from stock_manager import StockManager
from report_manager import ReportManager

class StockTrackingSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stok Takip Sistemi")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Veritabanı bağlantısı
        self.db = Database()
        
        # Manager sınıfları
        self.product_manager = ProductManager(self.db)
        self.stock_manager = StockManager(self.db)
        self.report_manager = ReportManager(self.db)
        
        # Manager'lar arası referansları kur
        self.product_manager.set_other_managers(self.stock_manager, self.report_manager)
        
        self.create_widgets()
        
    def create_widgets(self):
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="STOK TAKİP SİSTEMİ", 
                              font=('Arial', 24, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_product_tab()
        self.create_stock_tab()
        self.create_report_tab()
        
    def create_product_tab(self):
        # Ürün Yönetimi Tab'ı
        product_frame = ttk.Frame(self.notebook)
        self.notebook.add(product_frame, text="Ürün Yönetimi")
        self.product_manager.create_interface(product_frame)
        
    def create_stock_tab(self):
        # Stok İşlemleri Tab'ı
        stock_frame = ttk.Frame(self.notebook)
        self.notebook.add(stock_frame, text="Stok İşlemleri")
        self.stock_manager.create_interface(stock_frame)
        
    def create_report_tab(self):
        # Raporlar Tab'ı
        report_frame = ttk.Frame(self.notebook)
        self.notebook.add(report_frame, text="Raporlar")
        self.report_manager.create_interface(report_frame)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StockTrackingSystem()
    app.run()