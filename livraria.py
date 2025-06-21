import tkinter as tk
from tkinter import messagebox 

valorPadx = 5
ValorPady = 5
fonte = ['calibri',12]
largura = 20

janela = tk.Tk()
janela.title('CADASTRO DE LIVROS')
janela.geometry('1120x300')
janela.configure(bg='#C0C0C0')

labelIsbn = tk.Label(janela,text='ISBN ', font=fonte, width=largura, bg='#4F4F4F')
labelIsbn.grid(row=0, column=0, padx=valorPadx, pady=ValorPady)
entryIsbn = tk.Entry(janela, font=fonte, width=largura, justify='left', bg='#DCDCDC')
entryIsbn.grid(row=0, column=1, padx=valorPadx, pady=ValorPady)

labelTitulo = tk.Label(janela,text='TÍTULO ', font=fonte, width=largura, bg='#4F4F4F')
labelTitulo.grid(row=1, column=0, padx=valorPadx, pady=ValorPady)
entryTitulo = tk.Entry(janela, font=fonte, width=45, justify='left',bg='#DCDCDC')
entryTitulo.grid(row=1, column=1, padx=valorPadx, pady=ValorPady)

labelAutor = tk.Label(janela,text='AUTOR ', font=fonte, width=largura, bg='#4F4F4F')
labelAutor.grid(row=1, column=2, padx=valorPadx, pady=ValorPady)
entryAutor = tk.Entry(janela, font=fonte, width=45, justify='left' ,bg='#DCDCDC')
entryAutor.grid(row=1, column=3, padx=valorPadx, pady=ValorPady)

labelEditora = tk.Label(janela,text='EDITORA ', font=fonte, width=largura, bg='#4F4F4F')
labelEditora.grid(row=2, column=0, padx=valorPadx, pady=ValorPady)
entryEditora = tk.Entry(janela, font=fonte, width=45, justify='left' ,bg='#DCDCDC')
entryEditora.grid(row=2, column=1, padx=valorPadx, pady=ValorPady)

labelGenero = tk.Label(janela,text='GÊNERO ', font=fonte, width=largura, bg='#4F4F4F')
labelGenero.grid(row=2, column=2, padx=valorPadx, pady=ValorPady)
entryGenero = tk.Entry(janela, font=fonte, width=45, justify='left',bg='#DCDCDC')
entryGenero.grid(row=2, column=3, padx=valorPadx, pady=ValorPady)

labelPaginas = tk.Label(janela,text='NUM DE PÁGINAS ', font=fonte, width=largura, bg='#4F4F4F')
labelPaginas.grid(row=3, column=0, padx=valorPadx, pady=ValorPady)
entryPaginas = tk.Entry(janela, font=fonte, width=45, justify='left' ,bg='#DCDCDC')
entryPaginas.grid(row=3, column=1, padx=valorPadx, pady=ValorPady)

labelAno = tk.Label(janela,text='ANO PUBLICAÇÃO ', font=fonte, width=largura, bg='#4F4F4F')
labelAno.grid(row=3, column=2, padx=valorPadx, pady=ValorPady)
entryAno = tk.Entry(janela, font=fonte, width=45, justify='left',bg='#DCDCDC') 
entryAno.grid(row=3, column=3, padx=valorPadx, pady=ValorPady)

buttonGravar = tk.Button(janela, text='GRAVAR', font=fonte, width=20,bg='#696969')
buttonGravar.grid(row=4, column=0, padx=valorPadx, pady=ValorPady)

buttonExcluir = tk.Button(janela, text='EXCLUIR', font=fonte, width=20,bg='#696969')
buttonExcluir.grid(row=4, column=1, padx=valorPadx, pady=ValorPady)

buttonLocalizar = tk.Button(janela, text='LOCALIZAR', font=fonte, width=20,bg='#696969')
buttonLocalizar.grid(row=4, column=2, padx=valorPadx, pady=ValorPady)



janela.mainloop()