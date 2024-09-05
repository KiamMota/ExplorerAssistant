import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from applications.functions.directory_functions.dir_basic_functions import DirectoryBasicFunctions
from applications.functions.directory_functions.mouse.dir_mouse_interactive import DirectoryMouseInteractive

class DirectoryTree:
    def __init__(self, parent):
        self.tree = ttk.Treeview(parent, show="tree")
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.current_path = ""
        self.tree.heading("#0", text="Diretórios", anchor=tk.W)
        self.tree.tag_configure('custom', font=('Courier', 10))

        self.folder_icon = tk.PhotoImage(file="icons/folder.png").subsample(2, 2)
        self.opened_folder_icon = tk.PhotoImage(file="icons/openedfolder.png").subsample(2, 2)
        self.audio_file_icon = tk.PhotoImage(file="icons/directory/audiofiles.png").subsample(2, 2)
        self.doc_file_icon = tk.PhotoImage(file="icons/configs.png").subsample(2, 2)

        # Ajusta a largura da coluna para adicionar espaço ao ícone
        self.tree.column("#0", width=300, anchor="w")

        self.event_handler = DirectoryEventHandler(self)
        self.observer = None
        self.stop_event = threading.Event()

        self.mouse_interactive = DirectoryMouseInteractive(self)
        self.basic_functions = DirectoryBasicFunctions(self)
        self.dragging_item = None

    def start_observer(self):
        if self.current_path and not self.observer:
            self.observer = Observer()
            self.observer.schedule(self.event_handler, path=self.current_path, recursive=True)
            self.observer.start()

    def stop_observer(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None

    def populate(self, path):
        self.stop_observer()
        self.current_path = path
        expanded_items = self.get_expanded_items()
        self.tree.delete(*self.tree.get_children())
        self._add_items("", path)
        self.set_expanded_items(expanded_items)
        self.start_observer()

    def get_expanded_items(self):
        expanded_items = set()
        for item in self.tree.get_children():
            expanded_items.update(self._get_expanded_items_recursively(item))
        return expanded_items

    def _get_expanded_items_recursively(self, item):
        expanded_items = set()
        if self.tree.item(item, "open"):
            expanded_items.add(item)
            for child in self.tree.get_children(item):
                expanded_items.update(self._get_expanded_items_recursively(child))
        return expanded_items
    
    def set_expanded_items(self, expanded_items):
        for item in expanded_items:
            self.tree.item(item, open=True)

    def _add_items(self, parent, path):
        try:
            entries = os.listdir(path)
        except PermissionError:
            print(f"Permissão negada para acessar o diretório: {path}")
            return
        except FileNotFoundError:
            print(f"Diretório não encontrado: {path}")
            return

        for entry in entries:
            entry_path = os.path.join(path, entry)
            try:
                if os.path.isdir(entry_path):
                    node = self.tree.insert(parent, "end", text=f"   {entry}", open=False, image=self.folder_icon)
                    self._add_items(node, entry_path)
                else:
                    ext = os.path.splitext(entry)[1].lower()
                    if ext in ['.mp3', '.wav', '.flac']:
                        icon = self.audio_file_icon
                    else:
                        icon = self.doc_file_icon
                    # Adiciona espaços antes do texto para criar padding
                    self.tree.insert(parent, "end", text=f"   {entry}", open=False, image=icon)
            except PermissionError:
                print(f"Permissão negada para acessar o item: {entry_path}")
                continue

class DirectoryEventHandler(FileSystemEventHandler):
    def __init__(self, directory_tree):
        self.directory_tree = directory_tree

    def on_modified(self, event):
        # Atualiza a árvore quando um arquivo ou diretório é modificado
        self._handle_event(event)

    def on_created(self, event):
        # Atualiza a árvore quando um arquivo ou diretório é criado
        self._handle_event(event)

    def on_deleted(self, event):
        # Atualiza a árvore quando um arquivo ou diretório é deletado
        self._handle_event(event)

    def on_moved(self, event):
        # Atualiza a árvore quando um arquivo ou diretório é movido
        self._handle_event(event)

    def _handle_event(self, event):
        # Verifica se o evento está dentro do diretório atual
        if not event.src_path.startswith(self.directory_tree.current_path):
            return
        self.directory_tree.populate(self.directory_tree.current_path)
