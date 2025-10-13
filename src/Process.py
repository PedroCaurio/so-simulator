from collections import deque

class Process:                              
    def __init__(self, beggining: int, pid: int, exectime: int, priority: int , memory: int, sequence_access_page: str, e_s_chance: float):
        '''
            Classe que simula um processo
        '''
        # VARIÁVEIS DE PROCESSO
        self.beggining = beggining          # Momento de criação do processo
        self.pid = pid                      # Id do processo
        self.exectime = exectime            # Tempo necessário de execução para concluir o processo
        self.priority = priority            # Prioridade ou número de bilhetes
        self.alreadyexec = 0                # Quantidade de tempo já executada do processo
        self.done = None                    # Variável de controle para definir quando o processo foi concluido
        self.state = "Nao Iniciado"               # "Nao Iniciado", "Pronto", "Executando", "Bloqueado" e "Concluido"
        self.vruntime = None                # Tempo de execução virtual - Utilizado apenas no algoritmo CFS
        self.dynamic_priority = priority    # Usado somente no algoritmo de prioridade

        # VARIÁVEIS DE MEMÓRIA
        self.memory = memory
        self.pages_table = {}               # {num_pag: num_moldura}
        self.access_page_order = list(map(int, sequence_access_page.split(' '))) if sequence_access_page else []
        self.next_access_idx = 0
        self.queue_fifo = deque()

        # VARIÁVEIS DE E/S
        self.ask_es_chance = e_s_chance
    def get_next_page(self):
        '''
            Função que retorna a próxima página que deve ser acessada
        '''
        # ARRUMAR: ESSA FUNÇÃO PODE RETORNAR UM VALOR FORA DO RANGE
        page_number = self.access_page_order[self.next_access_idx]
        self.next_access_idx += 1
        return page_number
    
    #########################
    #   FUNÇÕES DE ESTADO   #
    #########################
    def is_done(self) -> bool:
        '''
            Função que retorna se o processo está concluido
        '''
        return True if self.alreadyexec >= self.exectime else False

    def is_ready(self) -> bool:
        '''
            Função que retorna se o processo está pronto
        '''
        return True if self.state == "Pronto" else False
    
    def is_blocked(self):
        '''
            Função que retorna se o processo está bloqueado
        '''
        return True if self.state == "Bloqueado" else False
    
    def is_executing(self):
        '''
            Função que retorna se o processo está executanto
        '''
        return True if self.state == "Executando" else False
    
    def can_start(self, actual_clock):
        '''
            Função que verifica se o processo pode iniciar de acordo com o actual_clock
        '''
        if self.beggining <= actual_clock and self.state == "Nao Iniciado":
            ret = True
            self.state = "Pronto"
        else:
            ret = False
        return ret
    
    ####################################
    #   FUNÇÕES DE MUDANÇA DE ESTADO   #
    ###################################

    def execute(self, n:int, current_clock: int, block) -> int:
        '''
            Função que simula a execução do processo, alterando para executando, pronto ou bloqueado
        '''
        # Cálculo do quanto deve ser executado
        step = n if self.alreadyexec + n <= self.exectime else self.exectime-self.alreadyexec
        self.alreadyexec += step

        self.state = "Executando"
        if self.is_done():
            self.done = current_clock + step    # Guarda o momento que o processo ficou concluido
            self.state = "Concluido"
        if block:
            self.block()
        return step
    
    # FUNÇÃO QUE BLOQUEIA O PROCESSO
    def block(self): self.state = "Bloqueado"
    
    # FUNÇÃO QUE FAZ O PROCESSO FICAR PRONTO
    def make_ready(self): self.state = "Pronto"
    
    