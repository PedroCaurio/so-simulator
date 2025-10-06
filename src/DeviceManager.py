from src.Device import Device
from src.Process import Process
import random

class DeviceManager:
    def __init__(self):
        self.devices = []
        
    def add_device(self, id: int, simultaneous_uses: int, operation_time: int):
        self.devices.append(Device(id, simultaneous_uses, operation_time))

    def random_device(self):
        if self.devices:
            dev = random.choice(self.devices)
            return dev.id
        return None
    
    def acessing(self): # Retorna os processos que estão vinculados aos dispositivos
        ret = {}
        for dev in self.devices:
            for process in dev.process_using:
                ret[process.pid] = dev.id
        return ret


    def acess_device(self, id: int, process: Process):
        for dev in self.devices:
            if dev.id == id:
                dev.acess(process)
                return True
        return False
    
    def execute_devices(self, n: int, current_clock: int):
        for dev in self.devices:
            dev.execute(n, current_clock)