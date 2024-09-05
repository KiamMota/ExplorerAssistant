import tkinter as tk
from tkinter import messagebox

class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.loading_window = None
        self.message_label = None

    def show_loading(self):
        # Cria uma janela de carregamento
        if self.loading_window is None or not self.loading_window.winfo_exists():
            self.loading_window = tk.Toplevel(self.root)
            self.loading_window.title("Carregando")
            self.loading_window.geometry("300x100+{}+{}".format(
                (self.root.winfo_screenwidth() - 300) // 2,
                (self.root.winfo_screenheight() - 100) // 2
            ))
            self.loading_window.transient(self.root)  # Torna a janela dependente da janela principal
            self.loading_window.grab_set()  # Faz com que a janela de carregamento seja modal
            
            # Adiciona uma label com a mensagem de carregamento
            self.message_label = tk.Label(self.loading_window, text="Desenhando a árvore de diretórios, aguarde...", padx=20, pady=20)
            self.message_label.pack(expand=True, fill=tk.BOTH)
            
            self.root.update_idletasks()  # Atualiza o estado da interface

    def hide_loading(self):
        # Fecha a janela de carregamento
        if self.loading_window is not None and self.loading_window.winfo_exists():
            self.loading_window.destroy()

    def show_access_denied(self):
        messagebox.showerror("Erro de Acesso", "Desculpe! O Acesso ao diretório foi negado.")

# Exemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    loading = LoadingScreen(root)

    # Exemplo de mostrar a tela de carregamento e depois escondê-la
    loading.show_loading()
    root.after(3000, loading.hide_loading)  # Esconde a tela de carregamento após 3 segundos

    root.mainloop()
