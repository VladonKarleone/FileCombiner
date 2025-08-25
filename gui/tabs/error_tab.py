import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from gui.widgets import create_labeled_entry, create_scrolled_text
from core.error_parser import extract_project_files_from_error
from core.constants import SEPARATOR

class ErrorTab(ttk.Frame):
    def __init__(self, parent, log_message_callback):
        super().__init__(parent)
        self.log_message = log_message_callback
        
        self.project_root = tk.StringVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Фрейм для ввода текста ошибки
        error_frame = ttk.LabelFrame(self, text="Текст ошибки", padding="10")
        error_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Кнопка загрузки файла с ошибкой
        load_button_frame = ttk.Frame(error_frame)
        load_button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(load_button_frame, text="Загрузить из файла", 
                  command=self.load_error_from_file).pack(side=tk.RIGHT)
        
        # Текстовое поле для ошибки
        error_inner_frame, self.error_text_widget = create_scrolled_text(error_frame, height=10)
        error_inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Фрейм для выбора корневой папки проекта
        root_frame = create_labeled_entry(
            self, "Корневая папка проекта:", self.project_root, self.browse_project_root
        )
        root_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Кнопка обработки
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Извлечь и объединить файлы", 
                  command=self.process_error).pack(pady=10)
        
        # Прогресс бар
        self.progress = ttk.Progressbar(self, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)
        
        # Текстовое поле для лога
        log_frame = ttk.LabelFrame(self, text="Лог", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        log_inner_frame, self.log_widget = create_scrolled_text(log_frame, height=10)
        log_inner_frame.pack(fill=tk.BOTH, expand=True)
    
    def browse_project_root(self):
        folder = filedialog.askdirectory()
        if folder:
            self.project_root.set(folder)
    
    def load_error_from_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("Log files", "*.log"), ("All files", "*.*")]
        )
        if file_path:
            try:
                # Пытаемся прочитать файл с разными кодировками
                encodings = ['utf-8', 'cp1251', 'cp866']
                content = None
                
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            content = f.read()
                        break
                    except UnicodeDecodeError:
                        continue
                
                if content is None:
                    # Если ни одна кодировка не подошла, пробуем бинарный режим
                    with open(file_path, 'rb') as f:
                        content = f.read().decode('utf-8', errors='replace')
                
                self.error_text_widget.delete(1.0, tk.END)
                self.error_text_widget.insert(1.0, content)
                self.log_message(f"Загружен файл: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")
    
    def process_error(self):
        # Получаем текст ошибки из виджета
        error_text = self.error_text_widget.get(1.0, tk.END)
        
        if not error_text.strip():
            messagebox.showerror("Ошибка", "Введите текст ошибки")
            return
        
        project_root = self.project_root.get()
        if not project_root:
            messagebox.showerror("Ошибка", "Укажите корневую папку проекта")
            return
        
        self.progress.start()
        self.log_message("Анализ текста ошибки...")
        
        try:
            # Извлекаем пути к файлам из текста ошибки
            project_files = extract_project_files_from_error(error_text, project_root)
            
            if not project_files:
                self.log_message("Не найдено файлов проекта в тексте ошибки")
                messagebox.showinfo("Информация", "Не найдено файлов проекта в тексте ошибки")
                return
            
            self.log_message(f"Найдено файлов: {len(project_files)}")
            
            # Запрашиваем место сохранения
            output_file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if not output_file:
                return
            
            # Записываем найденные файлы
            with open(output_file, 'w', encoding='utf-8') as outfile:
                for file_path in project_files:
                    try:
                        # Получаем относительный путь
                        relative_path = os.path.relpath(file_path, project_root)
                        
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read().strip()
                        
                        # Записываем информацию о файле и его содержимое
                        outfile.write(f"{relative_path}:\n{content}\n")
                        outfile.write(SEPARATOR)
                        self.log_message(f"Обработан: {relative_path}")
                        
                    except UnicodeDecodeError:
                        self.log_message(f"Пропуск файла {file_path}: не текстовый формат")
                    except PermissionError:
                        self.log_message(f"Нет доступа к файлу: {file_path}")
                    except Exception as e:
                        self.log_message(f"Ошибка при обработке файла {file_path}: {str(e)}")
            
            self.log_message(f"Готово! Результат сохранён в: {output_file}")
            messagebox.showinfo("Готово", f"Файлы успешно объединены в: {output_file}")
            
        except Exception as e:
            self.log_message(f"Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        finally:
            self.progress.stop()