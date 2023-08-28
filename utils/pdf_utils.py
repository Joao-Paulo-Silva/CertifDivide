from tkinter import messagebox
from PyPDF2 import PdfReader, PdfWriter
import os
from pathlib import Path
from config.config import get_config

# Função para buscar o nome no texto do pdf.
def extract_names_from_pdf(pdf_path: str, prefix: str, key: str, page_interval: int, progress_bar, past_names: bool = True, suffix: str = None):
    progress_bar['value'] = 0
    progress_bar.update()
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        extracted_names = []
        pasta = []
        pages_total = len(pdf_reader.pages)
        for page_number, page in enumerate(pdf_reader.pages, start=1):
            # Verifica apenas as páginas indicadas pelo intervalo
            if page_number % page_interval == 0:
                page_text = page.extract_text()
                index = page_text.find(prefix)
                if index != -1:
                    if suffix is None:
                        name = extract_text_until_newline(page_text, index + len(prefix))
                        extracted_names.append(name)
                    else:
                        extracted_text = extract_text_between_prefix_and_suffix(page_text, prefix, suffix)
                        if extracted_text is not None:
                            extracted_names.append(extracted_text.replace("\n", " "))
                    if past_names:
                        key_dict = extract_text_until_newline(page_text, page_text.find(key) + len(key))
                        pasta.append(key_dict.split('/')[0])
                    progress_bar['value'] = ((page_number + 1) * 100) // pages_total
                    progress_bar.update()

        return extracted_names, pasta

# Pega o texto do prefixo até a quebra de linha
def extract_text_until_newline(text: str, start_index: int):
    newline_index = text.find('\n', start_index)
    if newline_index != -1:
        return text[start_index:newline_index].strip()
    else:
        return text[start_index:].strip()

# Pega o texto entre um prefixo e sufixo 
def extract_text_between_prefix_and_suffix(text: str, prefix: str, suffix: str):
    start_index = text.find(prefix)
    if start_index == -1:
        return None
    start_index += len(prefix)
    
    end_index = text.find(suffix, start_index)
    if end_index == -1:
        return None
    
    return text[start_index:end_index].strip()

# Função para deixar os nomes únicos colocando um valor após
def add_unique_suffixes(lista: list):
    contador_nomes = {}
    lista_final = []
    for nome in lista:
        if nome in contador_nomes:
            contador_nomes[nome] += 1
            nome_modificado = f"{nome} ({contador_nomes[nome]})"
        else:
            contador_nomes[nome] = 0
            nome_modificado = nome

        lista_final.append(nome_modificado)

    return lista_final

# Função para dividir o pdf
def split_pdf(input_pdf, output_directory, names, pastas, pages_per_division, progress_bar):
    pdf_reader = PdfReader(input_pdf)
    total_pages = len(pdf_reader.pages)
    divisions = total_pages // pages_per_division
    progress_bar['value'] = 0
    progress_bar.update()

    if len(names) != divisions:
        messagebox.showerror("Erro", f"A quantidade de nomes na planilha deve ser igual ao número de divisões ({divisions})!")
        return
    else:
        if len(pastas) == 0 or len(pastas) > len(names):
            names = add_unique_suffixes(names)
    for i in range(0, total_pages, pages_per_division):
        pdf_writer = PdfWriter()
        for j in range(pages_per_division):
            index = i + j
            if index < total_pages:
                pdf_writer.add_page(pdf_reader.pages[index])
        output_pdf_path: str
        if len(pastas) > 0 or len(pastas) == len(names):
            for pasta in list(set(pastas)):
                nova_pasta = Path(output_directory + f"/{pasta}")
                if not nova_pasta.exists():
                    os.makedirs(nova_pasta)
            output_pdf_path = os.path.join(output_directory, f"{pastas.pop(0)}/{names.pop(0)}.pdf")
        else:
            pasta = get_config()["default_folder_name"]
            nova_pasta = Path(output_directory + f"/{pasta}")
            if not nova_pasta.exists():
                os.makedirs(nova_pasta)
            output_pdf_path = os.path.join(output_directory, f"{pasta}/{names.pop(0)}.pdf")
        with open(output_pdf_path, "wb") as output_file:
            pdf_writer.write(output_file)
        progress_bar['value'] = ((i + 1) * 100) // total_pages
        progress_bar.update()
    print(progress_bar['value'])
    if progress_bar['value'] >= 99:
        messagebox.showinfo("Concluído", "Divisão de PDFs concluída!")
