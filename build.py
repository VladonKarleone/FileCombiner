import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--name=FileCombiner',
    '--add-data=core;core',
    '--add-data=gui;gui',
    '--add-data=utils;utils',
    '--hidden-import=tkinter',
    '--hidden-import=os',
    '--hidden-import=re',
    '--hidden-import=json',
    '--hidden-import=datetime'
])