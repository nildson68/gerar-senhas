import tkinter as tk
from tkinter import messagebox
import json
import os

class CadastroProdutos:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Produtos")

        # Labels e Entradas
        tk.Label(root, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.codigo_entry = tk.Entry(root)
        self.codigo_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Produto:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.produto_entry = tk.Entry(root)
        self.produto_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Tipo de Produto:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.tipo_entry = tk.Entry(root)
        self.tipo_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Preço:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.preco_entry = tk.Entry(root)
        self.preco_entry.grid(row=3, column=1, padx=5, pady=5)

        # Botão para cadastrar
        self.btn_cadastrar = tk.Button(root, text="Cadastrar", command=self.cadastrar)
        self.btn_cadastrar.grid(row=4, column=0, columnspan=2, pady=10)

        # Lista para mostrar os produtos cadastrados
        self.lista_produtos = tk.Text(root, width=50, height=10)
        self.lista_produtos.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.lista_produtos.config(state='disabled')

        # Lista interna para armazenar os produtos
        self.produtos = []

        # Tenta carregar produtos do arquivo
        self.arquivo = "produtos.json"
        self.carregar_produtos()

    def cadastrar(self):
        codigo = self.codigo_entry.get().strip()
        produto = self.produto_entry.get().strip()
        tipo = self.tipo_entry.get().strip()
        preco = self.preco_entry.get().strip()

        if not codigo or not produto or not tipo or not preco:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        try:
            preco = float(preco)
        except ValueError:
            messagebox.showwarning("Erro", "Preço deve ser um número válido!")
            return

        # Adiciona o produto na lista
        self.produtos.append({
            "codigo": codigo,
            "produto": produto,
            "tipo": tipo,
            "preco": preco
        })

        # Salva os produtos no arquivo
        self.salvar_produtos()

        # Atualiza a área de texto
        self.atualizar_lista()

        # Limpa os campos
        self.codigo_entry.delete(0, tk.END)
        self.produto_entry.delete(0, tk.END)
        self.tipo_entry.delete(0, tk.END)
        self.preco_entry.delete(0, tk.END)

        messagebox.showinfo("Sucesso", "Produto cadastrado!")

    def atualizar_lista(self):
        self.lista_produtos.config(state='normal')
        self.lista_produtos.delete(1.0, tk.END)
        self.lista_produtos.insert(tk.END, "Código | Produto | Tipo | Preço\n")
        self.lista_produtos.insert(tk.END, "-"*40 + "\n")
        for p in self.produtos:
            linha = f"{p['codigo']} | {p['produto']} | {p['tipo']} | R$ {p['preco']:.2f}\n"
            self.lista_produtos.insert(tk.END, linha)
        self.lista_produtos.config(state='disabled')

    def salvar_produtos(self):
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.produtos, f, ensure_ascii=False, indent=4)

    def carregar_produtos(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                try:
                    self.produtos = json.load(f)
                    self.atualizar_lista()
                except json.JSONDecodeError:
                    messagebox.showerror("Erro", "Arquivo JSON corrompido!")
                    self.produtos = []

if __name__ == "__main__":
    root = tk.Tk()
    app = CadastroProdutos(root)
    root.mainloop()