import os
import shutil
from tkinter import messagebox
from send2trash import send2trash  # Importa a função send2trash

class BasicFunctions:
    def __init__(self, directory_tree):
        self.directory_tree = directory_tree

    def create_new_folder(self):
        tree = self.directory_tree.tree
        selected_item = tree.selection()
        
        if selected_item:
            parent_item = selected_item[0]
            parent_path = self.directory_tree._get_full_path(parent_item)
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
                self.directory_tree.tree.insert(parent_item, "end", text=new_folder_name, open=False, image=self.directory_tree.folder_icon)
            else:
                self.directory_tree._add_items("", parent_path)
            print(f"Pasta '{new_folder_name}' criada em '{parent_path}'")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar a pasta: {e}")

    def rename_item(self, item, new_name):
        if not item:
            return
        
        parent_path = self.directory_tree._get_full_path(self.directory_tree.tree.parent(item))
        old_name = self.directory_tree.tree.item(item, "text").strip()
        new_item_path = os.path.join(parent_path, new_name)
        old_item_path = os.path.join(parent_path, old_name)

        if os.path.exists(new_item_path) and new_item_path != old_item_path:
            messagebox.showerror("Erro", "Um item com esse nome já existe.")
            return

        try:
            os.rename(old_item_path, new_item_path)
            self.directory_tree.tree.item(item, text=new_name)
            print(f"Item renomeado de '{old_name}' para '{new_name}'")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao renomear o item: {e}")

    def delete_item(self, item):
        if not item:
            return
        
        item_path = self.directory_tree._get_full_path(item)
        if messagebox.askyesno("Deletar Item", f"Quer mesmo deletar '{item_path}'? O arquivo ficará na lixeira do seu computador."):
            try:
                send2trash(item_path)  # Envia o item para a Lixeira
                self.directory_tree.tree.delete(item)
                print(f"Item '{item_path}' enviado para a lixeira")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar o item: {e}")
