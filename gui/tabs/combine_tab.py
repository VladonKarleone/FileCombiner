import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from gui.widgets import create_labeled_entry, create_scrolled_text
from core.file_processor import process_directory
from core.constants import SUPPORTED_EXTENSIONS

class CombineTab(ttk.Frame):
    def __init__(self, parent, log_message_callback):
        super().__init__(parent)
        self.log_message = log_message_callback
        
        # Переменные для хранения выбора
        self.folder_path = tk.StringVar()
        self.extensions = {}
        for ext in SUPPORTED_EXTENSIONS:
            self.extensions[ext] = tk.BooleanVar(value=ext in ['.py', '.json'])
        self.custom_ext = tk.StringVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Фрейм для выбора папки
        folder_frame = create_labeled_entry(
            self, "Папка:", self.folder_path, self.browse_folder
        )
        folder_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Фрейм для выбора расширений файлов
        ext_frame = ttk.LabelFrame(self, text="Типы файлов", padding="10")
        ext_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Стандартные расширения
        row, col = 0, 0
        for ext, var in self.extensions.items():
            ttk.Checkbutton(ext_frame, text=ext, variable=var).grid(
                row=row, column=col, sticky=tk.W, padx=5, pady=2)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Поле для пользовательских расширений
        ttk.Label(ext_frame, text="Другие (через запятую):").grid(
            row=row+1, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        ttk.Entry(ext_frame, textvariable=self.custom_ext, width=50).grid(
            row=row+2, column=0, columnspan=3, sticky=tk.W+tk.E, pady=5)
        
        # Кнопка обработки
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Объединить файлы", command=self.process_files).pack(pady=10)
        
        # Прогресс бар
        self.progress = ttk.Progressbar(self, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)
        
        # Текстовое поле для лога
        log_frame = ttk.LabelFrame(self, text="Лог", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        log_inner_frame, self.log_widget = create_scrolled_text(log_frame, height=10)
        log_inner_frame.pack(fill=tk.BOTH, expand=True)
    
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
    
    def process_files(self):
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Ошибка", "Выберите корректную папку")
            return
        
        # Получаем выбранные расширения
        extensions = [ext for ext, var in self.extensions.items() if var.get()]
        
        # Добавляем пользовательские расширения
        custom_exts = [ext.strip() for ext in self.custom_ext.get().split(',') if ext.strip()]
        for ext in custom_exts:
            if not ext.startswith('.'):
                ext = '.' + ext
            if ext not in extensions:
                extensions.append(ext)
        
        if not extensions:
            messagebox.showerror("Ошибка", "Выберите хотя бы одно расширение файла")
            return
        
        output_file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not output_file:
            return
        
        self.progress.start()
        self.log_message("Начало обработки...")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as outfile:
                process_directory(folder, outfile, extensions)
            
            self.log_message(f"Готово! Результат сохранён в: {output_file}")
            messagebox.showinfo("Готово", f"Файлы успешно объединены в: {output_file}")
            
        except Exception as e:
            self.log_message(f"Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        finally:
            self.progress.stop()