from src.Process import Process
class Device:
    def __init__(self, id, simultaneous_uses, operation_time):
        self.id = id
        self.simUses = simultaneous_uses
        self.opTime = operation_time
        self.alreadyExec_queue = []
        self.device_queue = []
        self.process_using = []
        self.done = {}
        # É necessário registrar quantas vezes o dispositivo foi acessado
        # É necessário registrar em que momentos ele é finalizado sua execução

    def acess(self, process: Process):
        if len(self.process_using) < self.simUses:
            self.process_using.append(process)
            self.alreadyExec_queue.append(0)
        else:
            self.device_queue.append(process)
        
    
    def is_done(self, process: Process): 
        exec_idx = self.process_using.index(process)
        return True if self.alreadyExec_queue[exec_idx] >= self.opTime else False
    
    def remove_process(self, process):
        idx = self.process_using.index(process)
        self.alreadyExec_queue.pop(idx)
        self.process_using.pop(idx)
    
    def __repr__(self):
        pids = []
        text = ""
        for process in self.process_using:
            pids.append(process.pid)
        for pid in pids:
            text += f"PID:{pid} - EXECUÇÃO: {self.alreadyExec_queue[pids.index(pid)]}/{self.opTime} |"
        return text

    def execute(self, n:int, current_clock: int) -> int:
        
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
        
    
