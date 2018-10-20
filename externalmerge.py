import struct
import sys
import os

registroCEP = struct.Struct("72s72s72s72s2s8s2s")
cepColumn = 5
f = open ("cep.dat", "rb")
novo = open ("novocepordenado.txt", "wb") #cria um novo arquivo, que vai armazenar os registros ordenados
tam = os.path.getsize("cep.dat")/registroCEP.size #pega o tamanho do arquivo
registro = registroCEP.size

tamBloco = 200 #define o tamanho de cada bloco, em linhas
blocos = []
qtdeBlocos = tam / tamBloco #define quantos blocos é possível obter no arquivo
resto = tam - (tamBloco * qtdeBlocos) #pega as eventuais linhas que sobrarem, para gerar um último bloco com tamanho diferente dos demais
listaBlocos = []
blocos = [tamBloco * qtdeBlocos]
if resto > 0:
    blocos.append(resto)

#função que retorna a coluna do CEP, dentro do registro, para ser usada pelo sort.
def getCEP (registroCEP):
    return cepColumn

#função para comparar CEPS, para ser usada no merge.
def cmp (ta, tb):
    if ta[cepColumn] == tb[cepColumn]: return 0
    if ta[cepColumn] > tb[cepColumn]: return 1    
    return -1

def merge(listaBlocos):

    for item in listaBlocos:
        while listaBlocos > 1:
            a = item
            b = item + 1
            arq1 = open("arq1.txt", "w")
            arq2 = open("arq2.txt", "w")
            resultado = open("resultado.txt","w")
            arq1.write(a)
            arq2.write(b)
            tam1 = os.path.getsize("arq1.txt")/registroCEP.size
            tam2 = os.path.getsize("arq2.txt")/registroCEP.size
            linhaArq1 = registroCEP.unpack(arq1.readline(registroCEP.size))
            linhaArq2 = registroCEP.unpack(arq2.readline(registroCEP.size))
            leitor1 = 0
            leitor2 = 0
            while leitor1 < tam1 and leitor2 < tam2:
                if cmp(linhaArq1,linhaArq2) == 1:
                    resultado.write(registroCEP.pack(*linhaArq2))
                    leitor2 += 1
                    if leitor2 < tam2:
                        linhaArq2 = registroCEP.unpack(arq2.readline(registroCEP.size))
                else:
                    resultado.write(registroCEP.pack(*linhaArq1))
                    leitor1 += 1
                    if leitor1 < tam1:
                        linhaArq1 = registroCEP.unpack(arq1.readline(registroCEP.size))
            while (leitor1 < tam1):
    	        resultado.write(registroCEP.pack(*linhaArq1))
                leitor1 += 1
	            if leitor1 < tam1:
		            linhaArq1 = registroCEP.unpack(arq1.readline(registroCEP.size))

            while (leitor2 < tam2):
	            resultado.write(registroCEP.pack(*linhaArq2))
	            leitor2 += 1
	            if leitor2 < tam2:
		            linhaArq2 = registroCEP.unpack(arq2.readline(registroCEP.size))
            
            listaBlocos.append(resultado)
            arq1.close()
            arq2.close()
            resultado.close()
            del(listaBlocos[1])
            del(listaBlocos[0])
            
    return listaBlocos[0]

contMove = 0 #a variável que irá iterar no arquivo

for i in blocos: #itera em cada bloco armazenado na lista

    listaOrdenada = []
    cont = i
    f.seek(contMove*registro*tamBloco) #dá saltos no arquivo, de bloco em bloco
    
    ta = 0
    tb = 0

    while cont !=0: #nesse loop, cada linha do arquivo, respeitado o tamanho do bloco, é transcrita para uma nova lista
        line = f.read(registroCEP.size)
        linha = registroCEP.unpack(line)
        listaOrdenada.append(linha)
        cont = cont-1
    
    listaOrdenada.sort(key = getCEP) #ordena a nova lista que foi criada no loop anterior

    listaBlocos.append(listaOrdenada) #armazena a lista ordenada em uma outra lista, para fazer o merge
    
    contMove = contMove + 1
    listaOrdenada = [] #zera a lista, para que ela armazene um novo bloco na próxima iteração

listaResultado = merge(listaBlocos)

novo.append(listaResultado)

f.close()
novo.close()

