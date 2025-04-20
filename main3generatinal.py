import random
import math

# Parameter GA
POP_SIZE = 10  # Ukuran populasi
CHROM_LENGTH = 10
GEN_MAX = 5  # Jumlah generasi
PC = 0.7
PM = 0.01
TOURNAMENT_SIZE = 4
REPLACEMENT_SIZE = 10  # Mengganti seluruh populasi setiap generasi

# Fungsi decode kromosom ke x1 dan x2
def decode(chrom):
    half = len(chrom) // 2
    x1_bin = chrom[:half]
    x2_bin = chrom[half:]
    x1 = scale_binary(x1_bin, -10, 10)
    x2 = scale_binary(x2_bin, -10, 10)
    return x1, x2

def scale_binary(bin_str, min_val, max_val):
    dec = sum(int(bit) * (2 ** (len(bin_str) - i - 1)) for i, bit in enumerate(bin_str))
    max_bin = (2 ** len(bin_str)) - 1
    proporsi = dec / max_bin
    return min_val + proporsi * (max_val - min_val)

# Fungsi objektif (diminimalkan)
def objective(x1, x2):
    try:
        return -(math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + (3/4) * math.exp(1 - math.sqrt(x1**2)))
    except:
        return float('inf')

# Fitness adalah negatif dari fungsi objektif
def fitness(chrom):
    x1, x2 = decode(chrom)
    return -objective(x1, x2)

# Inisialisasi populasi
def init_population():
    return [''.join(random.choice('01') for _ in range(CHROM_LENGTH)) for _ in range(POP_SIZE)]

# Seleksi Tournament
def tournament_selection(pop):
    competitors = random.sample(pop, TOURNAMENT_SIZE)
    return max(competitors, key=fitness)

# Crossover
def crossover(p1, p2):
    if random.random() < PC:
        point = random.randint(1, CHROM_LENGTH - 1)
        return p1[:point] + p2[point:], p2[:point] + p1[point:]
    return p1, p2

# Mutasi
def mutate(chrom):
    return ''.join(
        '1' if bit == '0' and random.random() < PM else
        '0' if bit == '1' and random.random() < PM else
        bit
        for bit in chrom
    )

# Algoritma utama
def algoritma_genetik():
    population = init_population()

    # Tampilkan populasi awal
    print("=== Populasi Awal ===")
    for i, chrom in enumerate(population):
        x1, x2 = decode(chrom)
        print(f"{i+1:2d}. {chrom} -> x1={x1:.2f}, x2={x2:.2f}, fitness={fitness(chrom):.4f}")
    print("======================\n")

    best_overall = population[0]

    for gen in range(GEN_MAX):
        offspring = []

        print(f"=== Proses Generasi {gen + 1} ===")
        while len(offspring) < REPLACEMENT_SIZE:
            p1 = tournament_selection(population)
            p2 = tournament_selection(population)
            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1)
            c2 = mutate(c2)

            # Tampilkan proses pergantian
            p1_x1, p1_x2 = decode(p1)
            p2_x1, p2_x2 = decode(p2)
            c1_x1, c1_x2 = decode(c1)
            c2_x1, c2_x2 = decode(c2)

            print(f"Parent 1: {p1} -> x1={p1_x1:.2f}, x2={p1_x2:.2f}")
            print(f"Parent 2: {p2} -> x1={p2_x1:.2f}, x2={p2_x2:.2f}")
            print(f"Child  1: {c1} -> x1={c1_x1:.2f}, x2={c1_x2:.2f}")
            print(f"Child  2: {c2} -> x1={c2_x1:.2f}, x2={c2_x2:.2f}")
            print("-" * 40)

            offspring.append(c1)
            if len(offspring) < REPLACEMENT_SIZE:
                offspring.append(c2)
        print()

        population = offspring[:POP_SIZE]

        print(f"=== Generasi {gen + 1} ===")
        for i, chrom in enumerate(population):
            x1, x2 = decode(chrom)
            print(f"{i+1:2d}. {chrom} -> x1={x1:.2f}, x2={x2:.2f}, fitness={fitness(chrom):.4f}")
        print("======================\n")

        for chrom in population:
            if fitness(chrom) > fitness(best_overall):
                best_overall = chrom

    # Tampilkan hasil akhir
    x1, x2 = decode(best_overall)
    print("\n=== Hasil Akhir ===")
    print("Kromosom terbaik:", best_overall)
    print("x1 =", x1)
    print("x2 =", x2)
    print("Nilai fungsi =", objective(x1, x2))
    print("Fitness =", fitness(best_overall))

# Jalankan
algoritma_genetik()
