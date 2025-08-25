import os

def ensure_directory_exists(path):
    """Создает директорию, если она не существует"""
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False