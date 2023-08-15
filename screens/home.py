import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from config.config import get_config, load_or_create_config
from utils.pdf_utils import extract_names_from_pdf, split_pdf
from utils.sheet_utils import extract_column_by_header


def home(root, tab):
    load_or_create_config()
    config = get_config()

    def update_interface():
        if not name_mode_var.get():
            excel_label.grid()
            excel_file_entry.grid()
            excel_button.grid()
            excel_head.grid()
            excel_head_entry.grid()
        else:
            excel_label.grid_remove()
            excel_file_entry.grid_remove()
            excel_button.grid_remove()
            excel_head.grid_remove()
            excel_head_entry.grid_remove()
    font = ("Helvetica", 11)
    font_bold = ("Helvetica", 11, "bold")

    ttk.Label(tab, text="Selecione o arquivo PDF a ser dividido: *", font=font).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
    input_pdf_entry = ttk.Entry(tab, font=font)
    input_pdf_entry.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
    ttk.Button(tab, text="Selecionar Arquivo", width=20, bootstyle=(INFO, OUTLINE), command=lambda: input_pdf_entry.insert(0, filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])))\
        .grid(row=1, column=2, pady=(0, 10), padx=(5, 0))

    ttk.Label(tab, text="Selecione o diretório de destino para salvar as divisões: *", font=font).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
    output_directory_entry = ttk.Entry(tab, font=font)
    output_directory_entry.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
    ttk.Button(tab, text="Selecionar Pasta", width=20, bootstyle=(INFO, OUTLINE), command=lambda: output_directory_entry.insert(0, filedialog.askdirectory()))\
        .grid(row=3, column=2, pady=(0, 10), padx=(5, 0))

    ttk.Label(tab, text="Informe a quantidade de páginas por divisão: *", font=font).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
    pages_per_division_entry = ttk.Entry(tab, font=font)
    pages_per_division_entry.grid(row=5, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
    pages_per_division_entry.insert(0, "2")

    name_mode_var = tk.BooleanVar(value=True)
    name_mode_check = ttk.Checkbutton(tab, text="Automático", bootstyle="round-toggle", variable=name_mode_var, command=update_interface)
    name_mode_check.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
    

    excel_head = ttk.Label(tab, text="Insira o cabeçalho da coluna com os nomes:", font=font)
    excel_head.grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
    excel_head_entry = ttk.Entry(tab, font=font)
    excel_head_entry.insert(0, "Nomes")
    excel_head_entry.grid(row=8, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
    excel_label = ttk.Label(tab, text="Selecione o arquivo de planilha com os nomes dos certificados (.xlsx, .ods):", font=font)
    excel_label.grid(row=9, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
    excel_file_entry = ttk.Entry(tab, font=font)
    excel_file_entry.grid(row=10, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
    excel_button = ttk.Button(tab, text="Selecionar Arquivo", width=20, bootstyle=(INFO, OUTLINE), command=lambda: excel_file_entry.insert(0, filedialog.askopenfilename(filetypes=[("Planilhas Excel", "*.xlsx"), ("OpenDocument Spreadsheet", "*.ods")])))
    excel_button.grid(row=10, column=2, pady=(0, 10), padx=(5, 0))

    progress_bar = ttk.Progressbar(tab, bootstyle="striped", length=200, mode='determinate', maximum=100)
    label_var = tk.StringVar(value="Barra de progresso")
    label = tk.Label(tab, textvariable=label_var)
    update_interface()

    def divide_pdfs():
        
        input_pdf_path = input_pdf_entry.get()
        output_directory = output_directory_entry.get()
        pages_per_division = int(pages_per_division_entry.get())
        excel_file = excel_file_entry.get()
        
        names = []
        pastas = []
        progress_bar.grid(row=11, column=0, columnspan=1, pady=(0, 20), padx=(0, 0))
        label.grid(row=11, column=1, columnspan=2, pady=(0, 20), padx=(0, 0))
        if name_mode_var.get():
            if input_pdf_path != '':
                label_var.set('Localizando Nomes para Arquivos e Pastas.')
                label.update()
                names, pastas = extract_names_from_pdf(input_pdf_path, config['certificate_name'], config['certificate_registration'], pages_per_division, progress_bar)
            else:
                messagebox.showerror("Erro", "Informe o arquivo .pdf!")
        else:
            if excel_file == '':
                messagebox.showerror("Erro", "Informe um arquivo xlsx com nomes para os arquivos!")
                return
            else:
                names = extract_column_by_header(excel_file, excel_head_entry.get())

        if len(names) > 0:
            label_var.set('Separando Cada Certificado do PDF em Arquivos Individuais.')
            label.update()
            split_pdf(input_pdf_path, output_directory, names, pastas, pages_per_division, progress_bar)

    ttk.Button(tab, text="Dividir PDFs", command=divide_pdfs, width=15).grid(row=12, column=0, padx=10)
    ttk.Button(tab, text="Sair", command=root.quit, width=15, bootstyle="danger").grid(row=12, column=1, padx=10)
