import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from config.config import get_config, load_config, restore_config_default, save_config_to_json

config_itens = get_config()
def create_widgets(tab):
    font = ("Helvetica", 12)
    font_bold = ("Helvetica", 11, "bold")

    ttk.Label(tab, text="Prefixo para buscar o nome do arquivo:", font=font).grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
    name_entry = ttk.Entry(tab, width=65, font=font)
    name_entry.insert(0, config_itens["certificate_name"])
    name_entry.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E, pady=(0, 10))
    
    ttk.Label(tab, text="Prefixo para localizar o registro (os resultados após este prefixo são utilizados nos nomes das pastas):", font=font).grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
    registration_entry = ttk.Entry(tab, width=65, font=font)
    registration_entry.insert(0, config_itens["certificate_registration"])
    registration_entry.grid(row=4, column=0, columnspan=3, sticky=tk.W+tk.E, pady=(0, 10))
    
    ttk.Label(tab, text="Nome da pasta a ser salva, quando o modo automático estiver desativado:", font=font).grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
    folder_entry = ttk.Entry(tab, width=65, font=font)
    folder_entry.insert(0, config_itens["default_folder_name"])
    folder_entry.grid(row=6, column=0, columnspan=3, sticky=tk.W+tk.E, pady=(0, 10))
    
    def update_inputs():
        load_config()
        config = get_config()
        folder_entry.delete(0, "end")
        folder_entry.insert(0, config["certificate_name"])
        folder_entry.update()
        name_entry.delete(0, "end")
        name_entry.insert(0, config["certificate_name"])
        name_entry.update()
        folder_entry.delete(0, "end")
        folder_entry.insert(0, config["default_folder_name"])
        folder_entry.update()

    def new_config_save():
        new_config = {
            "default_folder_name": folder_entry.get(),
            "certificate_name": name_entry.get(),
            "certificate_registration": registration_entry.get(),
        }
        save_config_to_json(new_config)
        update_inputs()
        
    def restore_config():
        restore_config_default()
        update_inputs()

    save_button = ttk.Button(tab, text="Salvar Configuração", command=new_config_save, style="primary.TButton", cursor="hand2")
    save_button.grid(row=7, column=0, columnspan=1, sticky=tk.W+tk.E, pady=(0, 10))
    
    restore_button = ttk.Button(tab, text="Restaurar Padrões", command=restore_config, style="secondary.TButton", cursor="hand2")
    restore_button.grid(row=7, column=2, columnspan=1, sticky=tk.W+tk.E, pady=(0, 10))
