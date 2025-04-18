import random
import math

# Parameter GA
POP_SIZE = 20
CHROM_LENGTH = 20
GEN_MAX = 100
PC = 0.7
PM = 0.01

# Fungsi untuk meng-decode kromosom ke nilai x1, x2
def decode(chrom):
    half = len(chrom) // 2
    x1_bin = chrom[:half]
    x2_bin = chrom[half:]
    x1 = scale_binary(x1_bin, -10, 10)
    x2 = scale_binary(x2_bin, -10, 10)
    return x1, x2

def scale_binary(bin_str, min_val, max_val):
    max_bin = 2**len(bin_str) - 1
    dec = int(bin_str, 2)
    return min_val + (dec / max_bin) * (max_val - min_val)

# Fungsi objektif
def objective(x1, x2):
    try:
        return -(math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + (3/4) * math.exp(1 - math.sqrt(x1**2)))
    except:
        return float('inf')  # jika error tan tak terdefinisi

# Evaluasi fitness
def fitness(chrom):
    x1, x2 = decode(chrom)
    return -objective(x1, x2)  # karena ingin minimisasi, jadi negasi nilai fungsi

# Inisialisasi populasi acak
def init_population():
    return [''.join(random.choice('01') for _ in range(CHROM_LENGTH)) for _ in range(POP_SIZE)]

# Tournament selection
def select_parent(pop):
    a = random.choice(pop)
    b = random.choice(pop)
    return a if fitness(a) > fitness(b) else b

# Crossover
def crossover(p1, p2):
    if random.random() < PC:
        point = random.randint(1, CHROM_LENGTH - 1)
        return p1[:point] + p2[point:], p2[:point] + p1[point:]
    else:
        return p1, p2

# Mutasi
def mutate(chrom):
    return ''.join(bit if random.random() > PM else '1' if bit == '0' else '0' for bit in chrom)

# Algoritma utama
def genetic_algorithm():
    population = init_population()
    best_chrom = min(population, key=lambda c: objective(*decode(c)))

    for gen in range(GEN_MAX):
        new_pop = []
        while len(new_pop) < POP_SIZE:
            p1 = select_parent(population)
            p2 = select_parent(population)
            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1)
            c2 = mutate(c2)
            new_pop.extend([c1, c2])
        population = new_pop[:POP_SIZE]
        current_best = min(population, key=lambda c: objective(*decode(c)))
        if objective(*decode(current_best)) < objective(*decode(best_chrom)):
            best_chrom = current_best

    x1, x2 = decode(best_chrom)
    print("Kromosom terbaik:", best_chrom)
    print("x1 =", x1)
    print("x2 =", x2)
    print("Nilai fungsi =", objective(x1, x2))

# Jalankan program
genetic_algorithm()