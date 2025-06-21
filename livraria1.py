import tkinter as tk
from tkinter import messagebox




valorPadx = 5
valorPady = 5

fonte = ['Calibri', 16]

largura = 20

livraria = []

def limparTela():
    entryISBN.delete(0,tk.END)
    entryTítulo.delete(0,tk.END)
    entryAutor.delete(0,tk.END)
    entryEditora.delete(0,tk.END)
    entryPáginas.delete(0,tk.END)
    entryAno.delete(0,tk.END)
    entryGênero.delete(0,tk.END)

def gravar():
    livro = {'ISBN': entryISBN.get(),
         'Titulo'  : entryTítulo.get(),
         'Autor'   : entryAutor.get(),
         'Editora' : entryEditora.get(),
         'Páginas' : entryPáginas.get(),
         'Ano'     : entryAno.get(),
         'Gênero'  : entryGênero.get()
         }    
    livraria.append(livro)
    messagebox.showinfo('Sucesso','Livro cadastrado')
    limparTela()

janela = tk.Tk()
janela.title('Cadastro de Livros')
janela.geometry('500x360')

labelISBN= tk.Label(janela,text='ISBN', font=fonte,width=10,)
labelISBN.grid(row=0,column=0,padx=valorPadx,pady=valorPady)
entryISBN=tk.Entry(janela,font=fonte,width=30,justify='center')
entryISBN.grid(row=0,column=1,padx=valorPadx,pady=valorPady)

labelTítulo= tk.Label(janela,text='Título', font=fonte,width=10)
labelTítulo.grid(row=1,column=0,padx=valorPadx,pady=valorPady)
entryTítulo=tk.Entry(janela,font=fonte,width=30,justify='center')
entryTítulo.grid(row=1,column=1,padx=valorPadx,pady=valorPady)


labelTítulo= tk.Label(janela,text='Título', font=fonte,width=10)
labelTítulo.grid(row=1,column=0,padx=valorPadx,pady=valorPady)
entryTítulo=tk.Entry(janela,font=fonte,width=30,justify='center')
entryTítulo.grid(row=1,column=1,padx=valorPadx,pady=valorPady)


labelAutor= tk.Label(janela,text='Autor', font=fonte,width=10)
labelAutor.grid(row=2,column=0,padx=valorPadx,pady=valorPady)
entryAutor=tk.Entry(janela,font=fonte,width=30,justify='center')
entryAutor.grid(row=2,column=1,padx=valorPadx,pady=valorPady)


labelEditora= tk.Label(janela,text='Editora', font=fonte,width=10)
labelEditora.grid(row=3,column=0,padx=valorPadx,pady=valorPady)
entryEditora=tk.Entry(janela,font=fonte,width=30,justify='center')
entryEditora.grid(row=3,column=1,padx=valorPadx,pady=valorPady)

labelPáginas= tk.Label(janela,text='Páginas', font=fonte,width=10)
labelPáginas.grid(row=4,column=0,padx=valorPadx,pady=valorPady)
entryPáginas=tk.Entry(janela,font=fonte,width=30,justify='center')
entryPáginas.grid(row=4,column=1,padx=valorPadx,pady=valorPady)


labelAno= tk.Label(janela,text='Ano', font=fonte,width=10)
labelAno.grid(row=5,column=0,padx=valorPadx,pady=valorPady)
entryAno=tk.Entry(janela,font=fonte,width=30,justify='center')
entryAno.grid(row=5,column=1,padx=valorPadx,pady=valorPady)

labelGênero= tk.Label(janela,text='Gênero', font=fonte,width=10)
labelGênero.grid(row=6,column=0,padx=valorPadx,pady=valorPady)
entryGênero=tk.Entry(janela,font=fonte,width=30,justify='center')
entryGênero.grid(row=6,column=1,padx=valorPadx,pady=valorPady)



buttonArea = tk.Frame(janela)
buttonArea.grid(row=8,column=0,padx=valorPadx,pady=valorPady,sticky='w',columnspan=2)

ButtonGravar= tk.Button(buttonArea,text='Gravar', font=fonte,width=13,command=gravar)
ButtonGravar.grid(row=0,column=1,padx=valorPadx,pady=valorPady,sticky='w')

ButtonDeletar= tk.Button(buttonArea,text='Deletar', font=fonte,width=13)
ButtonDeletar.grid(row=0,column=2,padx=valorPadx,pady=valorPady,sticky='w')


ButtonLocalizar= tk.Button(buttonArea,text='Localizar', font=fonte,width=13)
ButtonLocalizar.grid(row=0,column=3,padx=valorPadx,pady=valorPady,sticky='w')

listagem = tk.Text(janela)
listagem.grid(row=9,column=0,columnspan=2,padx=5,pady=5)






janela.mainloop()