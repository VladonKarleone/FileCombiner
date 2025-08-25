import os
import sys
import tkinter as tk
from gui.app import FileCombinerApp
from core.file_processor import process_directory, process_files_list
from core.error_parser import extract_project_files_from_error

def main():
    # Если передан аргумент командной строки, используем соответствующий режим
    if len(sys.argv) > 1:
        if sys.argv[1] == "--error" and len(sys.argv) > 3:
            # Режим обработки ошибки из командной строки
            error_file = sys.argv[2]
            project_root = sys.argv[3]
            output_file = sys.argv[4] if len(sys.argv) > 4 else "combined_files.txt"
            
            try:
                # Читаем файл с ошибкой
                with open(error_file, 'r', encoding='utf-8') as f:
                    error_text = f.read()
                
                # Извлекаем пути к файлам
                project_files = extract_project_files_from_error(error_text, project_root)
                
                if not project_files:
                    print("Не найдено файлов проекта в тексте ошибки")
                    return
                
                # Сохраняем файлы
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    process_files_list(project_files, outfile, project_root)
                
                print(f"Результат сохранён в файл: {output_file}")
                
            except Exception as e:
                print(f"Ошибка: {str(e)}")
        
        elif os.path.isdir(sys.argv[1]):
            # Старый режим обработки папки  
            output_file = "combined_files.txt"
            
            with open(output_file, 'w', encoding='utf-8') as outfile:
                process_directory(sys.argv[1], outfile, ['.py', '.json'])
            
            print(f"Результат сохранён в файл: {output_file}")
        else:
            print(f"Ошибка: '{sys.argv[1]}' не является папкой или не существует.")
            sys.exit(1)
    else:
        # Запускаем графический интерфейс
        root = tk.Tk()
        app = FileCombinerApp(root)
        root.mainloop()

if __name__ == "__main__":
    main()