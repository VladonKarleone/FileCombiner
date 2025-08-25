import os
from .constants import SEPARATOR

def process_directory(folder_path, outfile, extensions, base_path=None):
    """
    Рекурсивно обрабатывает все файлы в указанной папке и её подпапках
    с учетом выбранных расширений файлов
    """
    if base_path is None:
        base_path = folder_path
    
    for item in sorted(os.listdir(folder_path)):
        item_path = os.path.join(folder_path, item)
        
        # Пропускаем файлы __init__.py
        if item == "__init__.py":
            continue
            
        # Если это папка - рекурсивно обрабатываем её
        if os.path.isdir(item_path):
            process_directory(item_path, outfile, extensions, base_path)
        # Если это файл - проверяем его расширение
        elif os.path.isfile(item_path) and any(item.endswith(ext) for ext in extensions):
            try:
                # Получаем относительный путь для отображения
                relative_path = os.path.relpath(item_path, base_path)
                
                with open(item_path, 'r', encoding='utf-8') as infile:
                    content = infile.read().strip()
                
                # Записываем информацию о файле и его содержимое
                outfile.write(f"{relative_path}:\n{content}\n")
                outfile.write(SEPARATOR)
                
            except UnicodeDecodeError:
                print(f"Пропуск файла {item_path}: не текстовый формат")
            except PermissionError:
                print(f"Нет доступа к файлу: {item_path}")
            except Exception as e:
                print(f"Ошибка при обработке файла {item_path}: {str(e)}")

def restore_files(combined_file_path, target_folder):
    """Восстанавливает файлы из объединенного файла в целевую папку"""
    try:
        with open(combined_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Разделяем содержимое на секции файлов
        sections = content.split(SEPARATOR)
        
        for section in sections:
            if not section.strip():
                continue
                
            # Извлекаем путь файла и содержимое
            if ":\n" in section:
                file_path, file_content = section.split(":\n", 1)
                full_path = os.path.join(target_folder, file_path)
                
                # Создаем необходимые директории
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                # Записываем содержимое файла
                with open(full_path, 'w', encoding='utf-8') as out_file:
                    out_file.write(file_content.strip())
        
        return True, "Файлы успешно восстановлены!"
    except Exception as e:
        return False, f"Ошибка при восстановлении: {str(e)}"

def process_files_list(file_paths, outfile, base_path):
    """Обрабатывает список файлов и записывает их содержимое в outfile"""
    for file_path in file_paths:
        try:
            # Получаем относительный путь для отображения
            relative_path = os.path.relpath(file_path, base_path)
            
            with open(file_path, 'r', encoding='utf-8') as infile:
                content = infile.read().strip()
            
            # Записываем информацию о файле и его содержимое
            outfile.write(f"{relative_path}:\n{content}\n")
            outfile.write(SEPARATOR)
            
        except UnicodeDecodeError:
            print(f"Пропуск файла {file_path}: не текстовый формат")
        except PermissionError:
            print(f"Нет доступа к файлу: {file_path}")
        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {str(e)}")