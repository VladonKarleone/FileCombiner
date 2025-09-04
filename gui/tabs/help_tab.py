import tkinter as tk
from tkinter import ttk
from gui.widgets import create_scrolled_text

class HelpTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
    
    def create_widgets(self):
        # Создаем текстовое поле с прокруткой
        help_frame, self.help_text = create_scrolled_text(self, height=25)
        help_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Добавляем текст справки
        help_content = """
        ФАЙЛОВЫЙ КОМБАЙНЕР - СПРАВКА

        ОПИСАНИЕ ПРИЛОЖЕНИЯ:
        Это приложение позволяет объединять текстовые файлы проекта в один файл
        и восстанавливать их обратно из объединенного файла.

        ВКЛАДКА "ОБЪЕДИНЕНИЕ":
        - Выберите папку с файлами проекта
        - Отметьте типы файлов для обработки (или укажите свои через запятую)
        - Нажмите "Объединить файлы" и выберите место сохранения

        ВКЛАДКА "ВОССТАНОВЛЕНИЕ":
        - Выберите объединенный файл
        - Укажите папку для восстановления файлов
        - Нажмите "Восстановить файлы"

        ВКЛАДКА "ПО ОШИБКЕ":
        - Вставьте текст ошибки Python или загрузите из файла
        - Укажите корневую папку проекта
        - Нажмите "Извлечь и объединить файлы"
        Приложение автоматически найдет файлы проекта, упомянутые в ошибке,
        и создаст объединенный файл с их содержимым.

        АВТОРЫ:
        Идея: Vladon Karleone
        Разработка: DeepSeek AI v3.0
        Тестирование: Vladon Karleone

        ВЕРСИЯ: 2.0
        """
        
        self.help_text.insert(1.0, help_content)
        self.help_text.config(state=tk.DISABLED)  # Делаем текст только для чтения