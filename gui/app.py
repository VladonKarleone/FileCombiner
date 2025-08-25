import tkinter as tk
from tkinter import ttk
from gui.tabs.combine_tab import CombineTab
from gui.tabs.restore_tab import RestoreTab
from gui.tabs.error_tab import ErrorTab

class FileCombinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Объединитель и восстановитель файлов")
        self.root.geometry("700x600")
        
        # Создаем Notebook (вкладки)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Создаем вкладки
        self.combine_tab = CombineTab(self.notebook, self.log_combine)
        self.restore_tab = RestoreTab(self.notebook, self.log_restore)
        self.error_tab = ErrorTab(self.notebook, self.log_error)
        
        self.notebook.add(self.combine_tab, text="Объединение")
        self.notebook.add(self.restore_tab, text="Восстановление")
        self.notebook.add(self.error_tab, text="По ошибке")
    
    def log_combine(self, message):
        self.combine_tab.log_widget.insert(tk.END, message + "\n")
        self.combine_tab.log_widget.see(tk.END)
        self.root.update_idletasks()
    
    def log_restore(self, message):
        self.restore_tab.log_widget.insert(tk.END, message + "\n")
        self.restore_tab.log_widget.see(tk.END)
        self.root.update_idletasks()
    
    def log_error(self, message):
        self.error_tab.log_widget.insert(tk.END, message + "\n")
        self.error_tab.log_widget.see(tk.END)
        self.root.update_idletasks()