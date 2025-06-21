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
fonte = ['calibri',18]
largura = 80

janela = tk.Tk()
janela.title('C A L C U L A D O R A')
janela.geometry('800x600')

labelnum1 = tk.Label(janela,text='Digite um número ', font=fonte, width=largura)
labelnum1.pack(padx=valorPadx, pady=ValorPady)
entryNum1 = tk.Entry(janela, font=fonte, width=largura, justify='right')
entryNum1.pack(padx=valorPadx, pady=ValorPady)

labelnum2 = tk.Label(janela,text='Digite outro número ', font=fonte, width=largura)
labelnum2.pack(padx=valorPadx, pady=ValorPady)
entryNum2 = tk.Entry(janela, font=fonte, width=largura, justify='right')
entryNum2.pack(padx=valorPadx, pady=ValorPady)

buttonSomar = tk.Button(janela, text='SOMAR', font=fonte, width=20, command=somar)
buttonSomar.pack(padx=valorPadx, pady=ValorPady)

buttonSub = tk.Button(janela, text='SUBTRAIR', font=fonte, width=20, command=subtrair)
buttonSub.pack(padx=valorPadx, pady=ValorPady)


buttonDiv = tk.Button(janela, text='DIVISÃO', font=fonte, width=20, command=dividir)
buttonDiv.pack(padx=valorPadx, pady=ValorPady)

buttonMult = tk.Button(janela, text='MULTIPLICAR', font=fonte, width=20, command=multiplicar)
buttonMult.pack(padx=valorPadx, pady=ValorPady)





janela.mainloop()