import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os", "json", "ttkbootstrap", 'tkinter','openpyxl', 'ezodf', 'PyPDF2'], "includes": ["ttkbootstrap", 'tkinter','openpyxl', 'ezodf', 'PyPDF2'], "include_files": ["icon.ico", "tutorial.pdf"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Divisor de Certificados",
    version="0.1",
    description="Ferramenta de Divisão de Certificados (pdf)",
    options={"build_exe": build_exe_options},
    executables=[Executable("app.py", base=base, icon='icon.ico')]
)