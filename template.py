import random
import math
import sys

#########
# Implementacao um esquema sem qualquer metodo de codificao.
#
# Cada byte do pacote original eh mapeado para o mesmo byte no pacote
# codificado.
########

###
##
# Funcoes a serem alteradas!
##
###

##
# Codifica o pacote de entrada, gerando um pacote
# de saida com bits redundantes.
##
def codePacket(originalPacket, row, column):
    ##
    # Argumentos:
    #  - originalPacket: pacote original a ser codificado na forma de uma lista.
    #  - row: qtd de linhas na matriz de paridade
    #  - column: qtd de colunas na matriz de paridade
    # Cada entrada na lista representa um bit do pacote (inteiro 0 ou 1).
    # Valor de retorno: pacote codificado no mesmo formato.
    ##
    parityMatrix = [[0 for x in range(column)] for y in range(row)]
    # vai precisar disso bastante, por isso tá pré-computado
    chunkSize = row * column
    codedChunkSize = ((row + 1) * (column + 1)) - 1
    codedLen = int(len(originalPacket) / chunkSize * codedChunkSize)
    codedPacket = [0 for x in range(codedLen)]
    originalPacketLength = len(originalPacket)
    ##
    # Itera por cada byte do pacote original.
    ##
    for i in range(int(originalPacketLength / chunkSize)):

        ##
        # Bits do i-esimo byte sao dispostos na matriz.
        ##
        for j in range(row):
            for k in range(column):
                parityMatrix[j][k] = originalPacket[i * chunkSize + column * j + k]

        ##
        # Replicacao dos bits de dados no pacote codificado.
        ##
        for j in range(chunkSize):
            codedPacket[i * codedChunkSize + j] = originalPacket[i * chunkSize + j]

        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das colunas.
        ##
        for j in range(column):
            sum = 0
            for k in range(row):
                sum += parityMatrix[k][j]
            if sum % 2 == 0:
                codedPacket[i * codedChunkSize + chunkSize + j] = 0
            else:
                codedPacket[i * codedChunkSize + chunkSize + j] = 1

        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das linhas.
        ##
        for j in range(row):
            sum = 0
            for k in range(column):
                sum += parityMatrix[j][k]
            if sum % 2 == 0:
                codedPacket[i * codedChunkSize + chunkSize + column + j] = 0
            else:
                codedPacket[i * codedChunkSize + chunkSize + column + j] = 1

    return codedPacket

##
# Executa decodificacao do pacote transmittedPacket, gerando
# novo pacote decodedPacket.
##
def decodePacket(transmittedPacket, row, column):

    ##
    # Argumentos:
    #  - transmittedPacket: pacote apos simulacao da transmissao, potencialmente
    # contendo erros. Cada entrada na lista representa um bit do pacote
    # (inteiro 0 ou 1).
    # Valor de retorno: pacote decodificado no mesmo formato.
    ##
    parityMatrix = [[0 for x in range(column)] for y in range(row)]
    parityColumns = [0 for x in range(column)]
    parityRows = [0 for x in range(row)]
    decodedPacket = [0 for x in range(len(transmittedPacket))]
    
    codedLen = ((row + 1) * (column + 1)) - 1
    chunkSize = row * column

    n = 0 # Contador de bytes no pacote decodificado.

    ##
    # Itera por cada sequencia de (row+1)*(column+1)-1 bits (row*column de dados + resto de paridade).
    ##
    for i in range(0, len(transmittedPacket), codedLen):

        ##
        # Bits do i-esimo conjunto sao dispostos na matriz.
        ##
        for j in range(row):
            for k in range(column):
                temp = transmittedPacket[i + column * j + k]
                parityMatrix[j][k] = temp

        ##
        # Bits de paridade das colunas.
        ##
        for j in range(column):
            parityColumns[j] = transmittedPacket[i + chunkSize + j]

        ##
        # Bits de paridade das linhas.
        ##
        for j in range(row):
            parityRows[j] = transmittedPacket[i + (chunkSize + column) + j]

        ##
        # Verificacao dos bits de paridade: colunas.
        # Note que paramos no primeiro erro, ja que se houver mais
        # erros, o metodo eh incapaz de corrigi-los de qualquer
        # forma.
        ##
        errorInColumn = -1
        for j in range(column):
            sum=0
            for k in range(row):
                sum += parityMatrix[k][j]
            if sum % 2 != parityColumns[j]:
                errorInColumn = j
                break

        ##
        # Verificacao dos bits de paridade: linhas.
        # Note que paramos no primeiro erro, ja que se houver mais
        # erros, o metodo eh incapaz de corrigi-los de qualquer
        # forma.
        ##
        errorInRow = -1
        for k in range(row):
            sum = 0
            for j in range(column):
                sum += parityMatrix[k][j]
            if sum % 2 != parityRows[k]:
                errorInRow = k
                break

        ##
        # Se algum erro foi encontrado, corrigir.
        ##
        if errorInRow > -1 and errorInColumn > -1:

            if parityMatrix[errorInRow][errorInColumn] == 1:
                parityMatrix[errorInRow][errorInColumn] = 0
            else:
                parityMatrix[errorInRow][errorInColumn] = 1

        ##
        # Colocar bits (possivelmente corrigidos) na saida.
        ##
        for j in range(row):
            for k in range(column):
                decodedPacket[chunkSize * n + column * j + k] = parityMatrix[j][k]

        ##
        # Incrementar numero de bytes na saida.
        ##
        n = n + 1

    return decodedPacket

