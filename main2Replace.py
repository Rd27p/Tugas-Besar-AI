import random
import math

# Parameter GA
POP_SIZE = 10
CHROM_LENGTH = 5
GEN_MAX = 5
PC = 0.7
PM = 0.01
TOURNAMENT_SIZE = 4
REPLACEMENT_SIZE = 2

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
    return [''.join(random.choice('01') for _ in range(CHROM_LENGTH)) for _ in range(POP_SIZE)]

def tournament_selection(pop, tournament_size=TOURNAMENT_SIZE):
    competitors = random.sample(pop, tournament_size)
    return max(competitors, key=fitness)

def crossover(p1, p2):
    if random.random() < PC:
        point = random.randint(1, CHROM_LENGTH - 1)
        return p1[:point] + p2[point:], p2[:point] + p1[point:]
    return p1, p2

def mutate(chrom):
    return ''.join('1' if bit == '0' and random.random() < PM else '0' if bit == '1' and random.random() < PM else bit for bit in chrom)

def sort_by_fitness(pop):
    return sorted(pop, key=fitness)

def algoritma_genetik():
    population = init_population()

    # Populasi awal
    print("=== Populasi Awal ===")
    for i, chrom in enumerate(population):
        x1, x2 = decode(chrom)
        print(f"{i+1:2d}. {chrom} -> x1={x1:.2f}, x2={x2:.2f}, fitness={fitness(chrom):.4f}")
    print("======================\n")

    best_chrom = min(population, key=lambda c: objective(*decode(c)))

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

        sorted_pop = sort_by_fitness(population)
        survivors = sorted_pop[:POP_SIZE - REPLACEMENT_SIZE]
        replaced = sorted_pop[POP_SIZE - REPLACEMENT_SIZE:]

        print(f"Generasi {gen + 1}: {REPLACEMENT_SIZE} kromosom dengan fitness terendah diganti:")
        for idx in range(REPLACEMENT_SIZE):
            print(f"  Ganti: {replaced[idx]} -> {offspring[idx]}")
        print()

        population = survivors + offspring

        # Update kromosom terbaik
        current_best = min(population, key=lambda c: objective(*decode(c)))
        if objective(*decode(current_best)) < objective(*decode(best_chrom)):
            best_chrom = current_best

        print(f"=== Populasi Generasi {gen + 1} ===")
        for i, chrom in enumerate(population):
            x1, x2 = decode(chrom)
            print(f"{i+1:2d}. {chrom} -> x1={x1:.2f}, x2={x2:.2f}, fitness={fitness(chrom):.4f}")
        print("===============================\n")

    x1, x2 = decode(best_chrom)
    print("\n=== Hasil Akhir ===")
    print("Kromosom terbaik:", best_chrom)
    print("x1 =", x1)
    print("x2 =", x2)
    print("Nilai fungsi =", objective(x1, x2))

# Jalankan program
algoritma_genetik()
