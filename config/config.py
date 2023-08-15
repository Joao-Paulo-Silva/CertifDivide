import os
import json
from tkinter import messagebox


default_config = {
    "default_folder_name": "certificados",
    "certificate_name": 'Nome:',
    "certificate_registration": 'Registro:',
}

config_file_name = "config.json"

# Caminho para a pasta onde o arquivo JSON deve ser criado
config_folder = "./"

# Verifica se o arquivo JSON já existe
config_path = os.path.join(config_folder, config_file_name)

def load_or_create_config():
    if not os.path.exists(config_path):
        # Se não existir, cria o arquivo e salva as configurações padrão nele
        with open(config_path, "w") as config_file:
            json.dump(default_config, config_file, indent=4)
        return default_config
    else:
        # Se existir, verifica se o arquivo está vazio
        if os.path.getsize(config_path) == 0:
            # Se estiver vazio, salva as configurações padrão no arquivo
            with open(config_path, "w") as config_file:
                json.dump(default_config, config_file, indent=4)
            return default_config
        else:
            # Se não estiver vazio, carrega as configurações do arquivo JSON
            with open(config_path, "r") as config_file:
                loaded_config = json.load(config_file)
            return loaded_config
        
loaded_config = load_or_create_config()

def load_config():
    global loaded_config
    loaded_config = load_or_create_config()

def get_config():
    return loaded_config

def save_config_to_json(config_dict):
    with open(config_path, 'w') as json_file:
        json.dump(config_dict, json_file, indent=4)
        messagebox.showinfo("Concluído", "Configurações salvas com sucesso!")

def restore_config_default():
    save_config_to_json(default_config)