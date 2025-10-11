from src.Device import Device
from src.Process import Process
import random

class DeviceManager:
    def __init__(self):
        '''
            Essa classe faz o controle dos dispositivos, seus acessos e execuções
        '''
        self.devices = []
        
    def add_device(self, id: int, simultaneous_uses: int, operation_time: int) -> None:
        '''
            Adiciona o dispositivo a Lista de dispositivos
        '''
        self.devices.append(Device(id, simultaneous_uses, operation_time))

    def random_device(self) -> int:
        '''
            Seleciona um dispositivo aleatório e retorna seu ID
        '''
        if self.devices:
            dev = random.choice(self.devices)
            return dev.id
        return None
    
    def acessing(self) -> dict: 
        '''
            Função que associa os processos com os dispositivos que estão sendo usados. Retornando um dicionário com pares {pid, id}.
        '''
        ret = {}
        for dev in self.devices:
            for process in dev.process_using:
                ret[process.pid] = dev.id
        return ret


    def acess_device(self, id: int, process: Process) -> bool:
        '''
            Acessa o dispositivo associado com o 'id'
        '''
        for dev in self.devices:
            if dev.id == id:
                dev.acess(process)
                return True
        return False
    
    def execute_devices(self, n: int, current_clock: int):
        '''
            Executa todos os dispositivos um valor 'n'
        '''
        for dev in self.devices:
            dev.execute(n, current_clock)