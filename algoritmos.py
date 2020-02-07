import sys

INFINITO = float('inf')

def lerArquivo(file):
 #Lendo arquivo e removendo vírgulas
    arquivo  = open(file,'r')
    matriz = []

    for linha in arquivo:
        linha = linha.strip()
        linha = linha.split(',')
        linha = [int(x) for x in linha]
        matriz.append(linha)

    return matriz

#Função auxiliar do djikstra/prim que verifica a existência de vértices abertos
def existeAberto (abertos):
    numVertices = len(abertos)

    for i in range(numVertices):
        if (abertos[i]):
            return True

    return False

#Função auxiliar do djikstra/prim que verifica a menor distância até o momento de vértices abertos
def menorEstimativa(distancias, abertos):
    menor = INFINITO
    numVertices = len(distancias)
    index = 0

    for i in range(numVertices):
        if (abertos[i]):
            if (distancias[i] <= menor):
                menor = distancias[i]
                index = i 
    
    return index

#Algoritmo de Djikstra
def djikstra(file,origem):
    matriz = lerArquivo(file)
    numVertices = len(matriz[0])
    origem = origem - 1

    abertos = []
    distancias = []

    #Inicializando as listas de distâncias de verificação de vértices abertos/fechados
    for i in range(numVertices):
        abertos.append (True)
        distancias.append(INFINITO)

    distancias[origem] = 0        

    while(existeAberto(abertos)):
        #Calculando menor distância de vértice aberto
        menorE = menorEstimativa(distancias,abertos)

        #Fechando o vértice encontrado
        abertos[menorE] = False

        #Verificando se tem acesso ao vértice
        if(distancias[menorE] != INFINITO):
            #Relaxamento das arestas
            for i in range(numVertices):
                peso = matriz[menorE][i]
                if (abertos[i]):
                    if (peso != 0):
                        if (distancias[menorE]+peso < distancias[i]):
                            distancias[i] = distancias[menorE]+peso
    
    distancias[origem] = INFINITO  
      
    return distancias

#Algoritmo de Bellman-Ford
def bellmanFord(file,origem):
    matriz = lerArquivo(file)
    numVertices = len(matriz[0])
    origem = origem - 1

    distancias = []

    #Inicializando lista de distâncias
    for i in range(numVertices):
        distancias.append(INFINITO)
    
    distancias[origem] = 0    

    #Relaxamento das arestas 
    for x in range(numVertices-1):
        #Verificando todas as arestas
        for y in range(numVertices):
            #Verificando se é um vértice já acessado
            if (distancias[y]!=INFINITO):
                for i in range(numVertices):
                    peso = matriz[y][i]
                    if (peso != 0):
                        if (distancias[y]+peso < distancias[i]):
                            distancias[i] = distancias[y]+peso
    
    distancias[origem] = INFINITO

    return distancias

#Algoritmo de Prim
def prim(file):
    matriz = lerArquivo(file)
    numVertices = len(matriz[0])
    
    abertos = []
    pesos = []
    antecessores = []

    #Inicializando as listas de pesos, antecessores e de verificação de vértices abertos/fechados
    for i in range(numVertices):
        abertos.append (True)
        pesos.append(INFINITO)
        antecessores.append(-1)

    pesos[0] = 0 
    antecessores[0] = 0

    while(existeAberto(abertos)):
        #Calculando menor peso de vértice aberto
        menorE = menorEstimativa(pesos,abertos)

        #Fechando o vértice encontrado
        abertos[menorE] = False

        #Salvando os menores pesos e os vértices de origem
        for i in range(numVertices):
            peso = matriz[menorE][i]
            if (abertos[i]):
                if (peso != 0):
                    if (peso < pesos[i]):
                        pesos[i] = peso  
                        antecessores[i] = menorE

        #Gerando matriz da árvore geradora
        arvore = []

        for x in range(numVertices):
            arvore.append(0)
            linhas = []
            for y in range(numVertices):
                linhas.append(0)
            arvore[x] = linhas

        for x in range(numVertices):
            i = x
            j = antecessores[x]
            arvore[i][j] = pesos[x]
            arvore[j][i] = pesos[x]

    return arvore

#Algoritmo de Kruskal
def kruskal(file):
    matriz = lerArquivo(file)
    numVertices = len(matriz[0])

    #Inicializando listas de arestas
    arestas = []
    arvore = []

    #Adicionando as arestas na lista
    for x in range(numVertices):
        for y in range(numVertices):
            valor = matriz[x][y]
            if (valor != 0):
                arestas.append((x,y,valor))
                #Apagando valor simétrico
                matriz[y][x] = 0

    #Ordenando a lista pelo peso da aresta
    arestas = sorted(arestas, key = lambda aresta: aresta[2])

    #Inicializando a floresta com a primeira aresta
    floresta = [{arestas[0][0],arestas[0][1]}]
    arvore.append(arestas[0])

    for x in range(1,len(arestas)):
        v1 = {arestas[x][0]}
        v2 = {arestas[x][1]}
        index = -1
        for y in range(len(floresta)):
            #Verificando se os dois vértices estão no mesmo conjunto
            if v1.issubset(floresta[y]) and v2.issubset(floresta[y]):
                index = -2
                break
            #Verificando se um dos vértices estão em algum conjunto
            if v1.issubset(floresta[y]):
                if (index == -1):
                    index = y
                else:
                    #Unindo os conjuntos dos vértices encontrados
                    floresta[index].update(floresta[y])
                    del floresta[y]
                    arvore.append(arestas[x])
                    index = -2
                    break
            if v2.issubset(floresta[y]):
                if (index == -1):
                    index = y
                else:
                    #Unindo os conjuntos dos vértices encontrados
                    floresta[index].update(floresta[y])
                    del floresta[y]
                    arvore.append(arestas[x])
                    index = -2
                    break
                    
        #Adicionando vértices não encontrados aos conjuntos
        if (index == -1):
            floresta.append({arestas[x][0],arestas[x][1]})
            arvore.append(arestas[x])
        #Unindo os conjuntos quando um dos vértices foram encontrados
        elif (index != -2):
            floresta[index].update(v1)
            floresta[index].update(v2)
            arvore.append(arestas[x])

    #Gerando matriz da árvore geradora
    arvoreG = []

    #Inicializando matriz
    for x in range(numVertices):
        arvoreG.append(0)
        linhas = []
        for y in range(numVertices):
            linhas.append(0)
        arvoreG[x] = linhas

    #Setando os pesos nas arestas
    for x in arvore:
        i = x[0]
        j = x[1]
        k = x[2]
        arvoreG[i][j] = k
        arvoreG[j][i] = k

    return arvoreG
