frutas = ['maçã','pera','uva','abacate','gato']

print('Qtde itens: ',len(frutas))

print(frutas[0])
print(frutas[2])
print(frutas[4])

frutas.append('carambola') # append acrescenta dados
frutas.append('jaca')

print('Qtde itens: ',len(frutas))

print(frutas[5])
print(frutas[6])

frutas.pop(4)  # pop deleta dados
print('Qtde itens: ',len(frutas))

#frutas.remove('gato') remove para deletar pelo nome e não pela posição
frutas.remove('jaca')
print('Qtde itens: ',len(frutas))


print(frutas[4])
#print(frutas[5])

frutas[2] = 'melancia' #substituindo iten 2 por melancia
print(frutas[2])
print('Qtde itens: ',len(frutas))
