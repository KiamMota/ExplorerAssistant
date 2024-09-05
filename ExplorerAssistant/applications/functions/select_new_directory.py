import tkinter as tk
from tkinter import filedialog
import os

def create_new_directory():
    # Criar uma instância de Tkinter para o diálogo
    temp_root = tk.Tk()
    temp_root.withdraw()  # Esconder a janela principal

    # Solicitar o caminho do diretório onde o novo diretório será criado
    folder_path = filedialog.askdirectory(title="Selecione a Pasta", parent=temp_root)

    if folder_path:
        # Definir o nome do novo diretório
        new_dir_name = "NewDirectory"
        new_dir_path = os.path.join(folder_path, new_dir_name)
        try:
            # Verificar se o diretório já existe
            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path)
                print(f"Diretório '{new_dir_name}' criado com sucesso em '{folder_path}'")
            else:
                print(f"O diretório '{new_dir_name}' já existe em '{folder_path}'.")
        except Exception as e:
            print(f"Erro ao criar o diretório: {e}")
    else:
        print("Nenhuma pasta selecionada.")
