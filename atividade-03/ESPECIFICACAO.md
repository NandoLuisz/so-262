# 1. Visão Geral e Arquitetura do Simulador

## 1.1 Visão Geral

O projeto consiste no desenvolvimento de um **simulador de gerenciamento de processos** capaz de representar, em modo usuário, o funcionamento simplificado de um núcleo de sistema operacional.

O simulador **não deverá controlar, criar ou gerenciar processos reais do sistema operacional hospedeiro**. Todos os processos, estados, operações de CPU, operações de entrada e saída (E/S), escalonamento e mudanças de contexto deverão ocorrer exclusivamente dentro do ambiente virtual do simulador.

O simulador deverá representar, no mínimo, os seguintes conceitos:

- criação e gerenciamento de processos;
- estados de processos;
- execução de processos;
- escalonamento da CPU;
- operações de entrada e saída (E/S);
- mudança de contexto;
- contador de programa (PC);
- registradores virtuais;
- relógio lógico;
- utilização da CPU;
- tempos de espera e execução dos processos.

O objetivo é permitir a observação do comportamento de um sistema operacional simplificado durante a execução de diferentes processos, possibilitando analisar como a CPU é utilizada e como os processos são selecionados, executados, bloqueados e alternados ao longo do tempo.

O simulador deverá possuir **uma única CPU virtual**. Dessa forma, somente um processo poderá estar no estado **RUNNING** em cada instante da simulação.

---

## 1.2 Arquitetura do Simulador

A arquitetura do simulador deverá ser composta pelos seguintes elementos principais:

- **CPU Virtual**;
- **Registradores Virtuais**;
- **Contador de Programa (PC)**;
- **Relógio Lógico**;
- **Processos**;
- **Gerenciador de Processos**;
- **Escalonador de CPU**;
- **Filas de Processos**;
- **Gerenciador de Eventos de E/S**.

A estrutura geral poderá ser representada da seguinte forma:

```text
┌──────────────────────────────────────────────────┐
│                  SIMULADOR                       │
│                                                  │
│  ┌────────────────────────────────────────────┐  │
│  │             GERENCIADOR                    │  │
│  │           DE PROCESSOS                     │  │
│  │                                            │  │
│  │  ┌──────────────┐   ┌─────────────────┐  │  │
│  │  │   Processos  │   │ Filas de        │  │  │
│  │  │              │   │ Processos       │  │  │
│  │  └──────────────┘   └─────────────────┘  │  │
│  └────────────────────────────────────────────┘  │
│                       │                          │
│                       ▼                          │
│  ┌────────────────────────────────────────────┐  │
│  │             ESCALONADOR DE CPU             │  │
│  └──────────────────────┬─────────────────────┘  │
│                         │                        │
│                         ▼                        │
│  ┌────────────────────────────────────────────┐  │
│  │               CPU VIRTUAL                  │  │
│  │                                            │  │
│  │  ┌──────────────┐   ┌─────────────────┐  │  │
│  │  │ Registradores│   │       PC        │  │  │
│  │  │   Virtuais   │   │ Contador de     │  │  │
│  │  │              │   │    Programa     │  │  │
│  │  └──────────────┘   └─────────────────┘  │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  ┌────────────────────────────────────────────┐  │
│  │              RELÓGIO LÓGICO               │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  ┌────────────────────────────────────────────┐  │
│  │          GERENCIADOR DE EVENTOS           │  │
│  │                DE E/S                     │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 1.2.1 CPU Virtual

A **CPU Virtual** deverá representar o processador utilizado pelo simulador.

Ela será responsável por:

- executar as operações do processo atualmente selecionado;
- manter o processo atualmente em execução;
- atualizar o contador de programa;
- atualizar os registradores virtuais do processo;
- contabilizar o tempo de CPU utilizado;
- detectar eventos relacionados à execução do processo;
- liberar a CPU quando o processo terminar, bloquear-se ou sofrer preempção.

Como o simulador possuirá uma única CPU virtual, deverá existir no máximo **um processo no estado RUNNING por vez**.

A CPU virtual não deverá executar instruções reais do processador ou processos reais do sistema operacional. A execução deverá ocorrer exclusivamente por meio das operações definidas pelo simulador.

---

## 1.2.2 Registradores Virtuais

Cada processo deverá possuir um conjunto de **registradores virtuais**, utilizados para representar o contexto de execução do processo.

Os registradores deverão armazenar valores inteiros e deverão fazer parte do contexto do processo.

Durante uma mudança de contexto, os valores dos registradores do processo que está deixando a CPU deverão ser preservados.

Quando outro processo for colocado em execução, seus registradores deverão ser restaurados para os valores armazenados anteriormente.

A estrutura conceitual deverá ser:

```text
Processo
 ├── Estado
 ├── PC
 ├── Registradores
 ├── Tempo de CPU
 └── Informações da tarefa
```

A quantidade e os nomes dos registradores deverão ser definidos pela especificação da implementação do processo.

---

## 1.2.3 Contador de Programa (PC)

O **Program Counter (PC)** deverá representar a posição da próxima operação da tarefa que será executada pelo processo.

O PC deverá ser um valor inteiro que represente o índice da próxima operação na sequência de execução do processo.

Por exemplo:

```text
Tarefa:

[CPU 5] → [CPU 3] → [E/S 4] → [CPU 2]

PC = 0
       ↓
    CPU 5
```

Após a conclusão da primeira operação:

```text
PC = 1
       ↓
    CPU 3
```

Durante uma mudança de contexto, o valor do PC deverá ser preservado juntamente com os demais dados do contexto do processo.

Quando o processo voltar a executar, ele deverá continuar a partir da operação indicada pelo PC.

---

## 1.2.4 Relógio Lógico

O simulador deverá possuir um **relógio lógico** responsável por representar a passagem do tempo dentro do ambiente simulado.

O tempo da simulação deverá ser representado por unidades inteiras denominadas **ticks**.

O relógio deverá iniciar em:

```text
tempo = 0
```

A cada avanço de um tick, o simulador deverá atualizar os eventos que dependem da passagem do tempo.

O relógio lógico deverá ser utilizado para controlar, no mínimo:

- duração das operações de CPU;
- duração do quantum;
- duração das operações de E/S;
- conclusão de operações de E/S;
- tempo de espera dos processos;
- tempo total de execução da simulação.

O relógio lógico não deverá depender do tempo real de execução do computador hospedeiro.

Por exemplo, uma operação:

```text
CPU 5
```

deverá consumir cinco unidades de tempo simulado, independentemente de quanto tempo o computador real levar para executar o código correspondente.

---

## 1.2.5 Processos

Cada tarefa carregada pelo simulador deverá resultar na criação de um processo virtual.

Cada processo deverá possuir, no mínimo:

- identificador único (**PID**);
- estado atual;
- contador de programa (**PC**);
- registradores virtuais;
- sequência de operações da tarefa;
- tempo de CPU utilizado;
- tempo de criação;
- tempo de conclusão, quando aplicável.

Os processos deverão ser identificados por um PID único durante toda a execução da simulação.

Os estados possíveis dos processos deverão ser definidos pelo modelo de estados especificado na seção de gerenciamento de processos.

---

## 1.2.6 Filas de Processos

O simulador deverá manter estruturas de fila para organizar os processos de acordo com seu estado.

No mínimo, deverão existir:

```text
Fila READY
Fila BLOCKED
```

A fila **READY** deverá conter processos que estão aptos a utilizar a CPU, mas aguardam sua seleção pelo escalonador.

A estrutura utilizada para a fila READY deverá ser compatível com o algoritmo de escalonamento selecionado.

A fila **BLOCKED** deverá representar processos que estão aguardando a conclusão de uma operação de E/S.

Os processos no estado **TERMINATED** não deverão permanecer nas filas de processos prontos ou bloqueados.

---

## 1.2.7 Escalonador de CPU

O **Escalonador de CPU** deverá ser responsável por selecionar o próximo processo que utilizará a CPU virtual.

O simulador deverá permitir a utilização de diferentes algoritmos de escalonamento de forma intercambiável.

O algoritmo de escalonamento deverá receber os processos que estão no estado **READY** e determinar qual deles será colocado em execução.

Os algoritmos de escalonamento suportados e suas regras específicas serão definidos na seção **4. Especificação do Escalonador de CPU**.

---

## 1.2.8 Gerenciador de Eventos de E/S

O simulador deverá possuir um mecanismo responsável por controlar as operações de entrada e saída dos processos.

Quando um processo em execução solicitar uma operação de E/S:

1. a execução do processo deverá ser interrompida;
2. o processo deverá passar para o estado **BLOCKED**;
3. o processo deverá ser removido da CPU virtual;
4. deverá ser registrado o instante previsto para conclusão da E/S;
5. o escalonador deverá selecionar outro processo READY, caso exista.

Quando o tempo previsto para conclusão da E/S for atingido:

1. o processo deverá deixar o estado **BLOCKED**;
2. o processo deverá retornar ao estado **READY**;
3. o processo deverá ser inserido novamente na estrutura de processos prontos;
4. o escalonador deverá considerar o processo em suas próximas seleções.

---

## 1.3 Fluxo Geral de Execução

O funcionamento do simulador deverá ser baseado em um ciclo de execução orientado pelo relógio lógico.

O fluxo geral deverá ocorrer da seguinte maneira:

1. O simulador deverá iniciar com o relógio lógico em `0`.
2. O simulador deverá realizar a leitura do arquivo de tarefas.
3. Cada tarefa deverá ser convertida em um processo virtual.
4. Os processos deverão ser inicializados no estado **READY**.
5. O escalonador deverá selecionar um processo READY.
6. O processo selecionado deverá passar para o estado **RUNNING**.
7. O contexto do processo deverá ser carregado na CPU virtual.
8. A CPU virtual deverá executar a operação indicada pelo PC.
9. O relógio lógico deverá avançar de acordo com a duração da operação.
10. O simulador deverá verificar os eventos que ocorreram durante a execução.
11. Caso ocorra uma operação de E/S, o processo deverá passar para **BLOCKED**.
12. Caso ocorra uma preempção causada pelo escalonador, o processo deverá retornar para **READY**.
13. Caso o processo conclua todas as suas operações, deverá passar para **TERMINATED**.
14. Quando necessário, deverá ocorrer uma mudança de contexto.
15. O escalonador deverá selecionar o próximo processo READY.
16. O ciclo deverá continuar até que todos os processos estejam no estado **TERMINATED** e não existam eventos de E/S pendentes.

O fluxo simplificado será:

```text
                         INÍCIO
                            │
                            ▼
                  Leitura das tarefas
                            │
                            ▼
                   Criação dos processos
                            │
                            ▼
                         READY
                            │
                            ▼
                      Escalonador
                            │
                            ▼
                        RUNNING
                            │
                            ▼
                    Execução na CPU
                            │
                            ▼
                  ┌───────────────────┐
                  │   Evento ocorreu? │
                  └─────────┬─────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
            E/S          Quantum        Término
             │              │              │
             ▼              ▼              ▼
         BLOCKED          READY       TERMINATED
             │              ▲
             │              │
             ▼              │
       E/S concluída        │
             │              │
             ▼              │
           READY ────────────┘
             │
             ▼
        Escalonador
             │
             ▼
      Próximo processo
             │
             ▼
         RUNNING
             │
             ▼
          Execução
             │
             ▼
            ...
             │
             ▼
     Todos TERMINATED
             │
             ▼
           FIM
