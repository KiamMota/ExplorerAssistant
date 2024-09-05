import os
import shutil
from tkinter import messagebox, simpledialog
import tkinter as tk

class DirectoryBasicFunctions:
    def __init__(self, directory_tree):
        self.directory_tree = directory_tree
        self.tree = directory_tree.tree

        # Bind das hotkeys
        self.tree.bind("<KeyPress-f>", self.create_folder)
        self.tree.bind("<KeyPress-r>", self.start_rename)
        self.tree.bind("<Delete>", self.delete_item)

    def create_folder(self, event=None):
        selected_item = self.tree.selection()
        
        if selected_item:
            parent_item = selected_item[0]
            parent_path = self._get_full_path(parent_item)
        else:
            parent_path = self.directory_tree.current_path
            parent_item = ""

        new_folder_name = "NewFolder"
        new_folder_path = os.path.join(parent_path, new_folder_name)
        counter = 1
        while os.path.exists(new_folder_path):
            new_folder_name = f"NewFolder_{counter}"
            new_folder_path = os.path.join(parent_path, new_folder_name)
            counter += 1

        try:
            os.makedirs(new_folder_path)
            if parent_item:
                self.tree.insert(parent_item, "end", text=new_folder_name, open=False, image=self.directory_tree.folder_icon)
            else:
                self.directory_tree._add_items("", parent_path)
            print(f"Pasta '{new_folder_name}' criada em '{parent_path}'")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar a pasta: {e}")

    def start_rename(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item = selected_item[0]
        old_name = self.tree.item(item, "text").strip()
        new_name = self.prompt_rename(old_name)
        if new_name:
            self.rename_item(item, new_name)

    def prompt_rename(self, old_name):
        """Exibe uma caixa de diálogo simples para renomear o item."""
        new_name = simpledialog.askstring("Renomear Item", "Novo nome:", initialvalue=old_name)
        return new_name

    def rename_item(self, item, new_name):
        parent_path = self._get_full_path(self.tree.parent(item))
        old_name = self.tree.item(item, "text").strip()
        new_item_path = os.path.join(parent_path, new_name)
        old_item_path = os.path.join(parent_path, old_name)

        if os.path.exists(new_item_path) and new_item_path != old_item_path:
            messagebox.showerror("Erro", "Um item com esse nome já existe.")
            return

        try:
            os.rename(old_item_path, new_item_path)
            self.tree.item(item, text=new_name)
            print(f"Item renomeado de '{old_name}' para '{new_name}'")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao renomear o item: {e}")

    def delete_item(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item = selected_item[0]
        item_path = self._get_full_path(item)
        print(f"Tentando deletar: {item_path}")  # Adicione esta linha para depuração
        if not os.path.exists(item_path):
            messagebox.showerror("Erro", f"O item '{item_path}' não foi encontrado.")
            return
        if messagebox.askyesno("Deletar Item", f"Quer mesmo deletar '{item_path}'? Esta ação é irreversível."):
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                self.tree.delete(item)
                print(f"Item '{item_path}' excluído permanentemente")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar o item: {e}")
                
    def _get_full_path(self, item):
        """Obtém o caminho completo do item a partir da árvore."""
        path_parts = []
        while item:
            path_parts.append(self.tree.item(item, "text"))
            item = self.tree.parent(item)
        path_parts.reverse()
        full_path = os.path.join(self.directory_tree.current_path, *path_parts)
        print(f"Caminho completo: {full_path}")  # Adicione esta linha para depuração
        return full_path