###
##
# Outras funcoes.
##
###

def old_codeHamming(data, ham):
    # TODO: não pegar data dividir ela pra fazer os hammingzinhos
    
    i = 2 # começa no 2 pq os dois primeiros slots sempre serão sempre bits de verificacao
    j = 0 # para iterar no data
    dataSize = len(data)
    codedPacket = [0 for x in range(dataSize - 1)]
    codedPacketChunk = [0 for x in range(ham)]

    for x in range(2, (dataSize - 1)):
        if (x % 2**i != 0):
            codedPacket[x] = data[j]
            j = j + 1
        else:
            i = i + 1
    #
    ###
    # Fazendo os bits de paridade
    ###
    #
    # Hamming (7,4)
    if dataSize == 4:
        codedPacket[0] = codedPacket[0] ^ data[0] ^ data[1] ^ data[3]
        codedPacket[1] = codedPacket[1] ^ data[0] ^ data[2] ^ data[3]
        codedPacket[3] = codedPacket[3] ^ data[1] ^ data[2] ^ data[3]

    # Hamming (12, 8)
    elif dataSize == 8:
        codedPacket[0] = data[0] ^ data[1] ^ data[3] ^ data[4] ^ data[6]
        codedPacket[1] = data[0] ^ data[2] ^ data[3] ^ data[5] ^ data[6]
        codedPacket[3] = data[1] ^ data[2] ^ data[3] ^ data[7]
        codedPacket[7] = data[4] ^ data[5] ^ data[6] ^ data[7]

    # Hamming (21,16)
    elif dataSize == 16:
        codedPacket[0] = codedPacket[0] ^ data[0] ^ data[1] ^ data[3] ^ data[4] ^ data[6] ^ data[8] ^ data[10] ^ data[11] ^ data[13] ^ data[15]
        codedPacket[1] = codedPacket[1] ^ data[0] ^ data[2] ^ data[3] ^ data[5] ^ data[6] ^ data[10] ^ data[12] ^ data[13]
        codedPacket[3] = codedPacket[3] ^ data[1] ^ data[2] ^ data[3] ^ data[7] ^ data[8] ^ data[9] ^ data[10] ^ data[14] ^ data[15]
        codedPacket[7] = codedPacket[7] ^ data[4] ^ data[5] ^ data[6] ^ data[7] ^ data[8] ^ data[9] ^ data[10]
        codedPacket[15] = codedPacket[15] ^ data[11] ^ data[12] ^ data[13] ^ data[14] ^ data[15]
        
    else:
        help(sys.argv[0])

    return codedPacket

def old_decodeHamming(codedPacket, ham):
    return decodedPacket

def codeHamming(data, tamTotal, tamDados):
    #TESTADO EM (7,4), (12,8), (21,16)
    #tamDados = 4
    #tamTotal = 7
    respFinal = []
    for i in range(int(len(data)/tamDados)):
        respParcial = [0 for x in range(tamTotal)]
        c=0

        #preenche o vetor da resposta parcial com os dados do sub array, mas ainda nao mexe nos bits de paridade
        for j in range(1,tamTotal+1):
            if (j != 0) and ((j & (j-1)) == 0):#ve se eh potencia de 2
                continue
            else:
                respParcial[j-1]= data[i*tamDados+c]
                c+=1

        #agora mexe só nos bits de paridade
        for j in range(1,tamTotal+1):
            if (j != 0) and ((j & (j - 1)) == 0):  # ve se eh potencia de 2
                sum =0
                #ve j, pula j, ve j, pula j...
                for k in range(j-1,tamTotal,j*2):
                    for l in range(j):
                        if k+l<tamTotal:
                            sum+=respParcial[k+l]
                if sum%2!=0:
                    respParcial[j-1]=1

        #adiciona a lista de resposta parcial no final da lista de resposta final
        respFinal.extend(respParcial)
    return respFinal