```

### 1.3.1 Condição de Encerramento

A simulação deverá ser encerrada somente quando:

- todos os processos tiverem atingido o estado **TERMINATED**; e
- não houver operações de E/S pendentes.

Ao final da simulação, o sistema deverá disponibilizar os resultados da execução para permitir a análise do comportamento dos processos e da CPU.

Os resultados que deverão ser apresentados serão definidos nas seções referentes ao gerenciamento de processos, escalonamento e métricas de desempenho.

# 2. Especificação do Bloco de Controle de Processo (PCB) e da Tabela de Processos

## 2.1 Bloco de Controle de Processo (PCB)

O **PCB (Process Control Block)** será a estrutura de dados responsável por armazenar todas as informações necessárias para representar e controlar um processo dentro do simulador.

Cada processo deverá possuir **exatamente um PCB** durante toda a execução da simulação.

O PCB deverá armazenar o estado atual do processo, seu contexto de execução e as informações necessárias para que o processo possa ser interrompido, escalonado e posteriormente retomado.

O PCB deverá conter, no mínimo, os seguintes campos:

| Campo         | Tipo sugerido   | Obrigatório | Descrição                                            |
| ------------- | --------------- | ----------- | ---------------------------------------------------- |
| `pid`         | `int`           | Sim         | Identificador único do processo                      |
| `state`       | `enum`          | Sim         | Estado atual do processo                             |
| `pc`          | `int`           | Sim         | Índice da próxima operação da tarefa a ser executada |
| `registers`   | Estrutura/array | Sim         | Valores dos registradores virtuais salvos            |
| `priority`    | `int`           | Sim         | Prioridade utilizada pelo escalonador                |
| `cpuTime`     | `int`           | Sim         | Tempo total de CPU utilizado pelo processo           |
| `waitingTime` | `int`           | Sim         | Tempo total aguardando pela CPU                      |

O PCB poderá possuir outros campos auxiliares necessários à implementação, como:

- tempo de criação;
- tempo de conclusão;
- tempo de início da execução;
- operação atual de E/S;
- instante previsto para conclusão de E/S;
- identificador ou referência da tarefa associada.

Esses campos auxiliares não deverão substituir nenhum dos campos obrigatórios definidos nesta seção.

---

## 2.2 Identificador do Processo (PID)

Cada processo deverá possuir um **PID (Process Identifier)** único.

O PID será utilizado para identificar o processo durante toda a execução da simulação.

Os PIDs deverão ser atribuídos pelo simulador no momento da criação dos processos.

Exemplo:

```text
PID: 1
PID: 2
PID: 3
PID: 4
```

Dois processos existentes na Tabela de Processos não poderão possuir o mesmo PID.

A implementação deverá possuir um mecanismo de geração de PID que impeça a criação de processos com identificadores duplicados.

O PID de um processo não deverá ser alterado após sua criação.

---

## 2.3 Estado do Processo

O campo `state` deverá representar o estado atual do processo.

Os estados suportados deverão ser:

| Estado       | Descrição                                              |
| ------------ | ------------------------------------------------------ |
| `READY`      | Processo pronto para executar e aguardando a CPU       |
| `RUNNING`    | Processo atualmente utilizando a CPU                   |
| `BLOCKED`    | Processo aguardando a conclusão de uma operação de E/S |
| `TERMINATED` | Processo que concluiu todas as suas operações          |

As transições deverão ocorrer de acordo com os eventos definidos pelo simulador.

Exemplo:

```text
P1: READY
 ↓
P1: RUNNING
 ↓
P1: BLOCKED
 ↓
P1: READY
 ↓
P1: RUNNING
 ↓
P1: TERMINATED
```

As regras completas de transição serão especificadas na seção de **Ciclo de Vida e Grafo de Transição de Estados**.

Um processo no estado `TERMINATED` será considerado encerrado e não poderá retornar a nenhum outro estado.

---

## 2.4 Contador de Programa (PC)

O campo `pc` deverá armazenar o índice da próxima operação da tarefa associada ao processo.

O PC deverá ser representado por um número inteiro.

Por exemplo, considerando a seguinte tarefa:

```text
[CPU 5] → [CPU 3] → [IO 4] → [CPU 2]
```

O estado inicial será:

```text
PC = 0
```

indicando que a próxima operação será `CPU 5`.

Após a conclusão dessa operação:

```text
PC = 1
```

indicando que a próxima operação será `CPU 3`.

O PC deverá ser atualizado conforme as operações da tarefa forem concluídas.

Durante uma mudança de contexto, o valor do PC deverá ser preservado no PCB.

Quando o processo retornar ao estado `RUNNING`, sua execução deverá continuar a partir da operação indicada pelo PC.

---

## 2.5 Registradores Salvos

O campo `registers` deverá armazenar os valores dos registradores virtuais pertencentes ao processo.

Os registradores deverão fazer parte do contexto de execução do processo.

Quando um processo deixar a CPU devido a uma mudança de contexto, seus valores de registradores deverão ser armazenados no respectivo PCB.

Quando o processo voltar a utilizar a CPU, os valores armazenados no PCB deverão ser restaurados para a CPU virtual.

Exemplo:

```text
CPU Virtual

R0 = 10
R1 = 20
R2 = 30
R3 = 40

        │
        │ Mudança de contexto
        ▼

PCB do Processo

R0 = 10
R1 = 20
R2 = 30
R3 = 40
```

A preservação dos registradores deverá garantir que uma interrupção ou preempção não altere o contexto do processo.

---

## 2.6 Prioridade

O campo `priority` deverá armazenar a prioridade do processo.

A prioridade será utilizada pelos algoritmos de escalonamento que considerarem esse atributo.

Nesta especificação, será adotada a seguinte regra:

> **Quanto maior o valor numérico da prioridade, maior será a prioridade do processo.**

Exemplo:

```text
P1 → prioridade 2
P2 → prioridade 5
P3 → prioridade 3
```

A ordem de preferência será:

```text
P2 → P3 → P1
```

A prioridade inicial de cada processo deverá ser obtida a partir da configuração da tarefa ou de outro mecanismo definido na especificação do arquivo de tarefas.

Caso seja utilizado mecanismo de alteração dinâmica de prioridade, como envelhecimento (_aging_) para redução de starvation, suas regras deverão ser definidas na seção de escalonamento.

---

## 2.7 Tempo de CPU Utilizado

O campo `cpuTime` deverá armazenar o total de unidades de tempo em que o processo utilizou a CPU virtual.

O valor deverá iniciar em:

```text
cpuTime = 0
```

O `cpuTime` deverá ser incrementado somente enquanto:

1. o processo estiver no estado `RUNNING`; e
2. a CPU estiver executando uma operação de CPU pertencente ao processo.

O tempo utilizado durante operações de E/S não deverá ser contabilizado como `cpuTime`.

Exemplo:

```text
P1 executa:

CPU 3
CPU 2
CPU 4
```

Então:

```text
cpuTime = 3 + 2 + 4
cpuTime = 9
```

O valor deverá ser utilizado posteriormente para cálculo das métricas da simulação.

---

## 2.8 Tempo de Espera

O campo `waitingTime` deverá armazenar o total de unidades de tempo durante as quais o processo permaneceu no estado `READY` aguardando pela CPU.

O valor deverá iniciar em:

```text
waitingTime = 0
```

O `waitingTime` deverá ser incrementado somente enquanto o processo estiver:

```text
state = READY
```

e não estiver utilizando a CPU.

Exemplo:

```text
Tempo 0 → P1 READY
Tempo 1 → P1 READY
Tempo 2 → P1 READY
Tempo 3 → P1 RUNNING
```

Nesse caso:

```text
waitingTime = 3
```

O período em que o processo estiver no estado `BLOCKED` aguardando uma operação de E/S **não deverá ser contabilizado como tempo de espera pela CPU**.

---

## 2.9 Tabela de Processos

A **Tabela de Processos** será responsável por armazenar e organizar os PCBs de todos os processos existentes durante a simulação.

A tabela deverá permitir a localização de um PCB a partir do seu PID.

Estrutura conceitual:

```text
Tabela de Processos
│
├── PID 1 → PCB
├── PID 2 → PCB
├── PID 3 → PCB
└── PID 4 → PCB
```

Cada PID deverá estar associado a exatamente um PCB.

A Tabela de Processos deverá manter os processos registrados enquanto eles fizerem parte da simulação.

Os processos que atingirem o estado `TERMINATED` deverão permanecer na Tabela de Processos até o encerramento da simulação.

Isso permitirá que suas informações sejam utilizadas na geração das estatísticas finais.

---

## 2.10 Operações da Tabela de Processos

A Tabela de Processos deverá fornecer, no mínimo, as seguintes operações.

### 2.10.1 Inserir Processo

Deverá adicionar um novo PCB à tabela.

Operação conceitual:

```text
addProcess(PCB)
```

Antes da inserção, o sistema deverá garantir que o PID ainda não esteja sendo utilizado.

Caso o PID já exista, o processo não deverá ser inserido.

---

### 2.10.2 Buscar Processo

Deverá localizar um processo a partir do seu PID.

Operação conceitual:

```text
getProcess(pid)
```

Quando o PID existir, a operação deverá retornar o PCB correspondente.

Quando o PID não existir, a operação deverá indicar que o processo não foi encontrado.

---

### 2.10.3 Remover Processo

A Tabela de Processos **não deverá remover automaticamente** um processo quando ele atingir `TERMINATED`.

O PCB deverá permanecer registrado até o encerramento da simulação, permitindo a consulta dos dados utilizados nas estatísticas finais.

Caso seja necessária uma operação de remoção para gerenciamento interno, ela deverá ser utilizada somente quando não comprometer os resultados da simulação.

---

### 2.10.4 Listar Processos

A tabela deverá permitir a consulta dos processos registrados.

A listagem deverá apresentar, no mínimo:

```text
PID    Estado       Prioridade
------------------------------
1      READY             2
2      RUNNING           5
3      BLOCKED           3
4      TERMINATED        1
```

Os dados apresentados deverão refletir o estado atual armazenado no PCB.

---

### 2.10.5 Consultar Processos por Estado

A tabela deverá permitir a obtenção dos processos que estejam em determinado estado.

Exemplo:

```text
READY:
P1
P4

