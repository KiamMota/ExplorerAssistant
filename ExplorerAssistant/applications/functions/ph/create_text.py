import tkinter as tk
from tkinter import simpledialog, messagebox
import os

class FileCreator:
    def __init__(self, root):
        self.root = root
        self.current_directory = None

    def set_current_directory(self, path):
        self.current_directory = path

    def create_text_files(self):
        # Verifica se um diretório está selecionado
        if not self.current_directory:
            messagebox.showwarning("Aviso", "Nenhum diretório selecionado. Selecione um diretório primeiro.")
            return

        # Abre a janela para perguntar o número de arquivos
        num_files = simpledialog.askinteger("Criar Arquivos", "Quantos arquivos .txt deseja criar?", minvalue=1)
        if num_files is None:
            return  # O usuário cancelou a entrada

        # Cria os arquivos de texto
        for i in range(num_files):
            file_path = os.path.join(self.current_directory, f"arquivo_{i + 1}.txt")
            with open(file_path, 'w') as file:
                file.write("Este é um arquivo de texto de placeholder.\n")

        messagebox.showinfo("Sucesso", f"{num_files} arquivos .txt foram criados no diretório selecionado.")

# Exemplo de integração com a interface gráfica
def on_addfile_button_click(file_creator):
    file_creator.create_text_files()

def create_ui():
    global file_creator
    
    root = tk.Tk()
    root.geometry("600x600")
    root.resizable(False, False)
    root.title("Explorer Assistant")
    root.option_add("*Font", "Courier 10")
    icon_size = 30  # Tamanho dos ícones

    # Instancia a classe FileCreator
    file_creator = FileCreator(root)

    # Carrega os ícones
    addfile_icon = tk.PhotoImage(file="icons/addfile.png").subsample(2, 2)
    
    # Cria um frame para os botões (barra de ferramentas)
    toolbar_frame = tk.Frame(root, relief=tk.RAISED, bd=1)
    toolbar_frame.pack(side=tk.TOP, fill=tk.X)

    # Adiciona o botão com o ícone addfile.png
    addfile_button = tk.Button(toolbar_frame, image=addfile_icon, relief=tk.RAISED, borderwidth=1, width=icon_size, height=icon_size)
    addfile_button.grid(row=0, column=0, padx=1, pady=2)
    addfile_button.config(command=lambda: on_addfile_button_click(file_creator))

    root.mainloop()

if __name__ == "__main__":
    create_ui()
