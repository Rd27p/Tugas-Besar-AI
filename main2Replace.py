import random
import math

# Parameter GA
POP_SIZE = 10
CHROM_LENGTH = 10
GEN_MAX = 5
PC = 0.7
PM = 0.01
TOURNAMENT_SIZE = 4
REPLACEMENT_SIZE = 2  # jumlah kromosom terburuk yang akan direplace

def decode(chrom):
    half = len(chrom) // 2
    x1_bin = chrom[:half]
    x2_bin = chrom[half:]
    x1 = scale_binary(x1_bin, -10, 10)
    x2 = scale_binary(x2_bin, -10, 10)
    return x1, x2

def scale_binary(bin_str, min_val, max_val):
    dec = 0
    for i in range(len(bin_str)):
        bit = int(bin_str[i])
        power = len(bin_str) - i - 1
        dec += bit * (2 ** power)
    max_bin = (2 ** len(bin_str)) - 1
    return min_val + (dec / max_bin) * (max_val - min_val)

def objective(x1, x2):
    try:
        return -(math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + (3/4) * math.exp(1 - math.sqrt(x1**2)))
    except:
        return float('inf')

def fitness(chrom):
    x1, x2 = decode(chrom)
    return -objective(x1, x2)

def init_population():
    population = []
    for _ in range(POP_SIZE):
        chrom = ''.join(random.choice('01') for _ in range(CHROM_LENGTH))
        population.append(chrom)
    return population

def tournament_selection(pop, tournament_size=TOURNAMENT_SIZE):
    competitors = random.sample(pop, tournament_size)
    best = competitors[0]
    for individual in competitors[1:]:
        if fitness(individual) > fitness(best):
            best = individual
    return best

def crossover(p1, p2):
    if random.random() < PC:
        point = random.randint(1, CHROM_LENGTH - 1)
        return p1[:point] + p2[point:], p2[:point] + p1[point:]
    return p1, p2

def mutate(chrom):
    mutated = ''
    for bit in chrom:
        r = random.random()
        if r < PM:
            mutated += '1' if bit == '0' else '0'
        else:
            mutated += bit
    return mutated

def sort_by_fitness(pop):
    # Fungsi untuk mengurutkan berdasarkan fitness tanpa lambda
    def fitness_comparator(chrom1, chrom2):
        return fitness(chrom2) - fitness(chrom1)
    
    for i in range(len(pop)):
        for j in range(i + 1, len(pop)):
            if fitness_comparator(pop[j], pop[i]) > 0:
                pop[i], pop[j] = pop[j], pop[i]
    return pop

def algoritma_genetik():
    population = init_population()

    # Menampilkan kromosom awal
    print("=== Populasi Awal ===")
    for i, chrom in enumerate(population):
        x1, x2 = decode(chrom)
        print(f"{i+1:2d}. {chrom} -> x1={x1:.2f}, x2={x2:.2f}, fitness={fitness(chrom):.4f}")
    print("======================\n")

    # Menyimpan kromosom terbaik awal
    best_chrom = population[0]
    for chrom in population[1:]:
        if objective(*decode(chrom)) < objective(*decode(best_chrom)):
            best_chrom = chrom

    for gen in range(GEN_MAX):
        offspring = []

        while len(offspring) < REPLACEMENT_SIZE:
            p1 = tournament_selection(population)
            p2 = tournament_selection(population)
            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1)
            c2 = mutate(c2)
            offspring.append(c1)
            if len(offspring) < REPLACEMENT_SIZE:
                offspring.append(c2)

        # Pertahankan kromosom terbaik
        sorted_pop = sort_by_fitness(population)
        survivors = sorted_pop[:POP_SIZE - REPLACEMENT_SIZE]
        replaced = sorted_pop[POP_SIZE - REPLACEMENT_SIZE:]  # yang digantikan

        # Logging kromosom yang diganti
        print(f"Generasi {gen + 1}: {REPLACEMENT_SIZE} kromosom diganti:")
        for idx, chrom in enumerate(replaced):
            print(f"  Ganti: {chrom} -> ", end='')
            if idx < len(offspring):
                print(f"{offspring[idx]}")
            else:
                print("(tidak ada pengganti)")
        print()

        # Gabungkan survivor dan anak-anak
        population = survivors + offspring

        # Update best chrom
        for chrom in population:
            if objective(*decode(chrom)) < objective(*decode(best_chrom)):
                best_chrom = chrom

        # Tampilkan populasi saat ini
        print(f"=== Populasi Generasi {gen + 1} ===")
        for i, chrom in enumerate(population):
            x1, x2 = decode(chrom)
            print(f"{i+1:2d}. {chrom} -> x1={x1:.2f}, x2={x2:.2f}, fitness={fitness(chrom):.4f}")
        print("===============================\n")

    x1, x2 = decode(best_chrom)

    # Menampilkan hasil akhir
    print("\n=== Hasil Akhir ===")
    print("Kromosom terbaik:", best_chrom)
    print("x1 =", x1)
    print("x2 =", x2)
    print("Nilai fungsi =", objective(x1, x2))

# Jalankan program
algoritma_genetik()
