import random
import math

# Parameter GA
POP_SIZE = 20
CHROM_LENGTH = 10
GEN_MAX = 100
PC = 0.7
PM = 0.01
TOURNAMENT_SIZE = 4

# Fungsi untuk meng-decode kromosom ke nilai x1, x2
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
    proporsi = dec / max_bin
    nilai_skala = min_val + proporsi * (max_val - min_val)
    return nilai_skala

# Fungsi objektif
def objective(x1, x2):
    try:
        return -(math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + (3/4) * math.exp(1 - math.sqrt(x1**2)))
    except:
        return float('inf')

# Perhitungan fitness
def fitness(chrom):
    x1, x2 = decode(chrom)
    return -objective(x1, x2)

# Inisialisasi populasi awal
def init_population():
    population = [] 
    for _ in range(POP_SIZE):
        chrom = '' 
        for _ in range(CHROM_LENGTH):
            chrom += random.choice('01')
        population.append(chrom)
    return population

# Seleksi Tournament
def tournament_selection(pop, tournament_size=TOURNAMENT_SIZE):
    competitors = random.sample(pop, tournament_size)
    best_fitness = -math.inf 
    best_individual = None
    for individual in competitors:
        individual_fitness = fitness(individual)
        if individual_fitness > best_fitness:
            best_fitness = individual_fitness
            best_individual = individual
    return best_individual

# Crossover
def crossover(p1, p2):
    if random.random() < PC:
        point = random.randint(1, CHROM_LENGTH - 1)
        return p1[:point] + p2[point:], p2[:point] + p1[point:]
    else:
        return p1, p2

# Mutasi
def mutate(chrom):
    mutated = ''
    for bit in chrom:
        r = random.random() 
        if r < PM:
            mutated += '1' if bit == '0' else '0'
        else:
            mutated += bit
    return mutated

# Algoritma utama
def algoritma_genetik():
    population = init_population()
    best_chrom = population[0]
    for chrom in population[1:]:
        if objective(*decode(chrom)) < objective(*decode(best_chrom)):
            best_chrom = chrom

    for gen in range(GEN_MAX):
        new_pop = []
        while len(new_pop) < POP_SIZE:
            p1 = tournament_selection(population)
            p2 = tournament_selection(population)
            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1)
            c2 = mutate(c2)
            new_pop.extend([c1, c2])
        population = new_pop[:POP_SIZE]

        # Cari best chrom di generasi sekarang
        current_best = population[0]
        for chrom in population[1:]:
            if objective(*decode(chrom)) < objective(*decode(current_best)):
                current_best = chrom

        if objective(*decode(current_best)) < objective(*decode(best_chrom)):
            best_chrom = current_best

    x1, x2 = decode(best_chrom)
    print("Kromosom terbaik:", best_chrom)
    print("x1 =", x1)
    print("x2 =", x2)
    print("Nilai fungsi =", objective(x1, x2))

# Jalankan program
algoritma_genetik()