def decodeHamming(data, tamTotal):
    # TESTADO EM (7,4), (12,8), (21,16)
    #tamDados = 4 !!! PROVOU-SE DESNECESSARIO NO DECODE
    #tamTotal = 7
    respFinal = []
    erroEm=0
    for i in range(int(len(data)/tamTotal)):
        vetorParcial = [0 for x in range(tamTotal)]

        #preenche o vetor parcial
        for j in range(tamTotal):
            vetorParcial[j]= data[i*tamTotal+j]


        #agora verifica os bits de paridade
        for j in range(1,tamTotal+1):
            if (j != 0) and ((j & (j - 1)) == 0):  # ve se eh potencia de 2
                sum =0
                #ve j, pula j, ve j, pula j...
                for k in range(j-1,tamTotal,j*2):
                    for l in range(j):
                        if k+l<tamTotal:
                            sum+=vetorParcial[k+l]
                # se a soma dos bits que ele deveria ver, com ele mesmo nao for divisivel por 2, entao esse bit de paridade acusa erro
                if sum%2!=0:
                    erroEm+=j

        #agora tenta corrigir onde acusou o erro
        if erroEm != 0:
            if vetorParcial[erroEm-1]==0:
                vetorParcial[erroEm-1]=1
            else:
                vetorParcial[erroEm-1]=0

        #adiciona a lista de resposta parcial no final da lista de resposta final
        respFinal.extend(vetorParcial)
    return respFinal

##
# Gera conteudo aleatorio no pacote passado como
# parametro. Pacote eh representado por um vetor
# em que cada posicao representa um bit.
# Comprimento do pacote (em bytes) deve ser
# especificado.
##
def generateRandomPacket(l):

    return [random.randint(0,1) for x in range(8 * l)]

##
# Gera um numero pseudo-aleatorio com distribuicao geometrica.
##
def geomRand(p):

    uRand = 0
    while(uRand == 0):
        uRand = random.uniform(0, 1)

    return int(math.log(uRand) / math.log(1 - p))

##
# Insere erros aleatorios no pacote, gerando uma nova versao.
# Cada bit tem seu erro alterado com probabilidade errorProb,
# e de forma independente dos demais bits.
# Retorna o numero de erros inseridos no pacote e o pacote com erros.
##
def insertErrors(codedPacket, errorProb):

    i = -1
    n = 0 # Numero de erros inseridos no pacote.

    ##
    # Copia o conteudo do pacote codificado para o novo pacote.
    ##
    transmittedPacket = list(codedPacket)

    while 1:

        ##
        # Sorteia a proxima posicao em que um erro sera inserido.
        ##
        r = geomRand(errorProb)
        i = i + 1 + r

        if i >= len(transmittedPacket):
            break

        ##
        # Altera o valor do bit.
        ##
        if transmittedPacket[i] == 1:
            transmittedPacket[i] = 0
        else:
            transmittedPacket[i] = 1

        n = n + 1

    return n, transmittedPacket

##
# Conta o numero de bits errados no pacote
# decodificado usando como referencia
# o pacote original. O parametro packetLength especifica o
# tamanho dos dois pacotes em bytes.
##
def countErrors(originalPacket, decodedPacket):

    errors = 0

    for i in range(len(originalPacket)):
        if originalPacket[i] != decodedPacket[i]:
            errors = errors + 1

    return errors

