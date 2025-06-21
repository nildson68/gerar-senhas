import tkinter as tk
from tkinter import messagebox

# def mensagem():
#    messagebox.showinfo('ATENÇÃO ', F'Olá {entryNome.get()}')

valorPadx = 10
valorPady = 10

janelaPrincipal = tk.Tk()
janelaPrincipal.title('Minha primeira janela')
janelaPrincipal.geometry('800x600') # geometry altera o tamanho da janela
janelaPrincipal.configure(bg='blue') # muda a cor da janela

labelFrase = tk.Label(janelaPrincipal, text='Seja bem vindo',bg='blue',fg='white', font=['arial', 20]) #pack posiciona o objeto na tela
labelFrase.pack(padx=valorPadx,pady=valorPady)

labelNome = tk.Label(janelaPrincipal, text='Digite seu nome')
labelNome.pack(padx=valorPadx, pady=valorPady)
entryNome = tk.Entry(janelaPrincipal,width=60, font=['verdana',20], bg='black', fg='yellow')
entryNome.pack(padx=valorPadx, pady=valorPady)

buttonEnviar = tk.Button(janelaPrincipal, text='Enviar',width=20,font=['verdana', 20],bg='yellow',fg='black',command=lambda: messagebox.showinfo('ATENÇÃO ', F'Olá {entryNome.get()}'))
buttonEnviar.pack(padx=valorPadx, pady=valorPady)

janelaPrincipal.mainloop()