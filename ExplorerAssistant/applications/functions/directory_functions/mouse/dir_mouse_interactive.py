import os
import shutil
import tkinter as tk
from tkinter import messagebox

class DirectoryMouseInteractive:
    def __init__(self, directory_tree):
        self.directory_tree = directory_tree
        self.bind_events()
        self.drag_data = {"item": None, "start_x": 0, "start_y": 0}

    def bind_events(self):
        tree = self.directory_tree.tree
        tree.bind("<Button-1>", self.on_left_click)  # Bind left-click event
        tree.bind("<Button-2>", self.on_middle_click)  # Bind middle-click event
        tree.bind("<B1-Motion>", self.on_mouse_drag)  # Bind mouse drag event
        tree.bind("<ButtonRelease-1>", self.on_mouse_release)  # Bind mouse release event

    def on_left_click(self, event):
        tree = self.directory_tree.tree
        item = tree.identify_row(event.y)
        if item:
            # Verifica se o item já está selecionado e remove a seleção se necessário
            selected_items = tree.selection()
            if item in selected_items:
                tree.selection_remove(item)
            else:
                tree.selection_set(item)

    def on_middle_click(self, event):
        # Aqui você pode implementar a lógica para o botão do meio do mouse se necessário
        pass

    def on_mouse_drag(self, event):
        tree = self.directory_tree.tree
        if self.drag_data["item"]:
            x = event.x
            y = event.y
            tree.move(self.drag_data["item"], self.get_target_node(x, y))
            tree.update_idletasks()

    def on_mouse_release(self, event):
        tree = self.directory_tree.tree
        if self.drag_data["item"]:
            target_node = self.get_target_node(event.x, event.y)
            if target_node:
                self.move_item(self.drag_data["item"], target_node)
            self.drag_data["item"] = None

    def get_target_node(self, x, y):
        tree = self.directory_tree.tree
        item = tree.identify_row(y)
        if item:
            return item
        return None

    def move_item(self, source_item, target_node):
        if not target_node:
            return
        
        source_path = self.directory_tree._get_full_path(source_item)
        target_path = self.directory_tree._get_full_path(target_node)
        new_path = os.path.join(target_path, os.path.basename(source_path))
        
        try:
            if os.path.isdir(source_path):
                shutil.move(source_path, new_path)
            else:
                shutil.move(source_path, new_path)
            self.directory_tree.refresh()  # Atualize a árvore para refletir as mudanças
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao mover o item: {e}")

