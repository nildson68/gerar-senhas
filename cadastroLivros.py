import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os

# Configurações iniciais
valorPadx = 5
valorPady = 5
fonte = ['Calibri', 16]
largura = 20
livraria = []
indice_selecionado = None
ARQUIVO_JSON = 'livros.json'

# Funções de persistência
def carregar_livros():
    global livraria
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
            livraria = json.load(f)

def salvar_livros():
    with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(livraria, f, ensure_ascii=False, indent=4)

def limparTela():
    entryISBN.delete(0, tk.END)
    entryTítulo.delete(0, tk.END)
    entryAutor.delete(0, tk.END)
    entryEditora.delete(0, tk.END)
    entryPáginas.delete(0, tk.END)
    entryAno.delete(0, tk.END)
    entryGênero.delete(0, tk.END)

def gravar():
    livro = {
        'ISBN': entryISBN.get(),
        'Titulo': entryTítulo.get(),
        'Autor': entryAutor.get(),
        'Editora': entryEditora.get(),
        'Páginas': entryPáginas.get(),
        'Ano': entryAno.get(),
        'Gênero': entryGênero.get()
    }
    livraria.append(livro)
    salvar_livros()
    messagebox.showinfo('Sucesso', 'Livro cadastrado')
    limparTela()
    atualizar_tabela()

def atualizar_tabela():
    for row in tabela.get_children():
        tabela.delete(row)

    for livro in livraria:
        tabela.insert('', 'end', values=(
            livro['ISBN'],
            livro['Titulo'],
            livro['Autor'],
            livro['Editora'],
            livro['Páginas'],
            livro['Ano'],
            livro['Gênero']
        ))

def preencher_campos(event):
    global indice_selecionado

    item_selecionado = tabela.selection()
    if item_selecionado:
        item_index = tabela.index(item_selecionado[0])
        indice_selecionado = item_index
        valores = tabela.item(item_selecionado)['values']

        entryISBN.delete(0, tk.END)
        entryISBN.insert(0, valores[0])

        entryTítulo.delete(0, tk.END)
        entryTítulo.insert(0, valores[1])

        entryAutor.delete(0, tk.END)
        entryAutor.insert(0, valores[2])

        entryEditora.delete(0, tk.END)
        entryEditora.insert(0, valores[3])

        entryPáginas.delete(0, tk.END)
        entryPáginas.insert(0, valores[4])

        entryAno.delete(0, tk.END)
        entryAno.insert(0, valores[5])

        entryGênero.delete(0, tk.END)
        entryGênero.insert(0, valores[6])

def excluir_livro():
    global indice_selecionado, livraria

    if indice_selecionado is not None:
        resposta = messagebox.askyesno('Confirmar Exclusão', 'Tem certeza que deseja excluir este livro?')
        if resposta:
            if 0 <= indice_selecionado < len(livraria):
                del livraria[indice_selecionado]
                salvar_livros()
                indice_selecionado = None
                limparTela()
                atualizar_tabela()
                messagebox.showinfo('Sucesso', 'Livro excluído com sucesso!')
    else:
        messagebox.showwarning('Aviso', 'Nenhum livro selecionado para excluir!')

def localizar_livro():
    termo_busca = entryTítulo.get().lower()

    if not termo_busca:
        messagebox.showwarning('Aviso', 'Digite um título para buscar!')
        return

    for item in tabela.selection():
        tabela.selection_remove(item)

    for item in tabela.get_children():
        valores = tabela.item(item)['values']
        titulo_livro = valores[1].lower()

        if termo_busca in titulo_livro:
            tabela.selection_add(item)
            tabela.see(item)

            entryISBN.delete(0, tk.END)
            entryISBN.insert(0, valores[0])
            entryTítulo.delete(0, tk.END)
            entryTítulo.insert(0, valores[1])
            entryAutor.delete(0, tk.END)
            entryAutor.insert(0, valores[2])
            entryEditora.delete(0, tk.END)
            entryEditora.insert(0, valores[3])
            entryPáginas.delete(0, tk.END)
            entryPáginas.insert(0, valores[4])
            entryAno.delete(0, tk.END)
            entryAno.insert(0, valores[5])
            entryGênero.delete(0, tk.END)
            entryGênero.insert(0, valores[6])
            return

    messagebox.showinfo('Busca', 'Nenhum livro encontrado com esse termo!')

# Interface
main = tk.Tk()
main.title('Cadastro de Livros')
main.geometry('1000x600')

janela = tk.Frame(main)
janela.pack(padx=5, pady=5)

