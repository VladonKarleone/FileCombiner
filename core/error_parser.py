import os
import re

def extract_project_files_from_error(error_text, project_root=None):
    """
    Извлекает пути к файлам проекта из текста ошибки
    Игнорирует системные пути и пути к библиотекам
    """
    # Улучшенное регулярное выражение для извлечения путей из трассировки стека
    # Оно ищет пути в формате "File "путь", line номер, in функция"
    path_pattern = r'File "([^"]+\.(py|json|txt|html|css|js))"'
    paths = re.findall(path_pattern, error_text)
    
    # Извлекаем только пути (первый элемент каждого кортежа)
    file_paths = [path[0] for path in paths]
    
    # Убираем дубликаты и сортируем
    unique_paths = sorted(set(file_paths))
    
    # Фильтруем пути: оставляем только те, которые находятся в проекте
    project_files = []
    for path in unique_paths:
        # Нормализуем путь (заменяем / на \ в Windows)
        normalized_path = os.path.normpath(path)
        
        # Игнорируем системные пути и пути к библиотекам
        if any(ignore in normalized_path for ignore in ['AppData', 'Lib\\site-packages', 'Python\\Python', 'lib\\python']):
            continue
        
        # Если указана корневая папка проекта, проверяем что файл в ней
        if project_root:
            normalized_project_root = os.path.normpath(project_root)
            # Преобразуем оба пути к абсолютным для сравнения
            abs_path = os.path.abspath(normalized_path)
            abs_project_root = os.path.abspath(normalized_project_root)
            
            if not abs_path.startswith(abs_project_root):
                continue
                
        if os.path.isfile(normalized_path):
            project_files.append(normalized_path)
        else:
            # Если файл не найден, попробуем найти его относительно корневой папки
            if project_root:
                relative_path = os.path.join(project_root, normalized_path)
                if os.path.isfile(relative_path):
                    project_files.append(relative_path)
    
    return project_files