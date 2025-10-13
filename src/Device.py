from src.Process import Process
class Device:
    def __init__(self, id, simultaneous_uses, operation_time):
        '''
        Essa classe é responsável por simular um dispositivo de entrada e saída de um SO.
        args:
            id: Identificador Único do Dispositivo,
            simultaneous_uses: Número de processos simultâneos que podem usar esse dispositivo,
            operation_time: Tempo em clocks da cpu que leva para realizar a operação
        '''
        self.id = id
        self.simUses = simultaneous_uses
        self.opTime = operation_time

        self.alreadyExec_queue = [] # Lista com tempos de execução para cada Processo
        self.device_queue = []      # Fila para armazenar processos que querem usar o Dispositivo, fila de espera.
        self.process_using = []     # Processos que estão usando o Dispositivo
        self.done = {}              # Lista com o Momento que cada processo acabou de usar o dispositivo, tem que ser revisto pois um processo
                                    # pode usar mais de uma vez um mesmo dispositivo, tornando o dicionário uma estrutura ruim

        # Variáveis para UI
            # É necessário registrar quantas vezes o dispositivo foi acessado
            # É necessário registrar em que momentos ele é finalizado sua execução

    def access(self, process: Process) -> None:
        '''
            Função para acessar o dispositivo. Adiciona o dispositivo a lista de processos usando o dispositivo se não tiver ultrapassado
            o máximo de ussos simultâneos. Caso tenha, entra na fila de espera.
            arg:
                process: Objeto Process que deseja usar o dispositivo
        '''
        print(len(self.process_using), self.simUses)
        if len(self.process_using) < self.simUses:
            self.process_using.append(process)
            self.alreadyExec_queue.append(0)
        else:
            self.device_queue.append(process)
        
    
    def is_done(self, process: Process) -> bool: 
        '''
            Função que verifica se o processo já acabou de usar o dispositivo.
            args:
                process: Processo que já está na lista de processos executando
        '''
        exec_idx = self.process_using.index(process)
        return True if self.alreadyExec_queue[exec_idx] >= self.opTime else False
    
    def remove_process(self, process) -> None:
        '''
            Função que remove um processo das estruturas de controle
            args:
                process: Processo que está na lista de processos executando
        '''
        idx = self.process_using.index(process)
        self.alreadyExec_queue.pop(idx)
        self.process_using.pop(idx)
    
    def __repr__(self):
        '''
            Função que constrói uma representação em texto do objeto Device. Ela é usada na interface gráfica para mostrar o estado do dispositivo
        '''
        pids = []
        queue = []
        text = ""
        for process in self.device_queue:
            queue.append(process.pid)
        for process in self.process_using:
            pids.append(process.pid)
        for pid in pids:
            text += f"PID:{pid} - EXECUÇÃO: {self.alreadyExec_queue[pids.index(pid)]}/{self.opTime} |"
        text += f"Fila: {queue}"
        return text

    def execute(self, n:int, current_clock: int) -> None:
        '''
            Função que executa o Dispositivo.
            args:
                n: tempo que o dispositivo tem no máximo para executar em clocks da cpu
                current_clock: Clock atual da CPU, usado apenas para registrar quando o dispositivo acabou a execução
        '''
        for process in self.process_using[:]:
            print(f"Processo {process.pid} - executando {n} periodos do dispositivo {self.id} - Existem {len(self.process_using)} processos usando o dispositivo")
            print(f"")
            exec_idx = self.process_using.index(process)
            step = n if self.alreadyExec_queue[exec_idx] + n <= self.opTime else self.opTime-self.alreadyExec_queue[exec_idx]
            self.alreadyExec_queue[exec_idx] += step
            if self.is_done(process):
                self.done[process.pid] = current_clock + step
                self.remove_process(process)
                if not self.device_queue and not self.process_using:
                    self.state = "Concluido"
                if self.device_queue:
                    self.process_using.append(self.device_queue.pop(0))
                    self.alreadyExec_queue.append(0)
        
    