RUNNING:
P2

BLOCKED:
P3

TERMINATED:
P5
```

Essa operação poderá ser utilizada pelo escalonador, pelo gerenciador de E/S e pelo mecanismo de controle da simulação.

---

## 2.11 Relação entre PCB, CPU e Tabela de Processos

A relação entre os principais componentes deverá seguir o modelo:

```text
              Tabela de Processos
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
        PCB P1      PCB P2      PCB P3
          │           │           │
          │           │           │
          └───────────┼───────────┘
                      │
                      ▼
                Escalonador
                      │
                      ▼
                 CPU Virtual
                      │
                      ▼
             Contexto do processo
```

Somente o processo selecionado pelo escalonador deverá ter seu contexto carregado na CPU virtual.

Quando ocorrer uma mudança de contexto:

```text
CPU Virtual
     │
     │ salva contexto
     ▼
PCB do processo atual
     │
     │ carrega contexto
     ▼
PCB do próximo processo
     │
     ▼
CPU Virtual
```

O contexto deverá incluir, no mínimo:

- PC;
- registradores.

---

## 2.12 Regras de Consistência

A implementação deverá respeitar obrigatoriamente as seguintes regras:

1. Cada processo deverá possuir exatamente um PCB.
2. Cada PID deverá ser único.
3. O PID não poderá ser alterado após a criação do processo.
4. Cada processo deverá possuir exatamente um estado atual.
5. Somente os estados `READY`, `RUNNING`, `BLOCKED` e `TERMINATED` deverão ser utilizados.
6. Com uma única CPU virtual, no máximo um processo poderá estar em `RUNNING` simultaneamente.
7. Um processo `TERMINATED` não poderá retornar para `READY`, `RUNNING` ou `BLOCKED`.
8. Um processo `BLOCKED` não poderá ser selecionado pelo escalonador para utilizar a CPU.
9. Um processo `READY` poderá ser selecionado pelo escalonador.
10. O PC deverá representar a próxima operação da tarefa a ser executada.
11. O PC deverá ser preservado durante uma mudança de contexto.
12. Os registradores deverão ser preservados durante uma mudança de contexto.
13. `cpuTime` deverá contabilizar somente o tempo de utilização da CPU.
14. `waitingTime` deverá contabilizar somente o tempo em que o processo permaneceu `READY` aguardando a CPU.
15. O tempo em `BLOCKED` não deverá ser contabilizado como `waitingTime`.
16. A prioridade deverá seguir a regra de que valores maiores representam maior prioridade.
17. Processos `TERMINATED` deverão permanecer na Tabela de Processos até o encerramento da simulação.
18. A Tabela de Processos deverá manter a associação entre cada PID e seu respectivo PCB.
19. As informações armazenadas no PCB deverão ser suficientes para restaurar o contexto do processo após uma mudança de contexto.
20. Nenhum processo deverá executar simultaneamente com outro processo na CPU virtual.

---

## 2.13 Exemplo Completo de PCB

Um PCB poderá ser representado conceitualmente da seguinte forma:

```text
PCB
├── PID: 3
├── Estado: READY
├── PC: 2
├── Registradores:
│   ├── R0: 10
│   ├── R1: 20
│   ├── R2: 30
│   └── R3: 40
├── Prioridade: 5
├── Tempo de CPU: 8
└── Tempo de espera: 4
```

Esse PCB representa um processo que possui:

- PID igual a `3`;
- estado atual `READY`;
- próxima operação localizada no índice `2` da tarefa;
- quatro registradores virtuais armazenados;
- prioridade `5`;
- `8` unidades de tempo de CPU utilizadas;
- `4` unidades de tempo aguardando pela CPU.

Quando o processo for selecionado novamente pelo escalonador, seu contexto deverá ser restaurado e a execução deverá continuar a partir da operação indicada pelo `PC`.

# 3. Ciclo de Vida e Grafo de Transição de Estados

## 3.1 Visão Geral

O ciclo de vida de um processo no simulador será representado por quatro estados:

- `READY` — processo pronto para executar e aguardando a CPU;
- `RUNNING` — processo atualmente utilizando a CPU virtual;
- `BLOCKED` — processo aguardando a conclusão de uma operação de E/S;
- `TERMINATED` — processo que concluiu sua execução.

O simulador possuirá uma única CPU virtual. Portanto, **no máximo um processo poderá permanecer no estado `RUNNING` em qualquer instante da simulação**.

As transições de estado deverão ocorrer exclusivamente em resposta aos eventos definidos nesta especificação.

O fluxo geral de estados será:

```text
                 ┌──────────────┐
                 │    READY     │
                 └──────┬───────┘
                        │
                  escalonador
                        │
                        ▼
                 ┌──────────────┐
                 │   RUNNING    │
                 └──────┬───────┘
                        │
             ┌──────────┼──────────┐
             │          │          │
          Quantum      E/S       exit
             │          │          │
             ▼          ▼          ▼
          READY      BLOCKED   TERMINATED
                        │
                        │ E/S concluída
                        ▼
                      READY
```

---

## 3.2 Estado `READY`

O estado `READY` representa um processo que está apto a executar, mas está aguardando a oportunidade de utilizar a CPU virtual.

Um processo deverá entrar em `READY` nas seguintes situações:

1. após sua criação;
2. após a conclusão de uma operação de E/S;
3. após a expiração do quantum, quando houver preempção;
4. após uma decisão de preempção do algoritmo de escalonamento, quando aplicável.

Processos em `READY` deverão permanecer disponíveis para seleção pelo escalonador.

Um processo em `READY` não deverá executar operações de CPU enquanto não for selecionado pelo escalonador.

Transição para execução:

```text
READY
  │
  │ escalonador seleciona
  ▼
RUNNING
```

---

## 3.3 Estado `RUNNING`

O estado `RUNNING` representa o processo que está atualmente utilizando a CPU virtual.

Como existe apenas uma CPU:

> O simulador deverá garantir que nunca existam dois processos simultaneamente no estado `RUNNING`.

Enquanto estiver em `RUNNING`, o processo poderá:

- executar operações de CPU;
- solicitar uma operação de E/S;
- sofrer preempção devido à expiração do quantum;
- executar `exit` e terminar sua execução.

As possíveis transições são:

```text
RUNNING
   │
   ├── Quantum expirou ──► READY
   │
   ├── Solicita E/S ─────► BLOCKED
   │
   └── exit ─────────────► TERMINATED
```

Quando o processo estiver em `RUNNING`, seu contexto deverá estar carregado na CPU virtual.

---

## 3.4 Estado `BLOCKED`

O estado `BLOCKED` representa um processo que não pode continuar sua execução porque está aguardando a conclusão de uma operação de E/S.

Quando estiver `BLOCKED`:

- o processo não poderá utilizar a CPU;
- o processo não poderá ser selecionado pelo escalonador;
- o processo deverá permanecer fora da fila `READY`;
- o tempo restante da operação de E/S deverá ser acompanhado pelo simulador;
- outros processos `READY` poderão utilizar a CPU.

Transição de entrada:

```text
RUNNING
   │
   │ solicita E/S
   ▼
BLOCKED
```

Quando a E/S for concluída:

```text
BLOCKED
   │
   │ E/S concluída
   ▼
READY
```

A conclusão da E/S não deverá conceder automaticamente a CPU ao processo. O processo deverá voltar para `READY` e aguardar uma seleção do escalonador.

---

## 3.5 Estado `TERMINATED`

O estado `TERMINATED` representa um processo que concluiu sua execução.

O processo deverá entrar nesse estado quando executar a operação simulada `exit` ou quando atingir o término definido para sua sequência de operações, conforme especificado no modelo de tarefas.

Ao entrar em `TERMINATED`:

1. o processo deverá deixar a CPU;
2. seu estado deverá ser atualizado para `TERMINATED`;
3. o instante de término deverá ser registrado;
4. o processo não deverá mais ser selecionado pelo escalonador;
5. seu PCB deverá permanecer na Tabela de Processos até o encerramento da simulação.

Um processo `TERMINATED` não poderá retornar a nenhum outro estado.

Transição:

```text
RUNNING
   │
   │ exit
   ▼
TERMINATED
```

---

## 3.6 Criação de Processos — `fork`

A operação simulada `fork` será responsável pela criação de um novo processo.

O `fork` **não deverá criar um processo real no sistema operacional hospedeiro**. A operação deverá existir exclusivamente dentro do ambiente virtual do simulador.

Quando um processo executar `fork`, o simulador deverá:

1. gerar um novo PID;
2. criar um novo PCB;
3. inicializar os dados obrigatórios do novo PCB;
4. inserir o novo PCB na Tabela de Processos;
5. definir o estado inicial do novo processo como `READY`;
6. disponibilizar o novo processo para o escalonador.

A criação do novo processo não deverá fazer com que ele entre diretamente em `RUNNING`.

A transição do novo processo será:

```text
fork
  │
  ▼
READY
```

O processo que executou `fork` deverá continuar no estado `RUNNING`, salvo se algum evento de escalonamento provocar sua saída da CPU.

A forma como o novo processo receberá sua sequência de operações deverá ser definida na especificação do formato das tarefas.

---

## 3.7 Expiração do Quantum

O **quantum** representa a quantidade máxima de tempo de CPU que um processo poderá utilizar continuamente antes de sofrer preempção, quando o algoritmo de escalonamento utilizar esse mecanismo.

O simulador deverá acompanhar o tempo utilizado pelo processo atualmente em `RUNNING`.

Quando o quantum expirar e o processo ainda estiver executando:

1. a execução deverá ser interrompida;
2. o contexto do processo deverá ser salvo no PCB;
3. o processo deverá mudar de `RUNNING` para `READY`;
4. o processo deverá ser inserido novamente na fila de processos prontos;
5. o escalonador deverá ser acionado para selecionar o próximo processo.

Transição:

```text
RUNNING
   │
   │ quantum expirou
   ▼
