
import copy


class BankersAlgorithm:
    def __init__(self, process_names, total_resources, allocation_matrix, max_matrix):
        """
        Inicializa o simulador do Algoritmo do Banqueiro.
        """
        self.process_names = process_names
        self.num_processes = len(process_names)
        self.num_resources = len(total_resources)
        self.total_resources = list(total_resources)
        self.allocation = copy.deepcopy(allocation_matrix)
        self.max_matrix = copy.deepcopy(max_matrix)

        self.aluno = "LUIS FERNANDO SOARES SALES"

        # Calcular a matriz de necessidade: Need = Max - Allocation
        self.need = [
            [
                self.max_matrix[i][j] - self.allocation[i][j]
                for j in range(self.num_resources)
            ]
            for i in range(self.num_processes)
        ]

        # Calcular os recursos disponíveis: Available = Total - Alocados
        self.available = list(self.total_resources)

        for j in range(self.num_resources):
            allocated_sum = sum(
                self.allocation[i][j]
                for i in range(self.num_processes)
            )
            self.available[j] -= allocated_sum

    def print_cabecalho(self, titulo):
        """Exibe o nome do aluno e o título do teste."""
        print("\n" + "=" * 70)
        print(f"ALUNO: {self.aluno}")
        print(f"TESTE: {titulo}")
        print("=" * 70)

    def display_state(self):
        """Exibe o estado atual do sistema."""
        print("=" * 70)
        print("ESTADO ATUAL DO SISTEMA")
        print(f"ALUNO: {self.aluno}")
        print("=" * 70)

        print(f"Recursos Totais (E):      {self.total_resources}")
        print(f"Recursos Disponíveis (A): {self.available}")
        print("-" * 70)

        print(
            f"{'Processo':<10} | {'Alocado (C)':<15} | "
            f"{'Máximo (Max)':<15} | {'Necessidade (Need)':<18}"
        )
        print("-" * 70)

        for i in range(self.num_processes):
            p_name = self.process_names[i]
            alloc_str = str(self.allocation[i])
            max_str = str(self.max_matrix[i])
            need_str = str(self.need[i])

            print(
                f"{p_name:<10} | {alloc_str:<15} | "
                f"{max_str:<15} | {need_str:<18}"
            )

        print("=" * 70)

    def is_safe_state(self, verbose=True):
        """
        Verifica se o sistema está em estado seguro.
        Retorna (True, sequência segura) ou (False, lista vazia).
        """
        work = list(self.available)
        finish = [False] * self.num_processes
        safe_sequence = []

        if verbose:
            print("\n[VERIFICAÇÃO DE ESTADO SEGURO]")
            print(f"Aluno: {self.aluno}")
            print(f"Vetor de Trabalho Inicial (Work): {work}\n")

        step = 1

        while len(safe_sequence) < self.num_processes:
            found_candidate = False

            for i in range(self.num_processes):
                if not finish[i]:
                    # Verificar se Need[i] <= Work
                    can_satisfy = all(
                        self.need[i][j] <= work[j]
                        for j in range(self.num_resources)
                    )

                    if can_satisfy:
                        if verbose:
                            print(
                                f"Passo {step}: "
                                f"{self.process_names[i]} pode ser atendido!"
                            )
                            print(
                                f"  Necessidade {self.need[i]} "
                                f"<= Disponível {work}"
                            )
                            print(
                                f"  {self.process_names[i]} executa e libera "
                                f"seus recursos: {self.allocation[i]}"
                            )

                        # Simular a liberação dos recursos do processo
                        for j in range(self.num_resources):
                            work[j] += self.allocation[i][j]

                        finish[i] = True
                        safe_sequence.append(self.process_names[i])
                        found_candidate = True
                        step += 1

                        if verbose:
                            print(f"  Novo Vetor de Trabalho (Work): {work}\n")

                        break

            if not found_candidate:
                if verbose:
                    print(
                        "ERRO: Nenhum processo pendente pode ser "
                        "atendido com os recursos disponíveis."
                    )
                    print("O SISTEMA ENCONTRA-SE EM UM ESTADO INSEGURO!")
                    print(f"ALUNO: {self.aluno}")

                return False, []

        if verbose:
            print("SUCESSO: O sistema está em um ESTADO SEGURO!")
            print(
                "Sequência Segura de Execução: "
                + " -> ".join(safe_sequence)
            )
            print(f"ALUNO: {self.aluno}")

        return True, safe_sequence

    def request_resources(self, process_index, request_vector):
        """
        Analisa uma solicitação de recursos de um processo.
        """
        # Validar o índice do processo
        if not 0 <= process_index < self.num_processes:
            print("ERRO: Índice de processo inválido.")
            print(f"ALUNO: {self.aluno}")
            return False

        # Validar o tamanho do vetor de solicitação
        if len(request_vector) != self.num_resources:
            print("ERRO: O vetor de solicitação possui tamanho inválido.")
            print(f"ALUNO: {self.aluno}")
            return False

        # Impedir quantidades negativas
        if any(resource < 0 for resource in request_vector):
            print("ERRO: A solicitação não pode conter valores negativos.")
            print(f"ALUNO: {self.aluno}")
            return False

        p_name = self.process_names[process_index]

        print("\n" + "#" * 70)
        print(f"ALUNO: {self.aluno}")
        print(f"SOLICITAÇÃO DE RECURSOS PELO PROCESSO {p_name}: {request_vector}")
        print("#" * 70)

        # Passo 1: verificar se a solicitação não ultrapassa a necessidade
        for j in range(self.num_resources):
            if request_vector[j] > self.need[process_index][j]:
                print(
                    f"REQUISIÇÃO NEGADA: {p_name} solicitou mais "
                    "do que sua necessidade máxima declarada."
                )
                print(
                    f"Solicitado: {request_vector[j]} > "
                    f"Necessidade: {self.need[process_index][j]} "
                    f"para o recurso R{j}"
                )
                print(f"ALUNO: {self.aluno}")
                return False

        # Passo 2: verificar se os recursos estão disponíveis
        for j in range(self.num_resources):
            if request_vector[j] > self.available[j]:
                print(
                    "PROCESSO BLOQUEADO: Recursos insuficientes "
                    "disponíveis no momento."
                )
                print(
                    f"Solicitado: {request_vector[j]} > "
                    f"Disponível: {self.available[j]} para o recurso R{j}"
                )
                print(
                    f"{p_name} deve aguardar a liberação de recursos "
                    "por outros processos."
                )
                print(f"ALUNO: {self.aluno}")
                return False

        # Passo 3: realizar uma alocação provisória
        print(
            "TENTATIVA PROVISÓRIA: Recursos disponíveis. "
            "Testando a alocação..."
        )

        for j in range(self.num_resources):
            self.available[j] -= request_vector[j]
            self.allocation[process_index][j] += request_vector[j]
            self.need[process_index][j] -= request_vector[j]

        # Passo 4: verificar a segurança do novo estado
        is_safe, sequence = self.is_safe_state(verbose=True)

        if is_safe:
            print(f"\nREQUISIÇÃO CONCEDIDA A {p_name}!")
            print("O estado resultante permanece SEGURO.")
            print(f"ALUNO: {self.aluno}")
            return True

        # Se o estado for inseguro, desfazer a alocação provisória
        print(f"\nREQUISIÇÃO NEGADA A {p_name}!")
        print(
            "A alocação levaria a um estado inseguro. "
            "Efetuando rollback..."
        )

        for j in range(self.num_resources):
            self.available[j] += request_vector[j]
            self.allocation[process_index][j] -= request_vector[j]
            self.need[process_index][j] += request_vector[j]

        print("Estado original restaurado. O processo deve aguardar.")
        print(f"ALUNO: {self.aluno}")

        return False


