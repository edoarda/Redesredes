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
    # TODO: entender a logica, os todos embaixo
    # Argumentos:
    #  - originalPacket: pacote original a ser codificado na forma de uma lista.
    #  - row: qtd de linhas na matriz de paridade
    #  - column: qtd de colunas na matriz de paridade
    # Cada entrada na lista representa um bit do pacote (inteiro 0 ou 1).
    # Valor de retorno: pacote codificado no mesmo formato.
    ##
    parityMatrix = [[0 for x in range(row)] for y in range(column)]
    codedLen = ((row + 1) * (column + 1)) - 1
    codedPacket = [0 for x in range(codedLen)]
    # vai precisar disso bastante, por isso tá pré-computado
    chunkSize = row * column
    originalPacketLength = len(originalPacket)
    ##
    # Itera por cada byte do pacote original.
    ##
    for i in range(originalPacketLength / chunkSize):

        ##
        # Bits do i-esimo byte sao dispostos na matriz.
        # TODO: ENTENDER ESSA LOGICA DO ORIGINAL PACKET LÁ
        ##
        for j in range(row):
            for k in range(column):
                parityMatrix[j][k] = originalPacket[i * 8 + 4 * j + k]

        ##
        # Replicacao dos bits de dados no pacote codificado.
        ##
        for j in range(chunkSize):
            codedPacket[i * codedLen + j] = originalPacket[i * chunkSize + j]

        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das colunas.
        ##
        for j in range(column):
            if (parityMatrix[0][j] + parityMatrix[1][j]) % 2 == 0:
                codedPacket[i * codedLen + chunkSize + j] = 0
            else:
                codedPacket[i * codedLen + chunkSize + j] = 1

        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das linhas.
        # TODO: ENTENDER A LÓGICA DO 12
        ##
        for j in range(row):
            if (parityMatrix[j][0] + parityMatrix[j][1] + parityMatrix[j][2] + parityMatrix[j][3]) % 2 == 0:
                codedPacket[i * codedLen + 12 + j] = 0
            else:
                codedPacket[i * codedLen + 12 + j] = 1

    return codedPacket

##
# Executa decodificacao do pacote transmittedPacket, gerando
# novo pacote decodedPacket.
##
def decodePacket(transmittedPacket, row, column):

    ##
    # TODO: completar!
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
                parityMatrix[j][k] = transmittedPacket[i + column * j + k]

        ##
        # Bits de paridade das colunas.
        ##
        for j in range(column):
            parityColumns[j] = transmittedPacket[i + chunkSize + j]

        ##
        # Bits de paridade das linhas.
        # TODO: O MALDITO DOZE
        ##
        for j in range(row):
            parityRows[j] = transmittedPacket[i + 12 + j]

        ##
        # Verificacao dos bits de paridade: colunas.
        # Note que paramos no primeiro erro, ja que se houver mais
        # erros, o metodo eh incapaz de corrigi-los de qualquer
        # forma.
        ##
        errorInColumn = -1
        for j in range(column):
            if (parityMatrix[0][j] + parityMatrix[1][j]) % 2 != parityColumns[j]:
                errorInColumn = j
                break

        ##
        # Verificacao dos bits de paridade: linhas.
        # Note que paramos no primeiro erro, ja que se houver mais
        # erros, o metodo eh incapaz de corrigi-los de qualquer
        # forma.
        ##
        errorInRow = -1
        for j in range(row):

            if (parityMatrix[j][0] + parityMatrix[j][1] + parityMatrix[j][2] + parityMatrix[j][3]) % 2 != parityRows[j]:
                errorInRow = j
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
    sys.stderr.write("\t" + selfName + " <tam_pacote> <reps> <prob. erro>\n\n")
    sys.stderr.write("Onde:\n")
    sys.stderr.write("\t- <tam_pacote>: tamanho do pacote usado nas simulacoes (em bytes).\n")
    sys.stderr.write("\t- <reps>: numero de repeticoes da simulacao.\n")
    sys.stderr.write("\t- <prob. erro>: probabilidade de erro de bits (i.e., probabilidade\n")
    sys.stderr.write("de que um dado bit tenha seu valor alterado pelo canal.)\n\n")

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
if len(sys.argv) != 4:
    help(sys.argv[0])

packetLength = int(sys.argv[1])
reps = int(sys.argv[2])
errorProb = float(sys.argv[3])
row = int(sys.argv[4])
column = int(sys.argv[5])

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
codedPacket = codePacket(originalPacket, row, column)

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
    decodedPacket = decodePacket(transmittedPacket, row, column)

    ##
    # Contar erros.
    ##
    bitErrorCount = countErrors(originalPacket, decodedPacket)

    if bitErrorCount > 0:

        totalBitErrorCount = totalBitErrorCount + bitErrorCount
        totalPacketErrorCount = totalPacketErrorCount + 1

print ('Numero de transmissoes simuladas: {0:d}\n'.format(reps))
print ('Numero de bits transmitidos: {0:d}'.format(reps * packetLength * 8))
print ('Numero de bits errados inseridos: {0:d}\n'.format(totalInsertedErrorCount))
print ('Taxa de erro de bits (antes da decodificacao): {0:.2f}%'.format(float(totalInsertedErrorCount) / float(reps * len(codedPacket)) * 100.0))
print ('Numero de bits corrompidos apos decodificacao: {0:d}'.format(totalBitErrorCount))
print ('Taxa de erro de bits (apos decodificacao): {0:.2f}%\n'.format(float(totalBitErrorCount) / float(reps * packetLength * 8) * 100.0))
print ('Numero de pacotes corrompidos: {0:d}'.format(totalPacketErrorCount))
print ('Taxa de erro de pacotes: {0:.2f}%'.format(float(totalPacketErrorCount) / float(reps) * 100.0))