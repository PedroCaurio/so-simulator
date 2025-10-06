# Simulador de Sistema Operacional

Este é um projeto para a disciplina de Sistemas Operacionais, desenvolvido em Python com a biblioteca PyQt6 para a interface gráfica.

## Sobre o Projeto

O simulador implementa os seguintes conceitos:
- Escalonamento de processos (algoritmo de Alternância Circular).
- Gerenciamento de memória com paginação (política FIFO).
- Simulação de dispositivos de Entrada e Saída.

## Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/PedroCaurio/so-simulator
    ```
2.  **Instale as dependências:**
    ```bash
    pip install PyQt6
    ```
3.  **Execute o gerador de entrada:**
    ```bash
    python geradorEntrada.py
    ```
4.  **Execute o programa principal:**
    ```bash
    python main.py
    ```

## Estrutura de Diretórios

- `/src`: Contém a lógica principal do simulador (Escalonador, Processos, Memória).
- `/UI`: Contém os arquivos da interface gráfica desenvolvida com PyQt6.
- `main.py`: Ponto de entrada da aplicação.

## Possíveis Aprimoramentos

### Interface Gráfica
[ ] - Alterar cores dos processos de acordo com estado

[ ] - Alterar interface dos dispositivos para aumentar a legibilidade

[ ] - Inserir cores nas variáveis de memória para visualizar page hits, substituições e inserções

[ ] - Permitir visualização das Tabeles de Páginas dos processos

[ ] - Permitir visualização da fila de processos que querem acessas um dispositivo

[ ] - Aumentar o tamanho dos widgets para evitar o redimensionamento

### Escalonador
[ ] - Adicionar demais algoritmos de escalonamento

### Memória
[ ] - Adicionar integração com as variáveis de memória máxima

[ ] - Adicionar integração com máximo de alocação por processo

[ ] - Adicionar outras políticas

### Gerador Entrada
[ ] - Verificar variáveis de memória para serem multiplos de 2

### Documentação
[ ] - Escalonador

[ ] - Main

[ ] - Device

[ ] - DeviceManager

[ ] - MemoryManager

[ ] - Process