READY
```

A preempção por quantum deverá ser utilizada pelo algoritmo **Round Robin** e por qualquer outro algoritmo que explicitamente utilize esse mecanismo.

Se o processo terminar ou solicitar E/S antes da expiração do quantum, a transição correspondente deverá ter prioridade sobre a preempção.

---

## 3.8 Solicitação de E/S

Quando um processo em `RUNNING` solicitar uma operação de E/S, o simulador deverá interromper sua execução de CPU e iniciar o tratamento da operação de E/S.

O simulador deverá:

1. interromper a execução da operação atual;
2. preservar o contexto do processo;
3. registrar a duração da operação de E/S;
4. registrar o instante previsto para conclusão da E/S;
5. alterar o estado de `RUNNING` para `BLOCKED`;
6. remover o processo da CPU virtual;
7. acionar o escalonador para selecionar outro processo `READY`, caso exista.

Transição:

```text
RUNNING
   │
   │ solicita E/S
   ▼
BLOCKED
```

O processo bloqueado não deverá permanecer na fila `READY`.

Durante o período em `BLOCKED`, o tempo de espera por E/S deverá ser acompanhado pelo simulador, mas não deverá ser contabilizado como `waitingTime` de CPU.

---

## 3.9 Conclusão de E/S

Quando o relógio lógico atingir o instante definido para a conclusão da operação de E/S, o processo deverá deixar o estado `BLOCKED`.

O simulador deverá:

1. detectar a conclusão da E/S;
2. atualizar o estado do processo para `READY`;
3. atualizar as informações relacionadas à E/S;
4. inserir o processo novamente na estrutura de processos prontos;
5. permitir que o escalonador considere o processo em suas próximas decisões.

Transição:

```text
BLOCKED
   │
   │ E/S concluída
   ▼
READY
```

O processo não deverá passar diretamente de `BLOCKED` para `RUNNING`.

---

## 3.10 Término da Execução — `exit`

A operação simulada `exit` deverá indicar que o processo terminou sua execução.

Quando `exit` for executado:

1. o processo deverá deixar o estado `RUNNING`;
2. o estado deverá ser alterado para `TERMINATED`;
3. o instante de término deverá ser registrado;
4. o contexto final deverá ser preservado no PCB;
5. o processo deverá deixar de ser considerado pelo escalonador;
6. a CPU deverá ser disponibilizada para o próximo processo.

Transição:

```text
RUNNING
   │
   │ exit
   ▼
TERMINATED
```

Após essa transição, o processo não poderá voltar a executar.

---

## 3.11 Mudança de Contexto

Uma **mudança de contexto** deverá ocorrer sempre que a CPU deixar de executar um processo e passar a executar outro.

A mudança de contexto deverá preservar o estado necessário para que o processo interrompido possa continuar posteriormente.

No mínimo, deverão ser preservados:

- `PC`;
- registradores virtuais;
- demais informações de execução necessárias ao funcionamento do simulador.

Fluxo conceitual:

```text
Processo P1
    │
    │ deixa a CPU
    ▼
Salvar contexto no PCB de P1
    │
    ▼
Escalonador seleciona P2
    │
    ▼
Carregar contexto do PCB de P2
    │
    ▼
Processo P2
    │
    ▼
RUNNING
```

A mudança de contexto não deverá alterar o estado lógico armazenado dos demais processos.

---

## 3.12 Grafo de Transição de Estados

O grafo completo de transição dos processos será:

```text
                       ┌──────────────┐
                ┌─────►│    READY     │◄──────────────┐
                │      └──────┬───────┘               │
                │             │                       │
                │             │ escalonador           │
                │             ▼                       │
                │      ┌──────────────┐               │
                │      │   RUNNING    │               │
                │      └──────┬───────┘               │
                │             │                       │
                │       ┌─────┼─────┐                 │
                │       │     │     │                 │
                │       │     │     │                 │
                │       │     │     │ exit            │
                │       │     │     └──────────┐       │
                │       │     │                ▼       │
                │       │     │        ┌────────────┐  │
                │       │     │        │ TERMINATED │  │
                │       │     │        └────────────┘  │
                │       │     │                        │
                │       │     │ solicita E/S            │
                │       │     ▼                        │
                │       │  ┌──────────────┐            │
                │       └─►│   BLOCKED    │            │
                │          └──────┬───────┘            │
                │                 │                    │
                │                 │ E/S concluída      │
                └─────────────────┘                    │
                                                       │
                         Quantum expirou ──────────────┘
```

De forma mais simples:

```text
                 ┌───────────────┐
                 │     READY     │
                 └───────┬───────┘
                         │
                   escalonador
                         │
                         ▼
                 ┌───────────────┐
                 │    RUNNING    │
                 └───┬─────┬─────┘
                     │     │
                 E/S │     │ quantum
                     │     │ expirou
                     ▼     ▼
              ┌──────────┐ READY
              │ BLOCKED  │
              └────┬─────┘
                   │
              E/S concluída
                   │
                   ▼
                 READY

RUNNING ─── exit ───► TERMINATED
```

---

## 3.13 Resumo das Transições

| Estado atual | Evento                | Novo estado  |
| ------------ | --------------------- | ------------ |
| —            | Criação do processo   | `READY`      |
| `READY`      | Escalonador seleciona | `RUNNING`    |
| `RUNNING`    | Quantum expira        | `READY`      |
| `RUNNING`    | Solicitação de E/S    | `BLOCKED`    |
| `BLOCKED`    | E/S concluída         | `READY`      |
| `RUNNING`    | `exit`                | `TERMINATED` |
| `TERMINATED` | Qualquer evento       | `TERMINATED` |

A operação `fork` deverá criar um **novo processo** no estado `READY`, não sendo considerada uma transição de estado do processo que executou a operação.

---

## 3.14 Regras de Consistência

A implementação deverá respeitar obrigatoriamente as seguintes regras:

1. Todo processo recém-criado deverá iniciar no estado `READY`.
2. Somente processos em `READY` poderão ser selecionados pelo escalonador.
3. No máximo um processo poderá estar em `RUNNING` simultaneamente.
4. Processos em `BLOCKED` não poderão ser selecionados pelo escalonador.
5. Processos em `TERMINATED` não poderão ser selecionados pelo escalonador.
6. Um processo em `BLOCKED` deverá retornar para `READY` somente após a conclusão de sua E/S.
7. Um processo que sofrer preempção por expiração do quantum deverá retornar para `READY`.
8. Um processo que executar `exit` deverá entrar em `TERMINATED`.
9. Um processo em `TERMINATED` não poderá retornar para `READY`, `RUNNING` ou `BLOCKED`.
10. A operação `fork` deverá criar um novo processo virtual e não deverá criar um processo real no sistema operacional.
11. O novo processo criado por `fork` deverá iniciar em `READY`.
12. A execução do processo que realizou `fork` deverá continuar normalmente, salvo ocorrência de outro evento de escalonamento.
13. Toda mudança de estado deverá ser registrada no log da simulação.
14. Toda mudança de processo na CPU deverá preservar o contexto do processo que está deixando a CPU.
15. O contexto mínimo preservado deverá conter o PC e os registradores virtuais.
16. Um processo `BLOCKED` deverá permanecer fora da fila `READY`.
17. A conclusão de uma E/S deverá colocar o processo em `READY`, e não diretamente em `RUNNING`.
18. O tempo em `BLOCKED` não deverá ser contabilizado como `waitingTime`.
19. A expiração do quantum somente deverá causar preempção se o processo ainda estiver em `RUNNING`.
20. Caso o processo termine ou solicite E/S antes da expiração do quantum, a transição correspondente deverá ocorrer em vez da transição por expiração do quantum.
21. Processos `TERMINATED` deverão permanecer registrados na Tabela de Processos até o encerramento da simulação.
22. O instante de término de cada processo deverá ser registrado para utilização nas métricas finais.

# 4. Especificação do Escalonador de CPU

## 4.1 Visão Geral

O simulador deverá possuir um módulo de **Escalonador de CPU** responsável por selecionar, entre os processos no estado `READY`, qual processo deverá utilizar a CPU virtual.

O escalonador deverá suportar, no mínimo, os seguintes algoritmos:

1. **Round Robin (RR);**
2. **Escalonamento por Prioridade Dinâmica.**

Os algoritmos deverão implementar uma **interface comum**, permitindo que sejam utilizados de forma intercambiável sem alterações nos demais componentes do simulador.

A escolha do algoritmo deverá ser realizada **antes do início da simulação**.

O algoritmo selecionado deverá permanecer ativo durante toda a execução daquela simulação.

O escalonador deverá considerar somente processos no estado `READY`.

Processos nos estados `BLOCKED` ou `TERMINATED` não poderão ser selecionados para execução.

---

## 4.2 Interface do Escalonador

Todos os algoritmos de escalonamento deverão seguir uma interface comum.

A interface deverá fornecer, no mínimo, as seguintes operações:

```text
schedule()
addProcess(process)
removeProcess(process)
```

### `schedule()`

A operação `schedule()` deverá selecionar o próximo processo que receberá a CPU.

O resultado deverá ser:

- um processo no estado `READY`, quando houver processos prontos;
- ausência de processo (`null`, `None` ou equivalente), quando não houver processos `READY`.

A operação `schedule()` não deverá selecionar processos `BLOCKED` ou `TERMINATED`.

### `addProcess(process)`

A operação deverá adicionar um processo à estrutura utilizada pelo algoritmo de escalonamento.

Somente processos que possam ser considerados pelo algoritmo deverão ser adicionados à estrutura de processos prontos.

### `removeProcess(process)`

A operação deverá remover um processo da estrutura utilizada pelo algoritmo.

Essa operação deverá ser utilizada quando o processo:

- deixar de estar `READY`;
- for selecionado para execução;
- entrar em `BLOCKED`;
- entrar em `TERMINATED`.

A forma exata de organização interna da estrutura poderá variar entre os algoritmos.

Estrutura conceitual:

```text
                  ┌──────────────────┐
                  │    Escalonador   │
                  └────────┬─────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
      ┌───────────────┐       ┌───────────────────┐
      │  Round Robin  │       │ Prioridade Dinâmica│
      └───────────────┘       └───────────────────┘
