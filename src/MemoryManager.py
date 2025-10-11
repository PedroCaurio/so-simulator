from collections import deque

class MemoryManager:
    def __init__(self, memory_total, page_frame_size, politic):
        '''
            Classe responsável por fazer o gerenciamento da memória física
        '''

        # POLITICA DE SUBSTITUIÇÃO
        self.scope = politic
        self.queue_fifo_global = deque()
        self.politic = "FIFO"
        
        # VARIÁVEIS DE MEMÓRIA
        self.memory = int(memory_total)
        self.page_frame_size = int(page_frame_size)
        self.num_frames = self.memory // self.page_frame_size
        self.frames = [None] * self.num_frames

        

    
    def page_alloc(self, process, page_number) -> bool:
        '''
            Função principal que faz alocação da página de um processo para uma moldura.
        '''
        # CASO 1: PÁGINA ESTÁ EM UMA MOLDURA - HIT PAGE
        page = (process.pid, page_number)
        if page in self.frames:
            return True

        # CASO 2: PÁGINA NÃO ESTÁ NA MOLDURA 
        # CASO 2.1: EXISTE ESPAÇO VAZIO EM UMA MOLDURA
        if None in self.frames:
            free_frame_idx = self.frames.index(None)
            self.frames[free_frame_idx] = page
            process.pages_table[page_number] = free_frame_idx

            # Inserir na fila do FIFO ou de outros dados dos algoritmos de substituição
            if self.politic == 'FIFO':
                if self.scope == "Global":
                    self.queue_fifo_global.append(page)
                elif self.scope == "Local":
                    process.queue_fifo.append(page)
            return True
        # CASO 2.2: SUBSTITUIÇÃO DE PÁGINA (LOCAL E GLOBAL)
        # Chamar a Política para realizar a substituição
        return getattr(self, self.politic)(process, page)
        
    def FIFO(self, process, page) -> bool:
        '''
            Algoritmo de substituição de página First-in First-out. Escolhe a página que será substituida baseado nos deques
            do memory manager, se for global, ou dos processos, se for local.
        '''
        if self.scope == "Global" and self.queue_fifo_global:
            page_to_remove = self.queue_fifo_global.popleft()
            frame_idx = self.frames.index(page_to_remove)
            self.frames[frame_idx] = page
            # Aloca a nova página no lugar da antiga
            self.queue_fifo_global.append(page)
            process.pages_table[page[1]] = frame_idx
            return True
        elif self.scope == "Local" and process.queue_fifo:
            page_to_remove = process.queue_fifo.popleft()
            frame_idx = self.frames.index(page_to_remove)
            self.frames[frame_idx] = page

            process.queue_fifo.append(page)
            process.pages_table[page[1]] = frame_idx
            return True
        return False
        