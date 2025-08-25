import tkinter as tk
from tkinter import ttk

def create_scrolled_text(parent, height=10):
    """Создает текстовое поле с полосой прокрутки"""
    frame = ttk.Frame(parent)
    text_widget = tk.Text(frame, height=height, wrap=tk.WORD)
    scrollbar = ttk.Scrollbar(frame, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    return frame, text_widget

def create_labeled_entry(parent, label_text, text_variable, browse_command=None, width=50):
    """Создает метку, поле ввода и кнопку обзора"""
    frame = ttk.Frame(parent)
    ttk.Label(frame, text=label_text).grid(row=0, column=0, sticky=tk.W)
    entry = ttk.Entry(frame, textvariable=text_variable, width=width)
    entry.grid(row=0, column=1, padx=5)
    
    if browse_command:
        ttk.Button(frame, text="Обзор", command=browse_command).grid(row=0, column=2)
    
    return frame