```

Os demais componentes do simulador deverão interagir somente com a interface do escalonador, sem depender diretamente da implementação de um algoritmo específico.

---

# 4.3 Round Robin

O algoritmo **Round Robin (RR)** deverá distribuir a utilização da CPU entre os processos `READY` de maneira rotativa.

O algoritmo deverá utilizar uma **fila circular de processos prontos**.

Cada processo deverá receber uma quantidade limitada de tempo de CPU denominada **quantum**.

---

## 4.3.1 Fila Circular de Processos Prontos

Os processos `READY` deverão ser organizados em uma fila circular.

A ordem dos processos na fila determinará a ordem em que eles serão selecionados.

Exemplo:

```text
┌────┐    ┌────┐    ┌────┐    ┌────┐
│ P1 │ →  │ P2 │ →  │ P3 │ →  │ P4 │
└────┘    └────┘    └────┘    └────┘
   ↑                              │
   └──────────────────────────────┘
```

Quando um processo for selecionado, ele deverá ser retirado da posição correspondente para utilizar a CPU.

Quando o processo sofrer preempção por expiração do quantum e ainda possuir operações a executar, ele deverá ser colocado **no final da fila**.

Exemplo:

```text
Antes:

[P1] → [P2] → [P3] → [P4]

P1 executa e o quantum expira.

Depois:

[P2] → [P3] → [P4] → [P1]
```

---

## 4.3.2 Quantum

O **quantum** será a quantidade máxima de unidades de tempo consecutivas que um processo poderá utilizar a CPU antes de sofrer preempção.

O valor do quantum deverá ser configurável antes do início da simulação.

Exemplo:

```text
Quantum = 3 ticks
```

Com quatro processos:

```text
P1 → 3 ticks
P2 → 3 ticks
P3 → 3 ticks
P4 → 3 ticks
P1 → 3 ticks
...
```

O quantum deverá ser contabilizado separadamente para cada período de execução do processo.

Quando um processo voltar a executar após uma preempção, um novo quantum deverá ser iniciado.

Caso o processo termine ou solicite E/S antes da expiração do quantum, ele deverá deixar a CPU imediatamente e **não deverá retornar à fila `READY` naquele momento**.

---

## 4.3.3 Seleção no Round Robin

Quando a CPU estiver disponível, o Round Robin deverá:

1. verificar a fila de processos `READY`;
2. selecionar o processo que estiver no início da fila;
3. remover o processo da posição inicial;
4. alterar seu estado para `RUNNING`;
5. carregar seu contexto na CPU virtual;
6. iniciar a contagem de um novo quantum.

Se a fila estiver vazia, o escalonador deverá informar que não existe processo pronto para executar.

---

## 4.3.4 Expiração do Quantum

Quando o quantum do processo `RUNNING` expirar:

1. a CPU deverá interromper a execução do processo;
2. o contexto deverá ser salvo no PCB;
3. o estado deverá ser alterado de `RUNNING` para `READY`;
4. o processo deverá ser colocado no final da fila circular;
5. o escalonador deverá selecionar o próximo processo disponível.

Transição:

```text
RUNNING
   │
   │ quantum expirou
   ▼
READY
   │
   │ fim da fila
   ▼
[FILA READY]
```

A preempção deverá ocorrer somente se o processo ainda possuir operações a executar e não estiver bloqueado ou terminado.

---

## 4.3.5 Processo Termina Antes do Quantum

Se o processo concluir sua execução antes da expiração do quantum, deverá executar `exit`.

Nesse caso:

```text
RUNNING
   │
   │ exit
   ▼
TERMINATED
```

O processo:

- não deverá retornar à fila `READY`;
- não deverá receber outro quantum;
- não poderá ser selecionado novamente;
- deverá permanecer registrado na Tabela de Processos.

O tempo efetivamente utilizado na CPU deverá ser contabilizado em `cpuTime`.

---

## 4.3.6 Processo Solicita E/S Antes do Quantum

Se o processo solicitar uma operação de E/S antes da expiração do quantum:

```text
RUNNING
   │
   │ solicita E/S
   ▼
BLOCKED
```

O simulador deverá:

1. interromper a execução do processo;
2. salvar seu contexto;
3. alterar seu estado para `BLOCKED`;
4. registrar a duração da E/S;
5. remover o processo da CPU;
6. removê-lo da estrutura de processos `READY`, caso esteja nela;
7. selecionar outro processo, caso exista.

Após a conclusão da E/S:

```text
BLOCKED
   │
   │ E/S concluída
   ▼
READY
```

O processo deverá ser inserido **no final da fila do Round Robin**.

---

## 4.3.7 Ordem de Entrada na Fila do Round Robin

Sempre que um processo retornar ao estado `READY` após:

- expiração do quantum; ou
- conclusão de uma operação de E/S;

ele deverá ser inserido no final da fila.

Isso deverá preservar o comportamento circular do algoritmo.

Exemplo:

```text
Fila atual:

[P1] → [P2] → [P3]

P2 sofre preempção.

Nova fila:

[P1] → [P3] → [P2]
```

---

# 4.4 Escalonamento por Prioridade Dinâmica

O segundo algoritmo deverá utilizar **prioridade dinâmica**.

Cada processo deverá possuir uma prioridade inicial armazenada em seu PCB.

Nesta especificação:

> Quanto maior o valor numérico da prioridade, maior será a prioridade do processo.

Exemplo:

```text
P1 → prioridade 2
P2 → prioridade 5
P3 → prioridade 3
P4 → prioridade 1
```

A ordem inicial de preferência será:

```text
P2 → P3 → P1 → P4
```

O escalonador deverá selecionar entre os processos `READY` aquele que possuir a maior **prioridade efetiva**.

---

## 4.4.1 Prioridade Original e Prioridade Efetiva

A prioridade do processo deverá ser dividida conceitualmente em:

- **prioridade original** — valor definido para o processo;
- **prioridade efetiva** — valor utilizado pelo escalonador no momento da seleção.

A prioridade original deverá permanecer armazenada no PCB.

A prioridade efetiva deverá ser calculada pelo escalonador considerando a prioridade original e o mecanismo de `aging`.

Exemplo:

```text
Prioridade original = 2
Tempo de espera     = 5
Prioridade efetiva  = 4
```

A fórmula exata do aumento de prioridade deverá ser definida pelos parâmetros de `aging` da simulação.

---

# 4.5 Prevenção de Starvation — Aging

O algoritmo de prioridade deverá possuir um mecanismo de **aging** para reduzir o risco de starvation.

**Starvation** ocorre quando um processo permanece por tempo excessivo em `READY` porque processos com prioridades maiores continuam sendo selecionados.

O `aging` deverá aumentar progressivamente a prioridade efetiva dos processos enquanto eles permanecerem aguardando a CPU.

Exemplo conceitual:

```text
Prioridade original: 1

Tempo de espera: 0
Prioridade efetiva: 1

Tempo de espera: 2
Prioridade efetiva: 2

Tempo de espera: 4
Prioridade efetiva: 3

Tempo de espera: 6
Prioridade efetiva: 4
```

A prioridade efetiva deverá aumentar conforme o processo acumular tempo de espera.

A prioridade original não deverá ser modificada pelo `aging`.

---

## 4.5.1 Regra de Aging

O mecanismo de aging deverá utilizar o tempo de espera do processo para calcular sua prioridade efetiva.

A prioridade efetiva deverá ser determinada por uma regra equivalente a:

```text
prioridadeEfetiva =
    prioridadeOriginal + incrementoPorAging
```

O incremento deverá ser determinado a partir do tempo de espera e da configuração do aging.

Exemplo de configuração:

```text
Aging:
a cada 2 ticks de espera
→ aumentar 1 ponto na prioridade efetiva
```

Nesse caso:

```text
prioridadeOriginal = 2

waitingTime = 0 → efetiva = 2
waitingTime = 2 → efetiva = 3
waitingTime = 4 → efetiva = 4
waitingTime = 6 → efetiva = 5
```

O valor do intervalo de aging deverá ser configurável.

---

# 4.6 Seleção por Prioridade

Quando a CPU estiver disponível, o escalonador por prioridade deverá:

1. identificar todos os processos no estado `READY`;
2. calcular ou atualizar a prioridade efetiva de cada processo;
3. identificar o processo com maior prioridade efetiva;
4. aplicar a regra de desempate quando necessário;
5. remover o processo selecionado da estrutura de processos prontos;
6. alterar seu estado para `RUNNING`;
7. carregar seu contexto na CPU virtual.

Exemplo:

```text
Processos READY:

P1 → prioridade efetiva 3
P2 → prioridade efetiva 7
P3 → prioridade efetiva 5

                │
                ▼

           Escalonador

                │
                ▼

P2 → RUNNING
```

---

# 4.7 Desempate de Prioridade

Caso dois ou mais processos possuam a mesma prioridade efetiva, deverá ser utilizada a regra **FCFS (First Come, First Served)**.

O processo que estiver aguardando há mais tempo no estado `READY` deverá ser selecionado primeiro.

Exemplo:

```text
P1 → prioridade efetiva 5 → esperando desde t=2
P2 → prioridade efetiva 5 → esperando desde t=5
```

Resultado:

```text
P1 → RUNNING
```

A regra FCFS deverá impedir que processos com a mesma prioridade sejam escolhidos de maneira arbitrária.

Em caso de empate também no instante de entrada em `READY`, deverá ser utilizado o menor PID como critério final de desempate.

---

# 4.8 Preempção no Escalonamento por Prioridade

O algoritmo de prioridade deverá ser **preemptivo**.

Enquanto um processo estiver em `RUNNING`, o simulador deverá verificar se existe algum processo `READY` com prioridade efetiva maior que a prioridade efetiva do processo atual.

Caso exista, deverá ocorrer uma preempção.

O processo atualmente em execução deverá:

1. ter seu contexto salvo;
2. ter seu estado alterado de `RUNNING` para `READY`;
3. retornar à estrutura de processos prontos;
4. perder a utilização atual da CPU.

O novo processo deverá:

1. ser selecionado pelo escalonador;
2. ter seu contexto carregado;
3. passar para `RUNNING`.

Exemplo:

```text
P1 → RUNNING
     prioridade efetiva = 3

        │
        │ P2 chega
        ▼

P2 → READY
     prioridade efetiva = 7

        │
        ▼

