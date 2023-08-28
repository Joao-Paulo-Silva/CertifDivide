import os
import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import webbrowser
def code_fonte():
    url = "https://github.com/Joao-Paulo-Silva/CertifDivide"
    webbrowser.open(url)

def create_tutorial(tab):
    # Criar um rótulo como título
    title_label = ttk.Label(tab, text="Conheça Mais Sobre o Aplicativo", font=("Helvetica", 16, "bold"), anchor="center", justify="center")
    title_label.grid(row=1, sticky=tk.W+tk.E, pady=(0, 10), padx=10)

    tutorial_content = """
        Este aplicativo oferece a funcionalidade de dividir certificados e declarações \
        em seções específicas, considerando o número de páginas de cada seção. Ele \
        disponibiliza duas abordagens distintas para a identificação de nomes de arquivos.
        O primeiro método é automatizado, localizando os nomes após um prefixo predefinido \
        para certificados e usando prefixo e sufixo para declarações. O segundo método envolve \
        a utilização de uma planilha que lista os nomes em ordem, correspondendo à sequência do \
        PDF que será dividido.
        Para mais detalhes, consulte o guia fornecido abaixo ou verifique o código-fonte da aplicação.
        """

    text = tk.Text(tab, wrap=tk.WORD, font=("Helvetica", 12))
    text.insert(tk.END, tutorial_content)
    text.grid(row=2, pady=10, padx=10, sticky=tk.W+tk.E)
    text.configure(borderwidth=0, highlightthickness=0, height=10, width=90, state="disabled")
    def open_tutorial():
        pdf_path = "CertifDivide.pdf"
        if os.path.exists(pdf_path):
            webbrowser.open(pdf_path)
        else:
            messagebox.showerror("Erro", "Arquivo não encontrado:")
            print("Arquivo não encontrado:", pdf_path)

    codigo_fonte = ttk.Button(tab, text="Abrir Código-fonte", width=50, command=code_fonte, bootstyle=(INFO, OUTLINE), cursor="hand2")
    codigo_fonte.grid(row=12, columnspan=1, sticky=tk.W, pady=(25, 0), padx=(20, 0))
    tutorial = ttk.Button(tab, text="Abrir Guia de Usuário!", width=50, command=open_tutorial, bootstyle=(DARK, OUTLINE), cursor="hand2")
    tutorial.grid(row=12, columnspan=3, sticky=tk.W, pady=(25, 0), padx=(500, 0))