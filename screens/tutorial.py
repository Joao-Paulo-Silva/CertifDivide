import os
import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import webbrowser

def create_tutorial(tab):
    # Criar um rótulo como título
    title_label = ttk.Label(tab, width=50,text="Conheça Mais Sobre o Aplicativo", font=("Helvetica", 16, "bold"), anchor="center", justify="center")
    title_label.grid(row=1, column=2, columnspan=5, sticky=tk.W+tk.E, pady=(0, 10), padx=10)

    # Criar um rótulo como parágrafo
    paragraph_label = ttk.Label(tab, width=80, font=("Helvetica", 11), text="Este aplicativo proporciona a capacidade de dividir certificados, considerando a quantidade de")
    paragraph_label.grid(row=2, column=2, columnspan=5, sticky=tk.W+tk.E, pady=(0, 0), padx=10)
    paragraph_label1 = ttk.Label(tab, width=80, font=("Helvetica", 11), text="páginas indicada. Ele oferece dois métodos distintos para identificar os nomes dos arquivos.")
    paragraph_label1.grid(row=3, column=2, columnspan=5, sticky=tk.W+tk.E, pady=(0, 0), padx=10)
    paragraph_label2 = ttk.Label(tab, width=80, font=("Helvetica", 11), text="O primeiro método é automatizado e localiza os nomes após um prefixo predefinido. O segundo ")
    paragraph_label2.grid(row=4, column=2, columnspan=5, sticky=tk.W+tk.E, pady=(0, 0), padx=10)
    paragraph_label3 = ttk.Label(tab, width=80, font=("Helvetica", 11), text="método envolve a utilização de uma planilha que contém os nomes dispostos em ordem,")
    paragraph_label3.grid(row=5, column=2, columnspan=5, sticky=tk.W+tk.E, pady=(0, 0), padx=10)
    paragraph_label4 = ttk.Label(tab, width=80, font=("Helvetica", 11), text="correspondendo ao PDF que será alvo das divisões.")
    paragraph_label4.grid(row=6, column=2, columnspan=5, sticky=tk.W+tk.E, pady=(0, 0), padx=10)
    
    def open_tutorial():
        pdf_path = "tutorial.pdf"
        if os.path.exists(pdf_path):
            webbrowser.open(pdf_path)
        else:
            messagebox.showerror("Erro", "Arquivo não encontrado:")
            print("Arquivo não encontrado:", pdf_path)
    save_button = ttk.Button(tab, text="Abrir Guia de Usuário!", command=open_tutorial, style="primary.TButton")
    save_button.grid(row=12, column=5, columnspan=2, sticky=tk.W+tk.E, pady=(25, 0), padx=(15, 0))