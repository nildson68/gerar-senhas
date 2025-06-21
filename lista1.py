import tkinter as tk
from tkinter import messagebox

valorPadx = 8
valorPady = 8
fonte     = ['Calibri',12]
largura   = 60

livraria=[]

def limparTela():
    entryISBN.delete(0,tk.END)
    entrytitulo.delete(0,tk.END)
    entryAutor.delete(0,tk.END)
    entryEditora.delete(0,tk.END)
    entryPaginas.delete(0,tk.END)
    entryAno.delete(0,tk.END)
    entryGenero.delete(0,tk.END)

def gravar():
    livro ={'ISBN': entryISBN.get(),
        'Titulo'  :entrytitulo.get(),
        'Autor'   :entryAutor.get(),
        'Editora' :entryEditora.get(),
        'Paginas' :entryPaginas.get(),
        'Ano'     :entryAno.get(),
        'Genero'  :entryGenero.get(),
    }
    livraria.append(livro)
    messagebox.showinfo('Sucesso','Livro Cadastrado')
    limparTela()
  

janela = tk.Tk()
janela.title('Cadastro de livro')
janela.geometry('1500x220')


labelISBN = tk.Label(janela,text='Digite o ISBN',font=fonte,width=largura)
labelISBN.grid(row=0,column=0,padx=valorPadx,pady=valorPady)
entryISBN = tk.Entry(janela,font=fonte,width=largura,justify='right')
entryISBN.grid(row=0,column=1,padx=valorPadx,pady=valorPady)

labeltitulo = tk.Label(janela,text='Titulo do livro',font=fonte,width=largura)
labeltitulo.grid(row=1,column=0,padx=valorPadx,pady=valorPady)
entrytitulo = tk.Entry(janela,font=fonte,width=largura)
entrytitulo.grid(row=1,column=1,padx=valorPadx,pady=valorPady)
 
labeAutor = tk.Label(janela,text='Nome do Autor',font=fonte,width=largura)
labeAutor.grid(row=2,column=0,padx=valorPadx,pady=valorPady)
entryAutor = tk.Entry(janela,font=fonte,width=largura,justify='right')
entryAutor.grid(row=2,column=1,padx=valorPadx,pady=valorPady)

labelEditora = tk.Label(janela,text='Nome da Editora',font=fonte,width=largura)
labelEditora.grid(row=3,column=0,padx=valorPadx,pady=valorPady)
entryEditora = tk.Entry(janela,font=fonte,width=largura,justify='right')
entryEditora.grid(row=3,column=1,padx=valorPadx,pady=valorPady)

labelPaginas = tk.Label(janela,text='Quantidade de paginas',font=fonte,width=largura)
labelPaginas.grid(row=4,column=0,padx=valorPadx,pady=valorPady)
entryPaginas = tk.Entry(janela,font=fonte,width=largura,justify='right')
entryPaginas.grid(row=4,column=1,padx=valorPadx,pady=valorPady)

labelAno = tk.Label(janela,text='Qual ano que foi lançado',font=fonte,width=largura)
labelAno.grid(row=5,column=0,padx=valorPadx,pady=valorPady)
entryAno = tk.Entry(janela,font=fonte,width=largura,justify='right')
entryAno.grid(row=5,column=1,padx=valorPadx,pady=valorPady)

labelGenero = tk.Label(janela,text='Qual o genero',font=fonte,width=largura)
labelGenero.grid(row=6,column=0,padx=valorPadx,pady=valorPady)
entryGenero = tk.Entry(janela,font=fonte,width=largura,justify='right')
entryGenero.grid(row=6,column=1,padx=valorPadx,pady=valorPady)

buttonGravar = tk.Button(janela,text='Gravar',font=fonte,width=largura,command=gravar)   
buttonGravar.grid(row=7,column=0,padx=valorPadx,pady=valorPady)

buttonExcluir = tk.Button(janela,text='Excluir',font=fonte,width=largura,command='')   
buttonExcluir.grid(row=7,column=1,padx=valorPadx,pady=valorPady)

buttonLocalizar = tk.Button(janela,text='Localizar',font=fonte,width=largura,command='')   
buttonLocalizar.grid(row=8,column=0,padx=valorPadx,pady=valorPady)




janela.mainloop()