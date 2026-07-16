import os
import sys
import time

def parse_pla(file_path):
    num_inputs = 0
    minterms = set()
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('.i'):
                num_inputs = int(line.split()[1])
            elif line.startswith('.e'):
                break
            elif not line.startswith('.'):
                parts = line.split()
                if len(parts) >= 2 and parts[1] == '1':
                    minterms.add(parts[0])
    return num_inputs, minterms

def combine_terms(term1, term2):
    diff_count = 0
    diff_index = -1
    for i in range(len(term1)):
        if term1[i] != term2[i]:
            diff_count += 1
            diff_index = i
    if diff_count == 1:
        chars = list(term1)
        chars[diff_index] = '-'
        return "".join(chars)
    return None

def find_prime_implicants(num_inputs, minterms):
    current_level = {m: {int(m, 2)} for m in minterms}
    prime_implicants = {}
    while current_level:
        next_level = {}
        combined_this_round = set()
        groups = {}
        for term in current_level:
            ones = term.count('1')
            groups.setdefault(ones, []).append(term)
        for i in range(num_inputs):
            g1 = groups.get(i, [])
            g2 = groups.get(i + 1, [])
            for t1 in g1:
                for t2 in g2:
                    new_term = combine_terms(t1, t2)
                    if new_term:
                        combined_this_round.add(t1)
                        combined_this_round.add(t2)
                        combined_coverage = current_level[t1] | current_level[t2]
                        next_level[new_term] = combined_coverage
        for term, coverage in current_level.items():
            if term not in combined_this_round:
                prime_implicants[term] = coverage
        current_level = next_level
    return prime_implicants

def select_essential_primes(minterms, prime_implicants):
    essential_primes = {}
    target_minterms = [int(m, 2) for m in minterms]
    for minterm in target_minterms:
        covertures = []
        for prime, covered_set in prime_implicants.items():
            if minterm in covered_set:
                covertures.append((prime, covered_set))
        if len(covertures) == 1:
            prime, covered_set = covertures[0]
            if prime not in essential_primes:
                essential_primes[prime] = covered_set
    return essential_primes

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erro: Não informou o arquivo .pla!")
        print("Uso correto: python quine_mccluskey.py <nome_do_arquivo.pla>")
        sys.exit(1)

    atividade = sys.argv[1]
    
    if os.path.exists(atividade):
        inputs, termos = parse_pla(atividade)
        
        inicio = time.perf_counter()
        
        todos_primos = find_prime_implicants(inputs, termos)
        primos_essenciais = select_essential_primes(termos, todos_primos)
        
        fim = time.perf_counter()
        
        tempo_total = fim - inicio

        print(f"\nResultado da Minimização ({atividade})")
        for termo, cobertura in primos_essenciais.items():
            print(f"Termo Binário: {termo} (Cobre os mintermos: {list(cobertura)})")
            
        print("-" * 50)
        print(f"Tempo de execução: {tempo_total:.6f} segundos.")
        print("-" * 50)
    else:
        print(f"Erro: O arquivo '{atividade}' não foi encontrado neste diretório!")