P1 → READY
P2 → RUNNING
```

O processo preemptado deverá preservar seu PC e seus registradores no PCB.

---

# 4.9 Processos com Mesma Prioridade

Quando o processo em `RUNNING` possuir a mesma prioridade efetiva que um processo `READY`, a chegada do novo processo **não deverá causar preempção por prioridade**.

Nesse caso, o processo atual deverá continuar utilizando a CPU até:

- terminar;
- solicitar E/S; ou
- sofrer outra condição de preempção definida pelo algoritmo.

Quando for necessário escolher entre processos `READY` com a mesma prioridade efetiva, deverá ser utilizada a regra FCFS.

---

# 4.10 Tratamento de Processos Bloqueados

Os dois algoritmos deverão respeitar as mesmas regras para processos `BLOCKED`.

Um processo `BLOCKED`:

- não poderá utilizar a CPU;
- não poderá ser selecionado pelo escalonador;
- não poderá permanecer na fila `READY`;
- deverá aguardar a conclusão da E/S.

Quando a E/S for concluída:

```text
BLOCKED
   │
   │ E/S concluída
   ▼
READY
```

O processo deverá voltar a disputar a CPU.

No Round Robin, deverá ser inserido no final da fila circular.

No escalonamento por prioridade, deverá ser reinserido na estrutura de processos prontos e sua prioridade efetiva deverá ser considerada de acordo com as regras de aging.

---

# 4.11 Troca entre os Algoritmos

A escolha do algoritmo deverá ocorrer antes do início da simulação.

Exemplo:

```text
================================
 SIMULADOR DE SISTEMA OPERACIONAL
================================

Escolha o algoritmo:

1 - Round Robin
2 - Prioridade Dinâmica

Opção: 1

Quantum: 3
```

Quando a opção `Round Robin` for selecionada, somente as regras do Round Robin deverão ser utilizadas.

Quando `Prioridade Dinâmica` for selecionada, somente as regras do escalonamento por prioridade deverão ser utilizadas.

A escolha do algoritmo não deverá exigir alterações na implementação:

- dos processos;
- do PCB;
- da Tabela de Processos;
- da CPU virtual;
- do gerenciamento de E/S.

Apenas a implementação concreta do escalonador deverá ser alterada.

---

# 4.12 Tratamento da CPU Ociosa

Caso não exista nenhum processo `READY` e exista pelo menos um processo `BLOCKED`, a CPU virtual deverá permanecer ociosa enquanto o relógio lógico continuar avançando até que algum evento de E/S seja concluído.

Exemplo:

```text
READY:   vazio
RUNNING: nenhum
BLOCKED: P2, P3

             │
             ▼

        CPU Ociosa
             │
             │ avanço do relógio
             ▼
       E/S de P2 concluída
             │
             ▼
          P2 → READY
             │
             ▼
        Escalonador
```

Quando um processo bloqueado retornar para `READY`, o escalonador deverá ser acionado.

---

# 4.13 Regras de Consistência do Escalonador

A implementação deverá respeitar obrigatoriamente as seguintes regras:

1. Somente processos `READY` poderão ser selecionados pelo escalonador.
2. Processos `BLOCKED` não poderão utilizar a CPU.
3. Processos `TERMINATED` não poderão utilizar a CPU.
4. No máximo um processo poderá estar em `RUNNING` simultaneamente.
5. Todo processo selecionado deverá passar para `RUNNING`.
6. Todo processo que deixar a CPU deverá ter seu contexto preservado.
7. O contexto mínimo deverá conter o PC e os registradores virtuais.
8. Um processo que terminar deverá passar para `TERMINATED`.
9. Um processo que solicitar E/S deverá passar para `BLOCKED`.
10. Um processo cuja E/S for concluída deverá retornar para `READY`.
11. No Round Robin, a fila de processos prontos deverá seguir uma ordem circular.
12. No Round Robin, um processo preemptado por expiração do quantum deverá retornar ao final da fila.
13. O quantum deverá ser configurável.
14. Um processo que terminar antes da expiração do quantum não deverá retornar à fila `READY`.
15. Um processo que solicitar E/S antes da expiração do quantum deverá passar para `BLOCKED`.
16. No escalonamento por prioridade, valores maiores deverão representar maior prioridade.
17. O escalonamento por prioridade deverá utilizar prioridade efetiva.
18. A prioridade original do processo não deverá ser alterada pelo aging.
19. O aging deverá aumentar a prioridade efetiva conforme o processo acumular tempo de espera.
20. Processos com mesma prioridade efetiva deverão utilizar FCFS como regra de desempate.
21. O menor PID deverá ser utilizado como último critério de desempate caso os processos também possuam o mesmo instante de entrada em `READY`.
22. O escalonamento por prioridade deverá ser preemptivo quando um processo `READY` possuir prioridade efetiva maior que a do processo `RUNNING`.
23. Um processo `READY` com prioridade igual à do processo `RUNNING` não deverá causar preempção por prioridade.
24. Processos que retornarem de E/S deverão voltar ao estado `READY`.
25. O processo que retornar de E/S não deverá receber a CPU automaticamente.
26. Toda mudança de processo na CPU deverá ser registrada no log.
27. Toda preempção deverá ser registrada no log.
28. A CPU deverá permanecer ociosa quando não houver processos `READY` e deverá continuar acompanhando os eventos de E/S.
29. O algoritmo escolhido deverá permanecer ativo durante toda a simulação.
30. A implementação dos algoritmos deverá ser intercambiável por meio da interface comum do escalonador.

---

# 4.14 Comparação dos Algoritmos

| Característica      | Round Robin                        | Prioridade Dinâmica                                                 |
| ------------------- | ---------------------------------- | ------------------------------------------------------------------- |
| Estrutura principal | Fila circular                      | Estrutura ordenada por prioridade                                   |
| Critério de seleção | Primeiro processo da fila          | Maior prioridade efetiva                                            |
| Quantum             | Obrigatório                        | Não é o mecanismo principal                                         |
| Preempção           | Expiração do quantum               | Prioridade efetiva maior                                            |
| Aging               | Não utilizado                      | Utilizado                                                           |
| Starvation          | Reduzido pela rotação              | Tratado por aging                                                   |
| Desempate           | Ordem da fila                      | FCFS                                                                |
| Prioridade          | Não utilizada para seleção         | Utilizada                                                           |
| Objetivo principal  | Distribuir a CPU de forma rotativa | Favorecer processos de maior prioridade                             |
| E/S concluída       | Processo vai para o final da fila  | Processo retorna para `READY` e participa da seleção por prioridade |

Os dois algoritmos deverão poder executar os mesmos conjuntos de tarefas, permitindo comparar as métricas produzidas por cada estratégia de escalonamento.

# 5. Entradas, Casos de Teste e Diretrizes de Entrega

## 5.1 Entrada do Simulador

O simulador deverá receber como entrada um **arquivo de tarefas** contendo a descrição dos processos que participarão da simulação.

O arquivo deverá fornecer as informações necessárias para:

- identificar cada processo;
- definir a prioridade inicial;
- definir a sequência de operações;
- definir os surtos de utilização da CPU;
- definir as operações de E/S;
- definir o término dos processos.

O simulador deverá realizar a leitura do arquivo antes do início da execução e utilizar as informações obtidas para criar os processos e seus respectivos PCBs.

O arquivo de tarefas deverá ser utilizado exclusivamente como entrada da simulação. A execução dos processos deverá ocorrer dentro do ambiente virtual do simulador, sem criação de processos reais no sistema operacional hospedeiro.

---

# 5.2 Formato do Arquivo de Tarefas

O arquivo de tarefas deverá utilizar o formato de texto com extensão `.txt`.

Cada processo deverá ser representado por uma linha contendo:

```text
PID;PRIORIDADE;OPERAÇÕES
```

As operações deverão ser separadas por espaços.

Serão suportadas as seguintes operações:

```text
CPU:n
IO:n
EXIT
```

Onde:

- `CPU:n` representa um surto de CPU com duração de `n` unidades de tempo;
- `IO:n` representa uma operação de E/S com duração de `n` unidades de tempo;
- `EXIT` representa o término do processo.

O valor `n` deverá ser um número inteiro positivo.

### Exemplo

```text
1;3;CPU:4 IO:3 CPU:2 EXIT
2;5;CPU:2 IO:4 CPU:3 EXIT
3;1;CPU:5 EXIT
```

Nesse exemplo:

- `P1` possui prioridade 3, executa 4 unidades de CPU, realiza E/S durante 3 unidades, executa mais 2 unidades de CPU e termina;
- `P2` possui prioridade 5, executa 2 unidades de CPU, realiza E/S durante 4 unidades, executa mais 3 unidades de CPU e termina;
- `P3` possui prioridade 1, executa 5 unidades de CPU e termina.

O parser deverá rejeitar linhas que não estejam de acordo com o formato definido.

---

# 5.3 Regras de Validação da Entrada

Antes de iniciar a simulação, o simulador deverá validar o arquivo de tarefas.

Deverão ser consideradas inválidas, no mínimo:

1. linhas sem PID;
2. linhas sem prioridade;
3. linhas sem sequência de operações;
4. PID duplicado;
5. prioridade que não seja um número inteiro;
6. duração `n` ausente ou inválida em `CPU:n`;
7. duração `n` ausente ou inválida em `IO:n`;
8. duração igual ou inferior a zero para `CPU:n`;
9. duração igual ou inferior a zero para `IO:n`;
10. operação desconhecida;
11. processo sem operação `EXIT`;
12. campos obrigatórios ausentes.

Quando uma entrada inválida for encontrada, o simulador deverá informar o erro de forma clara, indicando, quando possível, o número da linha e o problema identificado.

Exemplo:

```text
Erro no arquivo de tarefas.
Linha: 3
Problema: operação desconhecida "WAIT".
```

O simulador não deverá iniciar a execução enquanto existirem erros de validação na entrada.

---

# 5.4 Criação dos Processos

Os processos descritos no arquivo deverão ser criados pelo simulador antes do início da execução da CPU.

A criação deverá representar conceitualmente a criação de processos por meio da operação `fork`, mas **não deverá utilizar o `fork` real do sistema operacional**.

Para cada processo descrito no arquivo, o simulador deverá:

1. criar um PCB;
2. atribuir um PID único;
3. definir a prioridade inicial;
4. armazenar a sequência de operações;
5. inicializar o PC;
6. inicializar os registradores virtuais;
7. inicializar os contadores de tempo;
8. definir o estado inicial como `READY`;
9. registrar o instante de criação;
10. inserir o processo na Tabela de Processos;
11. adicionar o processo à estrutura utilizada pelo escalonador.

O instante de criação dos processos deverá ser definido de forma determinística.

Por padrão, todos os processos carregados a partir do arquivo deverão ser considerados criados no instante:

```text
t = 0
```

A ordem das linhas do arquivo deverá ser preservada para fins de desempate quando os processos possuírem as mesmas condições de seleção.

---

# 5.5 Sequência de Operações

Cada processo deverá possuir uma sequência ordenada de operações.

O simulador deverá executar as operações exatamente na ordem em que aparecem no arquivo.

Exemplo:

```text
P1:

CPU:3
IO:4
CPU:2
EXIT
```

A execução deverá seguir:

```text
CPU:3
   ↓
IO:4
   ↓
CPU:2
   ↓
EXIT
```

O processo deverá possuir um contador de operação, indicando qual operação da sequência deverá ser executada.

Exemplo conceitual:

```text
Operações:

[0] CPU:3
[1] IO:4
[2] CPU:2
[3] EXIT

PC lógico da operação:
      ↑
```

O contador deverá avançar somente quando a operação correspondente for concluída.

Quando uma operação `CPU:n` for interrompida por preempção, o processo deverá preservar a quantidade restante da operação para continuar posteriormente.

---

# 5.6 Operação `CPU:n`

A operação `CPU:n` representa um surto de utilização da CPU com duração de `n` unidades de tempo.

Exemplo:

```text
CPU:5
```

significa que o processo precisa utilizar a CPU durante cinco unidades de tempo para concluir essa operação.

Enquanto estiver executando uma operação `CPU`, o processo deverá permanecer no estado:

```text
RUNNING
```

A cada unidade de tempo efetivamente executada:

```text
cpuTime = cpuTime + 1
```

A quantidade restante da operação deverá ser decrementada:

```text
remainingCPU = remainingCPU - 1
```

Quando:

```text
remainingCPU = 0
```

a operação `CPU:n` deverá ser considerada concluída e o simulador deverá avançar para a próxima operação.

A execução de uma operação `CPU:n` poderá ser interrompida por:

- expiração do quantum no Round Robin;
- preempção por prioridade no escalonamento por prioridade;
- conclusão do surto de CPU;
- qualquer outro evento explicitamente definido nesta especificação.

Quando houver preempção, o processo deverá preservar sua posição e o restante do surto de CPU para continuar posteriormente.

---

# 5.7 Operação `IO:n`

A operação `IO:n` representa uma operação de Entrada/Saída com duração de `n` unidades de tempo.

Exemplo:

```text
IO:4
```

Quando um processo em `RUNNING` atingir uma operação `IO:n`, o simulador deverá:

1. concluir o processamento da operação anterior;
2. preservar o contexto do processo;
3. registrar a duração da E/S;
4. registrar o instante de conclusão previsto;
5. alterar o estado de `RUNNING` para `BLOCKED`;
6. remover o processo da CPU;
7. impedir que o processo seja selecionado pelo escalonador enquanto estiver bloqueado.

Transição:

```text
RUNNING
   │
   │ IO:n
   ▼
BLOCKED
```

Durante o período de E/S, o processo não deverá utilizar a CPU.

Quando a duração da E/S for concluída:

```text
BLOCKED
   │
   │ E/S concluída
   ▼
READY
```

O contador de operações deverá avançar para a próxima operação quando a E/S for concluída.

A conclusão da E/S não deverá fazer o processo entrar diretamente em `RUNNING`.

---

# 5.8 Operação `EXIT`

A operação `EXIT` representa o término normal do processo.

Quando o processo atingir `EXIT` enquanto estiver em `RUNNING`, o simulador deverá:

1. alterar seu estado para `TERMINATED`;
2. registrar o instante de término;
3. remover o processo da estrutura utilizada pelo escalonador;
4. liberar a CPU;
5. preservar suas informações no PCB;
6. manter seus dados disponíveis para as estatísticas finais.

Transição:

```text
RUNNING
   │
   │ EXIT
   ▼
TERMINATED
```

Um processo em `TERMINATED` não poderá voltar a qualquer outro estado.

---

# 5.9 Configuração da Simulação

Antes do início da execução, o simulador deverá permitir selecionar o algoritmo de escalonamento.

As opções disponíveis deverão ser:

```text
1 - Round Robin
2 - Prioridade Dinâmica
```

### Round Robin

Quando Round Robin for selecionado, o usuário deverá informar o quantum.

Exemplo:

```text
Algoritmo: Round Robin
Quantum: 3
```

O quantum deverá ser um número inteiro positivo.

### Prioridade Dinâmica

Quando Prioridade Dinâmica for selecionado, o simulador deverá utilizar:

- prioridade inicial definida no arquivo;
- prioridade efetiva;
- mecanismo de aging;
- desempate por FCFS;
- preempção por prioridade, conforme definido na seção 4.

A configuração do aging deverá utilizar os parâmetros definidos na especificação do escalonador.

A escolha do algoritmo deverá permanecer fixa durante toda a simulação.

---

# 5.10 Saída do Simulador

Ao final da execução, o simulador deverá apresentar informações suficientes para verificar o comportamento dos processos, da CPU e do algoritmo de escalonamento.

A saída deverá conter, no mínimo:

1. algoritmo utilizado;
2. quantum utilizado, quando aplicável;
3. gráfico de Gantt textual;
4. log das transições de estado;
5. estatísticas de utilização da CPU;
6. estatísticas individuais dos processos;
7. quantidade de mudanças de contexto;
8. instante de criação dos processos;
9. instante de término dos processos.

A saída deverá ser apresentada de maneira estruturada e legível.

---

# 5.11 Gráfico de Gantt Textual

O simulador deverá gerar um gráfico de Gantt em formato textual representando a utilização da CPU ao longo do tempo.

Cada intervalo deverá indicar o processo que utilizou a CPU naquele período.

Exemplo:

```text
Tempo:  0 1 2 3 4 5 6 7 8 9 10 11

CPU:   P1 P1 P1 P2 P2 P3 P3 P3 P1 P1 P2 P2
```

Também poderá ser apresentada uma representação agrupada:

```text
0────3────5────8────10────12
│ P1 │ P2 │ P3 │ P1 │ P2  │
```

Quando a CPU não estiver executando nenhum processo, deverá ser utilizado o identificador:

```text
IDLE
```

Exemplo:

```text
0──2──7──9──11
│P1│ IDLE │P2│
```

O período `IDLE` deverá ser contabilizado como tempo ocioso da CPU.

O gráfico de Gantt deverá ser consistente com o log de execução.

---

# 5.12 Log das Transições de Estado

O simulador deverá registrar todas as mudanças de estado dos processos.

Cada registro deverá informar, no mínimo:

- instante da mudança;
- PID;
- estado anterior;
- estado novo;
- motivo da transição.

Exemplo:

```text
[t=0] P1: READY -> RUNNING | escalonador
[t=2] P1: RUNNING -> READY  | quantum expirado
[t=2] P2: READY -> RUNNING | escalonador
[t=4] P2: RUNNING -> BLOCKED | solicitação de E/S
[t=4] P3: READY -> RUNNING | escalonador
[t=7] P2: BLOCKED -> READY | E/S concluída
[t=8] P3: RUNNING -> TERMINATED | EXIT
```

O log também deverá registrar eventos relevantes do escalonador, como:

- seleção de processo;
- preempção;
- expiração de quantum;
- conclusão de E/S;
- mudança de prioridade efetiva por aging;
- mudança de contexto.

Exemplo:

```text
[t=6] Aging | P1: prioridade efetiva 2 -> 3
[t=6] Preempção | P2 -> P1
```

O log deverá permitir verificar se as regras das seções anteriores estão sendo respeitadas.

---

# 5.13 Estatísticas da CPU

Ao final da simulação, deverão ser calculadas estatísticas relacionadas à utilização da CPU.

Deverão ser apresentados, no mínimo:

- tempo total da simulação;
- tempo em que a CPU esteve ocupada;
- tempo em que a CPU esteve ociosa;
- percentual de utilização da CPU;
- quantidade de mudanças de contexto.

A utilização da CPU deverá ser calculada por:

```text
Utilização da CPU =
(Tempo de CPU ocupada / Tempo total da simulação) × 100
```

Exemplo:

```text
Tempo total:       20
CPU ocupada:       16
CPU ociosa:         4