##
# Exibe modo de uso e aborta execucao.
##
def help(selfName):

    sys.stderr.write("Simulador de metodos de FEC/codificacao.\n\n")
    sys.stderr.write("Modo de uso:\n\n")
    sys.stderr.write("\t" + selfName + " <tam_pacote> <reps> <prob. erro> <opcao> <arg1> <arg2>\n\n")
    sys.stderr.write("Onde:\n")
    sys.stderr.write("\t- <tam_pacote>: tamanho do pacote usado nas simulacoes (em bytes).\n")
    sys.stderr.write("\t- <reps>: numero de repeticoes da simulacao.\n")
    sys.stderr.write("\t- <prob. erro>: probabilidade de erro de bits (i.e., probabilidade\n")
    sys.stderr.write("de que um dado bit tenha seu valor alterado pelo canal.)\n\n")
    sys.stderr.write("\t - <opcao>: \"2d\" para paridade bidimensional ou \"hamming\" para hamming\n")
    sys.stderr.write("\t - <arg1>: Paridade bidimensional: Número de LINHAS.\n")
    sys.stderr.write("\t - <arg1>: Hamming: Número de Bits totais do pedaço (Testado com:(7,4), (12,8) ou (21,16)). Digite o primeiro número da tupla.\n")
    sys.stderr.write("\t - <arg2>: Paridade bidimensional: Número de COLUNAS.\n")
    sys.stderr.write("\t - <arg2>: Hamming: Número de Bits de dados do pedaço (Testado com:(7,4), (12,8) ou (21,16)). Digite o ultimo número da tupla.\n")

    sys.exit(1)

##
# Programa principal:
#  - le parametros de entrada;
#  - gera pacote aleatorio;
#  - gera bits de redundancia do pacote
#  - executa o numero pedido de simulacoes:
#      + Introduz erro
#  - imprime estatisticas.
##

##
# Inicializacao de contadores.
##
totalBitErrorCount = 0
totalPacketErrorCount = 0
totalInsertedErrorCount = 0

##
# Leitura dos argumentos de linha de comando.
##
if (len(sys.argv) < 6) or (len(sys.argv) > 7):
    help(sys.argv[0])

packetLength = int(sys.argv[1])
reps = int(sys.argv[2])
errorProb = float(sys.argv[3])
opcao = sys.argv[4].lower()
if (opcao == "2d"):
    row = int(sys.argv[5])
    column = int(sys.argv[6])

elif (opcao == "hamming"):
    tamTotal = int(sys.argv[5])
    tamDados = int(sys.argv[6])

else:
    help(sys.argv[0])

if packetLength <= 0 or reps <= 0 or errorProb < 0 or errorProb > 1:
    help(sys.argv[0])

##
# Inicializacao da semente do gerador de numeros
# pseudo-aleatorios.
##
random.seed()

##
# Geracao do pacote original aleatorio.
##

originalPacket = generateRandomPacket(packetLength)

if(opcao=="2b"):
    codedPacket = codePacket(originalPacket, row, column)
elif (opcao == "hamming"):
    codedPacket = codeHamming(originalPacket,tamTotal,tamDados)

##
# Loop de repeticoes da simulacao.
##
for i in range(reps):

    ##
    # Gerar nova versao do pacote com erros aleatorios.
    ##
    insertedErrorCount, transmittedPacket = insertErrors(codedPacket, errorProb)
    totalInsertedErrorCount = totalInsertedErrorCount + insertedErrorCount

    ##
    # Gerar versao decodificada do pacote.
    ##
    if(opcao=="2b"):
        decodedPacket = decodePacket(transmittedPacket, row, column)
    elif (opcao == "hamming"):
        decodedPacket = decodeHamming(codedPacket,tamTotal)

        ##
    # Contar erros.
    ##
    bitErrorCount = countErrors(originalPacket, decodedPacket)

    if bitErrorCount > 0:

        totalBitErrorCount = totalBitErrorCount + bitErrorCount
        totalPacketErrorCount = totalPacketErrorCount + 1

print ('Numero de transmissoes simuladas: {0:d}\n'.format(reps))
print ('Numero de bits de dados: {0:d}'.format(reps * packetLength * 8))
print ('Numero de bits transmitidos: {0:d}'.format(reps * len(codedPacket)))
print ('Numero de bits errados inseridos: {0:d}\n'.format(totalInsertedErrorCount))
print ('Taxa de erro de bits (antes da decodificacao): {0:.2f}%'.format(float(totalInsertedErrorCount) / float(reps * len(codedPacket)) * 100.0))
print ('Numero de bits corrompidos apos decodificacao: {0:d}'.format(totalBitErrorCount))
print ('Taxa de erro de bits (apos decodificacao): {0:.2f}%\n'.format(float(totalBitErrorCount) / float(reps * packetLength * 8) * 100.0))
print ('Numero de pacotes corrompidos: {0:d}'.format(totalPacketErrorCount))
print ('Taxa de erro de pacotes: {0:.2f}%'.format(float(totalPacketErrorCount) / float(reps) * 100.0))