labelISBN = tk.Label(janela, text='ISBN', font=fonte, width=10)
labelISBN.grid(row=0, column=0, padx=valorPadx, pady=valorPady)
entryISBN = tk.Entry(janela, font=fonte, width=30, justify='center')
entryISBN.grid(row=0, column=1, padx=valorPadx, pady=valorPady)

labelTítulo = tk.Label(janela, text='Título', font=fonte, width=10)
labelTítulo.grid(row=1, column=0, padx=valorPadx, pady=valorPady)
entryTítulo = tk.Entry(janela, font=fonte, width=30, justify='center')
entryTítulo.grid(row=1, column=1, padx=valorPadx, pady=valorPady)

labelAutor = tk.Label(janela, text='Autor', font=fonte, width=10)
labelAutor.grid(row=2, column=0, padx=valorPadx, pady=valorPady)
entryAutor = tk.Entry(janela, font=fonte, width=30, justify='center')
entryAutor.grid(row=2, column=1, padx=valorPadx, pady=valorPady)

labelEditora = tk.Label(janela, text='Editora', font=fonte, width=10)
labelEditora.grid(row=3, column=0, padx=valorPadx, pady=valorPady)
entryEditora = tk.Entry(janela, font=fonte, width=30, justify='center')
entryEditora.grid(row=3, column=1, padx=valorPadx, pady=valorPady)

labelPáginas = tk.Label(janela, text='Páginas', font=fonte, width=10)
labelPáginas.grid(row=4, column=0, padx=valorPadx, pady=valorPady)
entryPáginas = tk.Entry(janela, font=fonte, width=30, justify='center')
entryPáginas.grid(row=4, column=1, padx=valorPadx, pady=valorPady)

labelAno = tk.Label(janela, text='Ano', font=fonte, width=10)
labelAno.grid(row=5, column=0, padx=valorPadx, pady=valorPady)
entryAno = tk.Entry(janela, font=fonte, width=30, justify='center')
entryAno.grid(row=5, column=1, padx=valorPadx, pady=valorPady)

labelGênero = tk.Label(janela, text='Gênero', font=fonte, width=10)
labelGênero.grid(row=6, column=0, padx=valorPadx, pady=valorPady)
entryGênero = tk.Entry(janela, font=fonte, width=30, justify='center')
entryGênero.grid(row=6, column=1, padx=valorPadx, pady=valorPady)

# Botões
buttonArea = tk.Frame(janela)
buttonArea.grid(row=8, column=0, padx=valorPadx, pady=valorPady, sticky='w', columnspan=2)

ButtonGravar = tk.Button(buttonArea, text='Gravar', font=fonte, width=13, command=gravar)
ButtonGravar.grid(row=0, column=1, padx=valorPadx, pady=valorPady, sticky='w')

ButtonDeletar = tk.Button(buttonArea, text='Excluir', font=fonte, width=13, command=excluir_livro)
ButtonDeletar.grid(row=0, column=2, padx=valorPadx, pady=valorPady, sticky='w')

ButtonLocalizar = tk.Button(buttonArea, text='Localizar', font=fonte, width=13, command=localizar_livro)
ButtonLocalizar.grid(row=0, column=3, padx=valorPadx, pady=valorPady, sticky='w')

# Tabela
frame_tabela = tk.Frame(main)
frame_tabela.pack(padx=10, pady=10, fill='both', expand=True)

tabela = ttk.Treeview(frame_tabela, columns=('ISBN', 'Título', 'Autor', 'Editora', 'Páginas', 'Ano', 'Gênero'), show='headings')

tabela.heading('ISBN', text='ISBN')
tabela.heading('Título', text='Título')
tabela.heading('Autor', text='Autor')
tabela.heading('Editora', text='Editora')
tabela.heading('Páginas', text='Páginas')
tabela.heading('Ano', text='Ano')
tabela.heading('Gênero', text='Gênero')

tabela.column('ISBN', width=100)
tabela.column('Título', width=150)
tabela.column('Autor', width=150)
tabela.column('Editora', width=100)
tabela.column('Páginas', width=70)
tabela.column('Ano', width=70)
tabela.column('Gênero', width=100)

scrollbar = ttk.Scrollbar(frame_tabela, orient='vertical', command=tabela.yview)
tabela.configure(yscroll=scrollbar.set)
scrollbar.pack(side='right', fill='y')

tabela.pack(fill='both', expand=True)
tabela.bind('<ButtonRelease-1>', preencher_campos)

# Inicializa os dados
carregar_livros()
atualizar_tabela()

main.mainloop()