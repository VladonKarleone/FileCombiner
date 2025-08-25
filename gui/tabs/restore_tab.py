import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from gui.widgets import create_labeled_entry, create_scrolled_text
from core.file_processor import restore_files
from utils.helpers import ensure_directory_exists

class RestoreTab(ttk.Frame):
    def __init__(self, parent, log_message_callback):
        super().__init__(parent)
        self.log_message = log_message_callback
        
        # Переменные для восстановления
        self.combined_file_path = tk.StringVar()
        self.restore_target_folder = tk.StringVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Фрейм для выбора файла
        file_frame = create_labeled_entry(
            self, "Объединенный файл:", self.combined_file_path, self.browse_combined_file
        )
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Фрейм для выбора папки назначения
        target_frame = create_labeled_entry(
            self, "Папка назначения:", self.restore_target_folder, self.browse_restore_folder
        )
        target_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Кнопка восстановления
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Восстановить файлы", command=self.restore_files).pack(pady=10)
        
        # Прогресс бар
        self.progress = ttk.Progressbar(self, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)
        
        # Текстовое поле для лога
        log_frame = ttk.LabelFrame(self, text="Лог", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        log_inner_frame, self.log_widget = create_scrolled_text(log_frame, height=10)
        log_inner_frame.pack(fill=tk.BOTH, expand=True)
    
    def browse_combined_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.combined_file_path.set(file_path)
    
    def browse_restore_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.restore_target_folder.set(folder)
    
    def restore_files(self):
        combined_file = self.combined_file_path.get()
        target_folder = self.restore_target_folder.get()
        
        if not combined_file or not os.path.isfile(combined_file):
            messagebox.showerror("Ошибка", "Выберите корректный объединенный файл")
            return
        
        if not target_folder:
            messagebox.showerror("Ошибка", "Выберите папку назначения")
            return
        
        # Создаем папку назначения, если её нет
        ensure_directory_exists(target_folder)
        
        self.progress.start()
        self.log_message("Начало восстановления...")
        
        try:
            success, message = restore_files(combined_file, target_folder)
            if success:
                self.log_message(message)
                messagebox.showinfo("Готово", message)
            else:
                self.log_message(message)
                messagebox.showerror("Ошибка", message)
                
        except Exception as e:
            error_msg = f"Ошибка при восстановлении: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Ошибка", error_msg)
        finally:
            self.progress.stop()