Utilização: 80%
```

O tempo de CPU ocupada deverá corresponder à soma dos intervalos em que algum processo esteve efetivamente em `RUNNING`.

O tempo de CPU ociosa deverá corresponder aos intervalos em que não havia processo executando.

Deverá ser respeitada a relação:

```text
Tempo total =
Tempo de CPU ocupada + Tempo de CPU ociosa
```

---

# 5.14 Estatísticas dos Processos

Para cada processo, o simulador deverá apresentar informações relacionadas à sua execução.

Exemplo:

```text
PID    CPU Time    Waiting Time    Turnaround Time
--------------------------------------------------
P1        8             4                 12
P2        6             5                 11
P3        5             7                 12
```

Deverão ser calculados, no mínimo:

### Tempo de CPU

Quantidade total de unidades de tempo durante as quais o processo utilizou efetivamente a CPU.

Esse valor deverá corresponder ao campo `cpuTime` do PCB.

---

### Tempo de Espera

Quantidade total de unidades de tempo durante as quais o processo permaneceu em `READY` aguardando a CPU.

O período em `BLOCKED` não deverá ser contabilizado como tempo de espera pela CPU.

---

### Turnaround Time

Tempo total entre a criação e o término do processo.

A fórmula será:

```text
Turnaround Time =
Instante de término - Instante de criação
```

Como os processos carregados inicialmente são criados em `t = 0`, seus respectivos turnaround times serão iguais ao instante em que terminarem.

---

### Tempo de E/S

O simulador deverá também registrar, quando aplicável, o tempo total em que o processo permaneceu realizando operações de E/S.

Esse valor deverá ser mantido separado do `waitingTime`.

---

# 5.15 Casos de Teste

Os testes deverão verificar individualmente os principais mecanismos do simulador.

Cada caso deverá possuir:

- objetivo;
- entrada;
- configuração;
- comportamento esperado;
- critérios de aprovação.

Os arquivos utilizados nos testes deverão ser controlados para permitir a comparação entre o resultado esperado e o resultado produzido pelo simulador.

---

## Caso de Teste 1 — Processo Único

### Objetivo

Verificar o funcionamento básico da CPU virtual, a execução de uma operação `CPU` e o término do processo.

### Entrada

```text
1;3;CPU:5 EXIT
```

### Configuração

Qualquer algoritmo disponível.

### Comportamento esperado

```text
P1: READY → RUNNING → TERMINATED
```

A CPU deverá permanecer ocupada durante as cinco unidades de CPU.

Resultado esperado:

```text
CPU Time = 5
Waiting Time = 0
Turnaround Time = 5
```

Não deverá ocorrer E/S ou bloqueio.

---

## Caso de Teste 2 — Round Robin

### Objetivo

Verificar o funcionamento da fila circular e da expiração do quantum.

### Entrada

```text
1;3;CPU:6 EXIT
2;3;CPU:4 EXIT
3;3;CPU:3 EXIT
```

### Configuração

```text
Algoritmo: Round Robin
Quantum: 2
```

### Ordem esperada de execução

```text
P1 → P2 → P3 → P1 → P2 → P3 → P1 → P2 → P1
```

A sequência deverá respeitar a seguinte lógica:

```text
t=0  P1
t=2  P2
t=4  P3
t=6  P1
t=8  P2
t=10 P3
t=11 P1
t=13 P2
t=14 P1
```

O último intervalo de cada processo poderá ser menor que o quantum caso o processo termine antes de completá-lo.

Os processos que sofrerem preempção por quantum deverão retornar ao final da fila.

---

## Caso de Teste 3 — Operações de E/S

### Objetivo

Verificar as transições `RUNNING → BLOCKED → READY`.

### Entrada

```text
1;3;CPU:2 IO:3 CPU:2 EXIT
2;2;CPU:4 EXIT
```

### Configuração

```text
Algoritmo: Round Robin
Quantum: 10
```

### Comportamento esperado

A execução deverá apresentar, conceitualmente:

```text
P1: READY → RUNNING
P1: RUNNING → BLOCKED
P2: READY → RUNNING
P1: BLOCKED → READY
P2: RUNNING → TERMINATED
P1: READY → RUNNING
P1: RUNNING → TERMINATED
```

Enquanto `P1` estiver em `BLOCKED`, ele não poderá utilizar a CPU.

O período de E/S de `P1` deverá durar exatamente três unidades de tempo.

---

## Caso de Teste 4 — Prioridade

### Objetivo

Verificar a seleção baseada na prioridade inicial.

### Entrada

```text
1;1;CPU:4 EXIT
2;5;CPU:3 EXIT
3;3;CPU:2 EXIT
```

### Configuração

```text
Algoritmo: Prioridade Dinâmica
```

Como todos os processos estarão `READY` no início e possuirão prioridades diferentes, a ordem esperada de seleção será:

```text
P2 → P3 → P1
```

O processo `P2` deverá ser selecionado primeiro por possuir prioridade 5.

---

## Caso de Teste 5 — Prevenção de Starvation por Aging

### Objetivo

Verificar se o mecanismo de aging aumenta progressivamente a prioridade efetiva de um processo que permanece aguardando.

### Entrada

```text
1;1;CPU:8 EXIT
2;5;CPU:2 EXIT
3;5;CPU:2 EXIT
4;5;CPU:2 EXIT
```

### Configuração

```text
Algoritmo: Prioridade Dinâmica
```

O processo `P1` deverá iniciar com prioridade menor que os demais.

Enquanto permanecer em `READY`, sua prioridade efetiva deverá aumentar conforme as regras de aging.

O log deverá registrar as alterações de prioridade efetiva.

Exemplo:

```text
[t=2] Aging | P1: prioridade efetiva 1 -> 2
[t=4] Aging | P1: prioridade efetiva 2 -> 3
[t=6] Aging | P1: prioridade efetiva 3 -> 4
...
```

O teste deverá verificar que o processo de baixa prioridade não permaneça indefinidamente sem receber CPU.

A execução deverá ser considerada correta quando o processo tiver sua prioridade efetiva atualizada conforme a configuração de aging e puder disputar a CPU de acordo com essa nova prioridade.

---

## Caso de Teste 6 — CPU Ociosa

### Objetivo

Verificar o comportamento da CPU quando não existir nenhum processo `READY` ou `RUNNING`.

### Entrada

```text
1;3;CPU:2 IO:5 CPU:2 EXIT
```

### Configuração

```text
Algoritmo: Round Robin
Quantum: 10
```

Após as duas primeiras unidades de CPU, `P1` deverá entrar em `BLOCKED`.

Como não haverá outro processo pronto, a CPU deverá permanecer ociosa durante a operação de E/S.

Exemplo conceitual:

```text
Tempo: 0 1 2 3 4 5 6 7 8 9

CPU:   P1 P1 IDLE IDLE IDLE IDLE IDLE P1 P1
```

O tempo de CPU ociosa deverá ser contabilizado nas estatísticas.

---

## Caso de Teste 7 — Comparação dos Algoritmos

### Objetivo

Executar o mesmo conjunto de processos utilizando os dois algoritmos e comparar os resultados.

### Entrada

```text
1;2;CPU:6 EXIT
2;5;CPU:4 EXIT
3;3;CPU:5 EXIT
```

### Execução 1

```text
Algoritmo: Round Robin
Quantum: 2
```

### Execução 2

```text
Algoritmo: Prioridade Dinâmica
```

Os resultados deverão ser comparados considerando:

- ordem de execução;
- tempo de espera;
- tempo de CPU;
- turnaround time;
- utilização da CPU;
- quantidade de mudanças de contexto;
- quantidade de preempções.

O objetivo do teste será demonstrar que os diferentes algoritmos podem produzir diferentes ordens de execução e métricas para o mesmo conjunto de processos.

---

# 5.16 Caso de Teste 8 — Desempate por FCFS

### Objetivo

Verificar o comportamento do escalonador de prioridade quando dois processos possuem a mesma prioridade efetiva.

### Entrada

```text
1;5;CPU:3 EXIT
2;5;CPU:3 EXIT
3;2;CPU:2 EXIT
```

### Configuração

```text
Algoritmo: Prioridade Dinâmica
```

Como `P1` e `P2` possuem a mesma prioridade inicial e foram criados no mesmo instante, deverá ser utilizada a ordem de entrada no estado `READY`.

Resultado esperado:

```text
P1 → P2 → P3
```

Caso exista empate também no instante de entrada em `READY`, deverá ser utilizado o menor PID como último critério de desempate.

---

# 5.17 Caso de Teste 9 — Preempção por Prioridade

### Objetivo

Verificar se um processo com prioridade efetiva maior pode causar a preempção do processo atualmente em execução.

### Entrada

```text
1;2;CPU:8 EXIT
2;5;CPU:2 EXIT
```

O teste deverá ser configurado de modo que `P1` esteja executando quando `P2` entrar em `READY`.

Quando `P2` possuir prioridade efetiva maior que a prioridade efetiva de `P1`, deverá ocorrer:

```text
P1: RUNNING → READY
P2: READY → RUNNING
```

O contexto de `P1` deverá ser preservado para que sua execução possa continuar posteriormente.

O log deverá registrar a preempção.

---

# 5.18 Validação dos Resultados

Os resultados da simulação serão considerados válidos quando todas as condições abaixo forem atendidas:

1. Todos os processos válidos forem criados corretamente.
2. Cada processo possuir um PID único.
3. Cada processo possuir um PCB.
4. As operações forem executadas na ordem definida no arquivo.
5. Operações `CPU:n` consumirem exatamente `n` unidades de CPU.
6. Operações `IO:n` permanecerem bloqueadas durante exatamente `n` unidades de tempo.
7. `EXIT` colocar o processo em `TERMINATED`.
8. Processos `BLOCKED` não utilizarem a CPU.
9. O escalonador selecionar somente processos `READY`.
10. No máximo um processo permanecer em `RUNNING` por vez.
11. O Round Robin respeitar o quantum configurado.
12. Processos preemptados pelo Round Robin retornarem ao final da fila.
13. O escalonamento por prioridade respeitar a prioridade efetiva.
14. O aging alterar a prioridade efetiva conforme sua configuração.
15. O desempate de prioridades seguir a regra FCFS.
16. O último critério de desempate ser o menor PID quando necessário.
17. A preempção por prioridade ocorrer somente quando houver processo `READY` com prioridade efetiva maior que a do processo `RUNNING`.
18. Processos bloqueados retornarem para `READY` após a conclusão da E/S.
19. A CPU permanecer `IDLE` quando não houver processo executável.
20. O tempo de CPU ser contabilizado corretamente.
21. O tempo de espera contabilizar somente períodos em `READY`.
22. O tempo em `BLOCKED` não ser contabilizado como `waitingTime`.
23. O turnaround ser calculado corretamente.
24. O gráfico de Gantt corresponder à execução real.
25. O log representar todas as mudanças de estado.
26. As mudanças de contexto serem contabilizadas corretamente.
27. O processo em `TERMINATED` não voltar a executar.
28. As estatísticas finais serem consistentes com o log e o gráfico de Gantt.

---

# 5.19 Diretrizes de Entrega

O projeto deverá ser entregue acompanhado dos seguintes componentes:

- código-fonte completo do simulador;
- arquivo de tarefas utilizado nos testes;
- documentação da especificação em formato Markdown;
- exemplos de execução;
- resultados dos casos de teste.

A documentação deverá permitir compreender o funcionamento do simulador sem necessidade de analisar diretamente o código-fonte.

A execução deverá permitir identificar claramente:

- algoritmo de escalonamento utilizado;
- quantum, quando aplicável;
- configuração do aging, quando aplicável;
- processos envolvidos;
- sequência de operações;
- sequência de execução;
- mudanças de contexto;
- transições de estado;
- períodos de CPU ociosa;
- estatísticas individuais;
- estatísticas gerais da CPU.

---

# 5.20 Critérios Mínimos de Entrega

A implementação será considerada funcional quando atender, no mínimo, aos seguintes requisitos:

### Processos

- criação dos processos a partir do arquivo;
- PCB para cada processo;
- PID único;
- sequência de operações;
- estados `READY`, `RUNNING`, `BLOCKED` e `TERMINATED`.

### CPU

- CPU virtual;
- execução de operações `CPU:n`;
- contador de programa;
- registradores virtuais;
- mudança de contexto;
- relógio lógico.

### E/S

- operações `IO:n`;
- bloqueio durante a E/S;
- conclusão da E/S;
- retorno para `READY`.

### Escalonamento

- Round Robin;
- quantum configurável;
- fila circular;
- prioridade dinâmica;
- aging;
- FCFS para desempate;
- preempção por prioridade.

### Observabilidade

- gráfico de Gantt textual;
- log de transições;
- estatísticas da CPU;
- estatísticas por processo;
- quantidade de mudanças de contexto.

### Validação

- casos de teste documentados;
- comportamento determinístico;
- resultados consistentes entre log, Gantt e estatísticas.

A saída do simulador deverá ser suficientemente clara para permitir a verificação do funcionamento do gerenciamento de processos e dos algoritmos de escalonamento sem necessidade de inspeção direta do código-fonte.
