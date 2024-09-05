import tkinter as tk
from tkinter import messagebox

class MouseMenu:
    def __init__(self, directory_tree):
        self.tree = directory_tree.tree
        self.menu = tk.Menu(self.tree, tearoff=0)
        self.create_menu()
        self.tree.bind("<Button-3>", self.show_menu)  # Bind do clique com o botão direito do mouse

    def create_menu(self):
        self.menu.add_command(label="Create New Folder (F)", command=self.create_folder)
        self.menu.add_command(label="Rename (R)", command=self.start_rename)
        self.menu.add_command(label="Delete (Del)", command=self.delete_item)

    def show_menu(self, event):
        self.tree.bind("<Button-1>", self.hide_menu)  # Bind do clique com o botão esquerdo do mouse
        self.menu.post(event.x_root, event.y_root)

    def hide_menu(self, event):
        self.menu.unpost()

    def create_folder(self):
        selected_item = self.tree.selection()
        if selected_item:
            # Implementar a criação de nova pasta na posição selecionada
            # Aqui você pode chamar o método da classe BasicFunctions se necessário
            pass

    def start_rename(self):
        selected_item = self.tree.selection()
        if selected_item:
            # Implementar a renomeação do item selecionado
            # Aqui você pode chamar o método da classe BasicFunctions se necessário
            pass

    def delete_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            # Implementar a exclusão do item selecionado
            # Aqui você pode chamar o método da classe BasicFunctions se necessário
            pass
