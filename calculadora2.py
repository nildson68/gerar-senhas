import tkinter as tk
from tkinter import messagebox

def somar():
    num1 = float(entryNum1.get())
    num2 = float(entryNum2.get())
    resultado = num1 + num2
    messagebox.showinfo('Resultado', f'A soma é {resultado:.2f}')

def subtrair():
    num1 = float(entryNum1.get())
    num2 = float(entryNum2.get())
    resultado = num1 - num2
    messagebox.showinfo('Resultado', f'A subtração é {resultado:.2f}')

def dividir():
    num1 = float(entryNum1.get())
    num2 = float(entryNum2.get())
    resultado = num1 / num2
    messagebox.showinfo('Resultado', f'A divisão é {resultado:.2f}')

def multiplicar():
    num1 = float(entryNum1.get())
    num2 = float(entryNum2.get())
    resultado = num1 * num2
    messagebox.showinfo('Resultado', f'A multiplicação é {resultado:.2f}')

valorPadx = 5
ValorPady = 5
fonte = ['calibri',12]
largura = 40

janela = tk.Tk()
janela.title('C A L C U L A D O R A')
janela.geometry('800x250')
janela.configure(bg='#A9A9A9')

labelnum1 = tk.Label(janela,text='Digite um número ', font=fonte, width=largura, bg='#778899')
labelnum1.grid(row=0, column=0, padx=valorPadx, pady=ValorPady)
entryNum1 = tk.Entry(janela, font=fonte, width=largura, justify='right')
entryNum1.grid(row=0, column=1, padx=valorPadx, pady=ValorPady)

labelnum2 = tk.Label(janela,text='Digite outro número ', font=fonte, width=largura, bg='#778899')
labelnum2.grid(row=1, column=0,padx=valorPadx, pady=ValorPady)
entryNum2 = tk.Entry(janela, font=fonte, width=largura, justify='right')
entryNum2.grid(row=1, column=1, padx=valorPadx, pady=ValorPady)

buttonSomar = tk.Button(janela, text='SOMAR', font=fonte, width=20,bg='#778899', command=somar)
buttonSomar.grid(row=2, column=0, padx=valorPadx, pady=ValorPady)

buttonSub = tk.Button(janela, text='SUBTRAIR', font=fonte, width=20,bg='#778899', command=subtrair)
buttonSub.grid(row=2, column=1, padx=valorPadx, pady=ValorPady)


buttonDiv = tk.Button(janela, text='DIVISÃO', font=fonte, width=20, bg='#778899', command=dividir)
buttonDiv.grid(row=3, column=0, padx=valorPadx, pady=ValorPady)

buttonMult = tk.Button(janela, text='MULTIPLICAR', font=fonte, width=20,bg='#778899', command=multiplicar)
buttonMult.grid(row=3, column=1, padx=valorPadx, pady=ValorPady)





janela.mainloop()