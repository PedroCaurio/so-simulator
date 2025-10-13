import random

if __name__ == "__main__":

    print("Bem-vindo ao gerador de arquivos de entrada para o escalonador!")
    print("Escolha o algoritmo: 1: alternancia circular, 2: prioridade, 3: loteria, 4: CFS")
    alg = int(input())
    print("Informe a fracao de CPU que cada processo tera direito por vez")
    clock = int(input())
    print("Informe o numero de processos a serem criados")
    numProcessos = int(input())
    print("Informe a Política de Memória (Local ou Global)")
    politica = input()
    if politica not in ["Local", "Global"]:
        raise ValueError
    print("Informe o tamanho da memória principal em bytes")
    tamMemPrincipal = int(input())
    if tamMemPrincipal & 1 != 0:
        raise ValueError
    print("Informe o tamanho das páginas/molduras")
    tamPagMold = int(input())
    if tamPagMold & 1 != 0:
        raise ValueError
    print("Informe o percentual máximo de alocação de memória dos processos")
    alocMem = int(input())
    print("Informe o número de dispositivos de E/S")
    numDispositivosES = int(input())

    if alg == 1:
        A = "alternanciaCircular" 
    elif alg == 2:
        A = "prioridade"
    elif alg == 3:
        A = "loteria"
    elif alg == 4:
        A = "CFS"
    else:
        print("O algoritmo informado nao existe")
        exit()

    out = open("entradaEscalonador.txt", 'w')

    out.write(A+"|"+str(clock)+"|"+politica+"|"+str(tamMemPrincipal)+"|"+str(tamPagMold)+"|"+str(alocMem)+"|"+str(numDispositivosES)+"\n")

    for disp in range (0, numDispositivosES):
        numUsosSimultaneos = random.randint(1, 3)
        tempoOperacao = random.randint(1, 10)*clock
        out.write(str(disp)+"|"+str(numUsosSimultaneos)+"|"+str(tempoOperacao)+"\n")

    for i in range (0, numProcessos):
        tempo = random.randrange(1,10)*clock
        prioridade = random.randrange(1, 100)
        memoriaNecessaria = random.choice([2048, 4096])
        numPags = memoriaNecessaria // tamPagMold
        seqAcessoPags = ""
        for n in range(3, 10):
            if n < 9:
                spc = " "
            else:
                spc = ""
            seqAcessoPags += str(random.randint(1, numPags))+spc
        out.write(str(i)+"|"+str(i)+"|"+str(tempo)+"|"+str(prioridade)+"|"+str(memoriaNecessaria)+"|"+seqAcessoPags+"|"+str(random.random())+"\n")

    out.close()