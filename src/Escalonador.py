from src.DeviceManager import DeviceManager
from src.MemoryManager import MemoryManager
from src.Process import Process
import random
from collections import deque


class Escalonador:                  #Criação do objeto Escalonador
    def __init__(self, infos):      
        '''
            Classe principal do Simulador, o escalonador instancia os gerenciadores de memória e de dispositivos
            além de fazer todo controle dos processos
        '''
        self.infos = list(infos)    # Lista de informações brutas
        self.alg = None             # Algoritmo selecionado pelo usuário
        self.frac = None            # Fração da CPU que cada processo terá controle 
        self.clock = 0              # Clock atual
        self.processes  = []
        self.ready = []

        # Alternância Circular
        self.last_process = None
        self.already_executed_processes = []
        self.round_robin_queue = deque()

        self.DevManager = DeviceManager()

    def initialize(self): 
        '''
            Função que lê o arquivo de entrada e cria todos Objetos Processos e Dispositivos com suas devidas informações. Além de criar o MemoryManager
        '''
        self.alg, self.frac,self.politic, self.memSize, self.framePageSize, self.alocPerc, self.numDevices = self.infos[0].split("|") 
        self.numDevices = int(self.numDevices)
        self.frac = int(self.frac)
        self.infos.pop(0) #Remove a primeira linha das informações
        self.tempoex = [] # Cria uma lista vazia para armazenar o tempo que cada processo precisa na CPU
        self.memManager = MemoryManager(self.memSize, self.framePageSize, self.politic)
        # CRIAÇÃO DOS DISPOSITIVOS
        for dev in range(self.numDevices):
            disp_id, numUsosSimul, tempoOper = self.infos[dev].split("|")
            self.DevManager.add_device(int(disp_id), int(numUsosSimul), int(tempoOper))
        
        # CRIAÇÃO DOS PROCESSOS
        for i in range(self.numDevices, len(self.infos)): #Itera sobre cada processo da entrada
            beg, pid, tempoEx, prioridade, qtdMem, seqAcessPag, askES = self.infos[i].split("|") #Separa as informações do processo em uma lista

            newprocess = Process(int(beg), int(pid), int(tempoEx), int(prioridade), int(qtdMem), seqAcessPag, float(askES)) #Cria uma variável newprocess da classe Process e utiliza as informações da entrada
            self.processes.append(newprocess) #Isere o novo processo na lista de processos do escalonador

            self.tempoex.append(newprocess.exectime) # Insere o tempo de execução desse novo Processo na lista tempo de execução

    def step_forward(self): # Baseado no quantum do sistema
        '''
            Função principal do Escalonador, executa um passo para frente. O máximo que um passo pode ter de tamanho de clock é a
            fração de cpu, porém ele pode executar menos caso o processo se bloqueie.
        '''
        # Atualizar processos prontos e bloqueados
        self.update_processes()
        

        self.actual_process = self.alternanciaCircular()
        
        
        if self.actual_process:
            # Execução do Processos
            
            time_to_exec = self.frac
            block = False
            # Verificar se o processo irá pedir E/S
            if random.random() < self.actual_process.ask_es_chance:
                time_to_exec = random.randint(0, self.frac) # Momento da fração que pedira, ao fim dela o dispositivo será acessado
                block = True
                
                
            # Executa todos dispositvos que estão em uso
            self.DevManager.execute_devices(time_to_exec, self.clock)

            if block:   # Se teve uma chamada de E/S do processo faz o acesso a um dispositivo aleatório
                dev_id = self.DevManager.random_device() # Retorna o id de um objeto Device aleatório
                self.DevManager.acess_device(dev_id, self.actual_process)


            # Acessar a próxima página do processo
            if time_to_exec > 0 and self.actual_process.next_acess_idx < len(self.actual_process.acess_page_order):
                self.memManager.page_alloc(self.actual_process, self.actual_process.get_next_page())

        
            # Executar o Processo adicionando tempo de Execução
        
            clock =+ self.actual_process.execute(time_to_exec, self.clock, block) # A função execute retorna o tempo que o processo executou
            self.clock += clock

            
        elif self.are_processes_remaining(): # Caso não tenha processos prontos mas tenha processos bloqueados
            self.DevManager.execute_devices(1, self.clock)
            self.clock += 1
        else:
            print("Todos processos finalizados, nada para executar")




    def alternanciaCircular(self) -> Process: 
        '''
            Algoritmos de escalonamento Alternancia Circular. Executa o primeiro da fila e coloca ele no final da fila.
        '''

        # Verifica os processos que estão prontos e não estão na fila
        for process in self.processes:
            if process.is_ready() and process not in self.round_robin_queue:
                self.round_robin_queue.append(process)

        # Torna o último processo que estava executando em Pronto, se ele não estiver bloqueado
        if self.last_process and self.last_process.is_executing():
            self.last_process.make_ready()

        # Seleciona o primeiro processo da fila para ser executado 
        if self.round_robin_queue:
            process_to_be_executed = self.round_robin_queue.popleft()
            self.last_process = process_to_be_executed
            return process_to_be_executed
        return None

        
    def are_processes_remaining(self) -> bool:
        '''
            Função que verifica se ainda tem algum processo que não está concluído
        '''
        for process in self.processes:
            if not process.is_done():
                return True
        return False

    def update_processes(self):
        '''
            Atualiza os processos que estão bloqueados ou que não foram iniciados ainda
        '''
        self.ready = []
        for process in self.processes:
            if process.is_ready() or process.can_start(self.clock):
                self.ready.append(process)
            elif process.is_blocked():
                process_device_dict = self.DevManager.acessing() #{process_pid : dev.id}
                if process.pid not in process_device_dict:
                    process.make_ready()
