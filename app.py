import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from screens.tutorial import create_tutorial
from screens.ui_config import create_widgets
from screens.home import home
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Ferramenta de Divisão de Certificados (pdf)')
    root.iconbitmap('icon.ico')
    root.resizable(False, False)

    frame = ttk.Frame(root, padding="10")
    frame.grid(column=2, row=14, sticky=(tk.N, tk.W, tk.E, tk.S))
    # Criar o notebook (guias)
    notebook = ttk.Notebook(root, bootstyle="dark", padding="0 10 0 0")
    notebook.grid(column=2, row=14, sticky=(tk.N, tk.W, tk.E, tk.S))
    # Criar as guias (tabs)
    tab1 = ttk.Frame(notebook, padding="15")
    tab2 = ttk.Frame(notebook, padding="15")
    tab3 = ttk.Frame(notebook, padding="15")
    home(root, tab1)
    create_widgets(tab2)
    create_tutorial(tab3)
    notebook.add(tab1, text="Inicio")
    notebook.add(tab2, text="Configurações")
    notebook.add(tab3, text="Sobre")

    root.mainloop()
