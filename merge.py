# -*- coding: utf-8 -*-
'''
Created on 19 de set de 2018
@author: Carla Lutz
'''
import struct
import sys
import os
from random import randint

filename = "cep_ordenado.dat"
f = open (filename, "r") #abre o arquivo
registroCEP = struct.Struct("72s72s72s72s2s8s2s")
cepColumn = 5
tam = os.path.getsize("cep_ordenado.dat") / registroCEP.size
print ("Quantidade de linhas: %d" % tam) #qtde de linhas a ser usada qdo o algoritmo estiver correto

lineCount = 0
qtdLinhas = 20
fout1 = open ("cep1.txt", "wb")
fout2 = open ("cep2.txt", "wb")
line = f.readline()
while lineCount < qtdLinhas:

    rand = randint(0,1)
    
    line = f.readline()
    if (rand == 1):
        
        fout1.write(line)
           
    else:
        
        fout2.write(line)
        
    lineCount += 1

fout1.close();
fout2.close();


#funcao para comparar ceps, entre maior ou menor
def cmp (ta, tb):
    if ta[cepColumn] == tb[cepColumn]: return 0
    if ta[cepColumn] > tb[cepColumn]: return 1    
    return -1

#algoritmo merge 
resultado = open ("result.txt", "wb")
tamA = os.path.getsize("cep1.txt")/registroCEP.size
tamB = os.path.getsize("cep2.txt")/registroCEP.size

conta = 0 #variavel para iterar no arquivo
contb = 0 #variavel para iterar no arquivo

a = open("cep1.txt", "rb")
b = open("cep2.txt", "rb")

lineA = registroCEP.unpack(a.readline(registroCEP.size))
lineB = registroCEP.unpack(b.readline(registroCEP.size))
while (conta < tamA and contb < tamB):
	if cmp(lineA, lineB) == 1:
		resultado.write(registroCEP.pack(*lineB))
		contb += 1
		if contb < tamB:
			lineB = registroCEP.unpack(b.readline(registroCEP.size))
	else:
		resultado.write(registroCEP.pack(*lineA))
		conta += 1
		if conta < tamA:
			lineA = registroCEP.unpack(a.readline(registroCEP.size))

while (conta < tamA):
	resultado.write(registroCEP.pack(*lineA))
	conta += 1
	if conta < tamA:
		lineA = registroCEP.unpack(a.readline(registroCEP.size))

while (contb < tamB):
	resultado.write(registroCEP.pack(*lineB))
	contb += 1
	if contb < tamB:
		lineB = registroCEP.unpack(b.readline(registroCEP.size))


f.close()
resultado.close()

