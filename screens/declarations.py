import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from config.config import get_config, load_or_create_config
from utils.format_input import validate_input
from utils.pdf_utils import extract_names_from_pdf, split_pdf
from utils.sheet_utils import extract_column_by_header


def declarations(root, tab):
    # Carregamento das configurações armazenadas e configuração dos inputs.
    load_or_create_config()
    config = get_config()
    validation = tab.register(validate_input)
    font = ("Helvetica", 12)

    # Função aninhada que realiza a atualização dos inputs, levando em 
    # consideração a opção de escolher nomes automáticos ou não."
    def update_interface():
        if not name_mode_var.get():
            excel_label.grid()
            excel_file_entry.grid()
            excel_button.grid()
            excel_head.grid()
            excel_head_entry.grid()
            prefix_entry.grid_remove()
            sufix_entry.grid_remove()
            prefix_label.grid_remove()
            sufix_label.grid_remove()
            pages_search_entry.grid_remove()
            label_page_search.grid_remove()
        else:
            excel_label.grid_remove()
            excel_file_entry.grid_remove()
            excel_button.grid_remove()
            excel_head.grid_remove()
            excel_head_entry.grid_remove()
            prefix_entry.grid()
            sufix_entry.grid()
            prefix_label.grid()
            sufix_label.grid()
            pages_search_entry.grid()
            label_page_search.grid()

    # Função aninhada chamada ao clicar no botão dividir pdf. 
    def divide_pdfs():
        names = []
        pastas = []
        # Pega os valores dos inputs.
        input_pdf_path = input_pdf_entry.get()
        output_directory = output_directory_entry.get()
        pages_per_division = int(pages_per_division_entry.get())
        pages_search = int(pages_search_entry.get())
        excel_file = excel_file_entry.get()
        prefix = prefix_entry.get()
        suffix = sufix_entry.get()
       
        # Deixa a barra de progresso visível.
        if prefix != '' or suffix != '':
            progress_bar.grid(row=11, column=0, columnspan=1, pady=(0, 20), padx=(0, 0))
            label.grid(row=11, column=1, columnspan=2, pady=(0, 20), padx=(0, 0))
        
        # Se o modo automático ativado.
        if name_mode_var.get():
            if input_pdf_path != '':
                label_var.set('Localizando Nomes para Arquivos e Pastas.')
                label.update()
                if prefix == '' or suffix == '':
                    messagebox.showerror("Erro", "O prefixo ou sufixo, não pode ficar vazio!")
                else:
                    names, pastas = extract_names_from_pdf(input_pdf_path, prefix, config['certificate_registration'], pages_search, progress_bar, past_mode_var.get(), suffix)
            else:
                messagebox.showerror("Erro", "Informe o arquivo .pdf!")
        else:
            if excel_file == '':
                messagebox.showerror("Erro", "Informe um arquivo xlsx com nomes para os arquivos!")
                return
            else:
                names = extract_column_by_header(excel_file, excel_head_entry.get())

        # Se conter nomes na lista iniciar a separação dos pdf's.
        if len(names) > 0:
            label_var.set('Separando Cada Certificado do PDF em Arquivos Individuais.')
            label.update()
            split_pdf(input_pdf_path, output_directory, names, pastas, pages_per_division, progress_bar)
            progress_bar.grid_remove()
            label.grid_remove()
            input_pdf_entry.delete(0, tk.END)
            output_directory_entry.delete(0, tk.END)
            excel_file_entry.delete(0, tk.END)
            prefix_entry.delete(0, tk.END)
            sufix_entry.delete(0, tk.END)
            update_interface()

    # ------------------------------------ INTERFACE ------------------------------------ #
    # Container que incorpora o campo de entrada para selecionar o arquivo PDF que será dividido.
    ttk.Label(tab, text="Selecione o arquivo PDF a ser dividido: *", font=font).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
    input_pdf_entry = ttk.Entry(tab, font=font)
    input_pdf_entry.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
    ttk.Button(tab, text="Selecionar Arquivo", width=20, cursor="hand2", bootstyle=(INFO, OUTLINE), command=lambda: input_pdf_entry.insert(0, filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])))\
        .grid(row=1, column=2, pady=(0, 10), padx=(5, 0))

    # Container que incorpora o campo para inserir a pasta destino das divisões.
    ttk.Label(tab, text="Selecione o diretório de destino para salvar as divisões: *", font=font).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
    output_directory_entry = ttk.Entry(tab, font=font)
    output_directory_entry.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
    ttk.Button(tab, text="Selecionar Pasta", width=20, cursor="hand2", bootstyle=(INFO, OUTLINE), command=lambda: output_directory_entry.insert(0, filedialog.askdirectory()))\
        .grid(row=3, column=2, pady=(0, 10), padx=(5, 0))

    # Container que incorpora o campo que insere a quantidade de paginas por divisão.
    ttk.Label(tab, text="Informe a quantidade de páginas por divisão: *", font=font).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
    pages_per_division_entry = ttk.Entry(tab, font=font, width=37, validate="key", validatecommand=(validation, "%P"))
    pages_per_division_entry.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
    pages_per_division_entry.insert(0, "1")

    # conteiner que incorpora o campo no qual informa em qual pagina busca o nome automaticamente.
    label_page_search = ttk.Label(tab, text="Página de Referência para Busca de Nomes: *", font=font)
    label_page_search.grid(row=4, column=1, sticky=tk.W, pady=(0, 5))
    pages_search_entry = ttk.Entry(tab, font=font, width=37, validate="key", validatecommand=(validation, "%P"))
    pages_search_entry.grid(row=5, column=1, columnspan=1, sticky=tk.W, pady=(0, 10))
    pages_search_entry.insert(0, "1")
    
    # Checkbox para verificar se gerará pastas de acordo com o registro das partes.
    past_mode_var = tk.BooleanVar(value=True)
    past_mode_check = ttk.Checkbutton(tab, text="Gerar Pastas", cursor="hand2", bootstyle="round-toggle", variable=past_mode_var, command=update_interface)
    past_mode_check.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

    # Checkbox para verificar se gerará pastas de acordo com o registro das partes.
    name_mode_var = tk.BooleanVar(value=True)
    name_mode_check = ttk.Checkbutton(tab, text="Nomes Automáticos", cursor="hand2", bootstyle="round-toggle", variable=name_mode_var, command=update_interface)
    name_mode_check.grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=(5, 10))
    
    # Campos para informar o prefixo e sufixo.
    prefix_label = ttk.Label(tab,text="Prefixo: *", font=("Helvetica", 10), width=15)
    prefix_label.grid(row=6, column=0, columnspan=1, padx=(120,0))
    prefix_entry = ttk.Entry(tab, font=font, width=15)
    prefix_entry.grid(row=7, column=0, columnspan=1, padx=(120,0))
    sufix_label = ttk.Label(tab,text="Sufixo: *", font=("Helvetica", 10), width=15)
    sufix_label.grid(row=6, column=0, columnspan=2, padx=(200,0))
    sufix_entry = ttk.Entry(tab, font=font, width=15)
    sufix_entry.grid(row=7, column=0, columnspan=2, padx=(200,0))
    
    # Campos para informar a tabela com os nomes do arquivo.
    excel_head = ttk.Label(tab, text="Insira o cabeçalho da coluna com os nomes:", font=font)
    excel_head.grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
    excel_head_entry = ttk.Entry(tab, font=font)
    excel_head_entry.insert(0, "Nomes")
    excel_head_entry.grid(row=9, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
    excel_label = ttk.Label(tab, text="Selecione o arquivo de planilha com os nomes dos certificados (.xlsx, .ods):", font=font)
    excel_label.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
    excel_file_entry = ttk.Entry(tab, font=font)
    excel_file_entry.grid(row=11, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
    excel_button = ttk.Button(tab, text="Selecionar Arquivo", cursor="hand2", width=20, bootstyle=(INFO, OUTLINE), command=lambda: excel_file_entry.insert(0, filedialog.askopenfilename(filetypes=[("Planilhas Excel", "*.xlsx"), ("OpenDocument Spreadsheet", "*.ods")])))
    excel_button.grid(row=11, column=2, pady=(0, 10), padx=(5, 0))

    # Barra de progresso.
    progress_bar = ttk.Progressbar(tab, bootstyle="striped", length=300, mode='determinate', maximum=100)
    label_var = tk.StringVar(value="Barra de progresso")
    label = tk.Label(tab, textvariable=label_var)

    # Botão para dividir os pdf e sair.
    ttk.Button(tab, text="Dividir PDFs", command=divide_pdfs, cursor="hand2", width=30).grid(row=12, column=0, padx=5, pady=10)
    ttk.Button(tab, text="Sair", command=root.quit, width=30, cursor="hand2", bootstyle="danger").grid(row=12, column=1, padx=5, pady=10)
    # Atualiza a interface ao iniciar a aplicação.
    update_interface()