from collections import deque

class Process:                              #Criação do objeto Process
    def __init__(self, beggining: int, pid: int, exectime: int, priority: int , memory: int, sequence_acess_page: str, e_s_chance: float):

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
        self.acess_page_order = list(map(int, sequence_acess_page.split(' '))) if sequence_acess_page else []
        self.next_acess_idx = 0
        self.queue_fifo = deque()

        # VARIÁVEIS DE E/S
        self.ask_es_chance = e_s_chance

    def get_next_page(self):
        page_number = self.acess_page_order[self.next_acess_idx]
        self.next_acess_idx += 1
        return page_number
    def is_done(self):
        return True if self.alreadyexec >= self.exectime else False

    def is_ready(self):
        return True if self.state == "Pronto" else False
    
    def is_blocked(self):
        return True if self.state == "Bloqueado" else False
    
    def is_executing(self):
        return True if self.state == "Executando" else False
    
    def can_start(self, actual_clock):
        if self.beggining <= actual_clock and self.state == "Nao Iniciado":
            ret = True
            self.state = "Pronto"
        else:
            ret = False
        return ret
    
    def execute(self, n:int, current_clock: int, block) -> int:
        step = n if self.alreadyexec + n <= self.exectime else self.exectime-self.alreadyexec
        self.alreadyexec += step
        self.state = "Executando"
        print("Step do processo", self.pid)
        if self.is_done():
            self.done = current_clock + step
            self.state = "Concluido"
        if block:
            self.block()
        return step
        
    def block(self): self.state = "Bloqueado"
    
    def make_ready(self): self.state = "Pronto"
    
    