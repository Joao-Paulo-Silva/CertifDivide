import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from screens.declarations import declarations
from screens.tutorial import create_tutorial
from screens.ui_config import create_widgets
from screens.certificates import certificates

if __name__ == '__main__':
    # Configura a Janela
    root = tk.Tk()
    root.title('Ferramenta de Divisão de Certificados e Declarações (pdf)')
    root.iconbitmap('icon.ico')
    root.resizable(False, False)

    # Criar o notebook (guias)
    notebook = ttk.Notebook(root, bootstyle="dark", padding="0 10 0 0")
    notebook.grid(column=2, row=14, sticky=(tk.N, tk.W, tk.E, tk.S))
    # Criar as guias (tabs)
    tab1 = ttk.Frame(notebook, padding="15")
    tab2 = ttk.Frame(notebook, padding="15")
    tab3 = ttk.Frame(notebook, padding="15")
    tab4 = ttk.Frame(notebook, padding="15")
    # Inicial o conteúdo das guais (tabs)
    certificates(root, tab1)
    declarations(root, tab2)
    create_widgets(tab3)
    create_tutorial(tab4)

    # Adiciona as Guias ao Notebook
    notebook.add(tab1, text="Certificados")
    notebook.add(tab2, text="Declarações")
    notebook.add(tab3, text="Configurações")
    notebook.add(tab4, text="Sobre")
    
    # Loop do app.
    root.mainloop()