def run_demo():
    # Dados do sistema
    process_names = ["P0", "P1", "P2", "P3", "P4"]
    total_resources = [10, 5, 7]

    # Matriz de alocação atual
    allocation = [
        [0, 1, 0],  # P0
        [2, 0, 0],  # P1
        [3, 0, 2],  # P2
        [2, 1, 1],  # P3
        [0, 0, 2]   # P4
    ]

    # Matriz de necessidade máxima
    max_matrix = [
        [7, 5, 3],  # P0
        [3, 2, 2],  # P1
        [9, 0, 2],  # P2
        [2, 2, 2],  # P3
        [4, 3, 3]   # P4
    ]

    # Criar o simulador
    banker = BankersAlgorithm(
        process_names,
        total_resources,
        allocation,
        max_matrix
    )

    print("=" * 70)
    print("SIMULAÇÃO DO ALGORITMO DO BANQUEIRO")
    print("Referência: Tanenbaum & Bos - Sistemas Operacionais Modernos")
    print(f"ALUNO: {banker.aluno}")
    print("=" * 70)

    # TESTE 1: exibir o estado inicial
    banker.print_cabecalho("TESTE 1 - ESTADO INICIAL")
    banker.display_state()

    # TESTE 2: verificar se o estado inicial é seguro
    banker.print_cabecalho("TESTE 2 - VERIFICAÇÃO DE ESTADO SEGURO")
    banker.is_safe_state(verbose=True)

    # TESTE 3: requisição válida e segura de P1
    banker.print_cabecalho("TESTE 3 - REQUISIÇÃO SEGURA DE P1")
    banker.request_resources(
        process_index=1,
        request_vector=[1, 0, 2]
    )
    banker.display_state()

    # TESTE 4: requisição de P4 com recursos insuficientes
    banker.print_cabecalho("TESTE 4 - REQUISIÇÃO DE P4")
    banker.request_resources(
        process_index=4,
        request_vector=[3, 3, 0]
    )
    banker.display_state()


if __name__ == "__main__":
    run_demo()
