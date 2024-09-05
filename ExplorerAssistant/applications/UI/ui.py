import tkinter as tk
from tkinter import filedialog
from applications.functions.select_new_directory import create_new_directory
from applications.functions.directory_functions.directory_tree import DirectoryTree
from applications.functions.directory_functions.loading import LoadingScreen
from applications.functions.ph.create_text import FileCreator

def show_loading_message():
    # Mostra a mensagem de carregamento
    loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    root.update_idletasks()  # Atualiza o layout imediatamente

def hide_loading_message():
    # Oculta a mensagem de carregamento
    loading_label.place_forget()
    root.update_idletasks()  # Atualiza o layout imediatamente

def on_directory_selected():
    # Mostra a mensagem de carregamento
    show_loading_message()
    
    # Solicita ao usuário a seleção de um diretório
    path = filedialog.askdirectory(title="Selecione a Pasta", parent=root)
    if path:  # Verifica se o usuário selecionou um diretório
        try:
            # Popula o tree view e atualiza o label
            directory_tree.populate(path)
            path_label.config(text=f"Diretório Atual: {path}")
        except PermissionError as e:
            # Compila o erro e exibe na interface
            error_message = f"Acesso ao diretório '{path}' negado pelo sistema."
    
    # Oculta a mensagem de carregamento
    hide_loading_message()

def create_ui():
    global root, directory_tree, path_label, loading_label
    
    root = tk.Tk()
    root.geometry("600x600")
    root.resizable(False, False)
    root.title("Explorer Assistant")
    root.option_add("*Font", "Courier 10")
    icon_size = 30  # Tamanho dos ícones

    # Carrega os ícones e ajusta o tamanho
    folderplus_icon = tk.PhotoImage(file="icons/folderplus.png").subsample(2, 2)
    folder_icon = tk.PhotoImage(file="icons/folder.png").subsample(2, 2)
    folderconfigs_icon = tk.PhotoImage(file="icons/folderconfigs.png").subsample(2, 2)
    configs_icon = tk.PhotoImage(file="icons/configs.png").subsample(2, 2)
    
    # Carrega o novo ícone para "addfile" e os ícones existentes para back e preview
    addfile_icon = tk.PhotoImage(file="icons/addfile.png").subsample(2, 2)
    back_icon = tk.PhotoImage(file="icons/main ui/backaction.png").subsample(2, 2)
    preview_icon = tk.PhotoImage(file="icons/main ui/previewaction.png").subsample(2, 2)
    
    # Cria um frame para os botões (barra de ferramentas)
    toolbar_frame = tk.Frame(root, relief=tk.RAISED, bd=1)
    toolbar_frame.pack(side=tk.TOP, fill=tk.X)

    # Adiciona os botões com os ícones
    icons = [folderplus_icon] + [folder_icon] * 4 + [addfile_icon, folderconfigs_icon, configs_icon]

    for i, icon in enumerate(icons):
        button = tk.Button(toolbar_frame, image=icon, relief=tk.RAISED, borderwidth=1, width=icon_size, height=icon_size)
        button.grid(row=0, column=i, padx=1, pady=2)
        if i == 0:  # O primeiro botão é o botão para selecionar um diretório
            button.config(command=on_directory_selected)

    # Espaço entre os ícones da esquerda e os novos ícones no lado direito
    spacer = tk.Label(toolbar_frame, width=10)  # Espaçamento entre os ícones
    spacer.grid(row=0, column=len(icons))

    # Adiciona os dois novos botões à direita
    back_button = tk.Button(toolbar_frame, image=back_icon, relief=tk.RAISED, borderwidth=1, width=icon_size, height=icon_size)
    back_button.grid(row=0, column=len(icons) + 1, padx=1, pady=2)

    preview_button = tk.Button(toolbar_frame, image=preview_icon, relief=tk.RAISED, borderwidth=1, width=icon_size, height=icon_size)
    preview_button.grid(row=0, column=len(icons) + 2, padx=1, pady=2)

    # Cria o frame para o Treeview
    tree_frame = tk.Frame(root)
    tree_frame.pack(expand=True, fill=tk.BOTH)

    # Adiciona o DirectoryTree
    directory_tree = DirectoryTree(tree_frame)

    # Cria o frame para o caminho do diretório atual
    path_frame = tk.Frame(root, relief=tk.RAISED, bd=1, padx=10, pady=5)
    path_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # Adiciona o Label para mostrar o caminho do diretório atual
    path_label = tk.Label(path_frame, text="Diretório Atual: Nenhum", anchor=tk.W, padx=10, pady=5)
    path_label.pack(fill=tk.X)

    # Cria o Label para a mensagem de carregamento
    loading_label = tk.Label(root, text="Desenhando a árvore de diretórios, aguarde...", font=("Courier", 14), bg="lightgray")
    loading_label.place_forget()  # Inicialmente escondido

    # Inicia o loop principal da interface gráfica
    root.mainloop()

if __name__ == "__main__":
    create_ui()
