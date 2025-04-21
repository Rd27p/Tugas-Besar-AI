import random
import math

# Parameter GA
POP_SIZE = 10
CHROM_LENGTH = 10
GEN_MAX = 5
PC = 0.7
PM = 0.25
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
    # Mengubah biner ke desimal
    for i in range(len(bin_str)):
        bit = int(bin_str[i])
        power = len(bin_str) - i - 1
        dec += bit * (2 ** power)
    max_bin = (2 ** len(bin_str)) - 1 
    return min_val + (dec / max_bin) * (max_val - min_val)

def objective(x1, x2):
    try:
        return -(math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + (3 / 4) * math.exp(1 - math.sqrt(x1 ** 2)))
    except:
        return float('inf')

def fitness(chrom):
    x1, x2 = decode(chrom)
    return -objective(x1, x2)

def init_population():
    return [''.join(random.choice('01') for _ in range(CHROM_LENGTH)) for _ in range(POP_SIZE)]

def tournament_selection(pop, tournament_size=TOURNAMENT_SIZE):
    competitors = random.sample(pop, tournament_size)
    # Cari parent1 (fitness terkecil)
    parent1 = competitors[0]
    for comp in competitors[1:]:
        if fitness(comp) < fitness(parent1):
            parent1 = comp
            
    competitors.remove(parent1)

    # Cari parent2 (fitness terkecil kedua)
    parent2 = competitors[0]
    for comp in competitors[1:]:
        if fitness(comp) < fitness(parent2):
            parent2 = comp

    return parent1, parent2

def crossover(p1, p2):
    if random.random() < PC:
        point1 = random.randint(1, CHROM_LENGTH // 2)
        point2 = random.randint(CHROM_LENGTH // 2, CHROM_LENGTH - 1)

        c1 = p1[:point1] + p2[point1:point2] + p1[point2:]
        c2 = p2[:point1] + p1[point1:point2] + p2[point2:]

        # Pastikan crossover tidak menyebabkan perubahan yang terlalu besar
        c1_x1, c1_x2 = decode(c1)
        c2_x1, c2_x2 = decode(c2)

        # Pembatasan agar tidak keluar dari rentang yang diinginkan
        c1_x1 = max(-10, min(10, c1_x1))
        c1_x2 = max(-10, min(10, c1_x2))
        c2_x1 = max(-10, min(10, c2_x1))
        c2_x2 = max(-10, min(10, c2_x2))

        # Encode kembali menjadi kromosom
        c1 = ''.join([format(int((x - (-10)) / 20 * (2 ** (CHROM_LENGTH // 2)) + 0.5), '0' + str(CHROM_LENGTH // 2) + 'b') for x in [c1_x1, c1_x2]])
        c2 = ''.join([format(int((x - (-10)) / 20 * (2 ** (CHROM_LENGTH // 2)) + 0.5), '0' + str(CHROM_LENGTH // 2) + 'b') for x in [c2_x1, c2_x2]])

        return c1, c2
    return p1, p2

def mutate(chrom, PM):
    mutated_chrom = []  # Daftar untuk menyimpan kromosom yang telah dimutasi
    for bit in chrom:
        if bit == '0':  # Jika bit adalah '0'
            if random.random() < PM:  # Jika angka acak lebih kecil dari PM, lakukan mutasi
                mutated_chrom.append('1')  # Mutasi menjadi '1'
            else:
                mutated_chrom.append('0')  # Jika tidak, tetap '0'
        elif bit == '1':  # Jika bit adalah '1'
            if random.random() < PM:  # Jika angka acak lebih kecil dari PM, lakukan mutasi
                mutated_chrom.append('0')  # Mutasi menjadi '0'
            else:
                mutated_chrom.append('1')  # Jika tidak, tetap '1'

    return ''.join(mutated_chrom)  # Gabungkan kembali menjadi string kromosom yang telah dimutasi


def sort_by_fitness(pop):
    return sorted(pop, key=fitness)

def get_fitness(chrom):
    """ Fungsi untuk menghitung fitness dari kromosom """
    return fitness(chrom)

def algoritma_genetik():
    population = init_population()

    print("=== Populasi Awal ===")
    for i, chrom in enumerate(population):
        x1, x2 = decode(chrom)
        print(f"{i+1:2d}. {chrom} -> x1={x1:.2f}, x2={x2:.2f}, fitness={fitness(chrom):.4f}")
    print("======================\n")

    # Memilih kromosom terbaik berdasarkan fitness terbesar
    best_chrom = max(population, key=get_fitness)  

    for gen in range(GEN_MAX):
        offspring = []
        parent_data = []
        attempts = 0
        while len(offspring) < REPLACEMENT_SIZE and attempts < 10:
            p1, p2 = tournament_selection(population)  # Pastikan p1 dan p2 berbeda
            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1, PM)
            c2 = mutate(c2, PM)

            parent_data.append((p1, p2, c1, c2))

            # Memilih jika fitness anak lebih baik daripada orang tua
            if fitness(c1) < fitness(p1):  # Jika fitness anak 1 lebih buruk, pertahankan parent
                offspring.append(p1)
            else:
                offspring.append(c1)

            if len(offspring) < REPLACEMENT_SIZE and fitness(c2) < fitness(p2):  # Jika fitness anak 2 lebih buruk
                offspring.append(p2)
            else:
                offspring.append(c2)
            attempts += 1

        # Gabungkan populasi lama dan offspring dan hapus duplikasi
        combined_population = population + offspring
        unique_population = []
        for chrom in combined_population:
            if chrom not in unique_population:
                unique_population.append(chrom)

        # Pilih populasi yang baru, pastikan ukurannya sesuai dengan POP_SIZE
        population = sorted(unique_population, key=get_fitness, reverse=True)[:POP_SIZE]

        while len(population) < POP_SIZE:
            population.append(random.choice(population))  # Tambahkan individu acak jika populasi kurang dari POP_SIZE

        print(f"Generasi {gen + 1}:")
        print(f"  Parent 1: {p1} -> x1={decode(p1)[0]:.2f}, x2={decode(p1)[1]:.2f}, fitness={fitness(p1):.4f}")
        print(f"  Parent 2: {p2} -> x1={decode(p2)[0]:.2f}, x2={decode(p2)[1]:.2f}, fitness={fitness(p2):.4f}")
        print(f"  Child 1 : {c1} -> x1={decode(c1)[0]:.2f}, x2={decode(c1)[1]:.2f}, fitness={fitness(c1):.4f}")
        print(f"  Child 2 : {c2} -> x1={decode(c2)[0]:.2f}, x2={decode(c2)[1]:.2f}, fitness={fitness(c2):.4f}")
        print("")

        print(f"=== Populasi Generasi {gen + 1} ===")
        for i, chrom in enumerate(population):
            x1, x2 = decode(chrom)
            print(f"{i+1:2d}. {chrom} -> x1={x1:.2f}, x2={x2:.2f}, fitness={fitness(chrom):.4f}")
        print("===============================\n")

        # Memilih individu dengan fitness terbaik di setiap generasi
        current_best = max(population, key=get_fitness)  # Memilih berdasarkan fitness terbesar
        if fitness(current_best) > fitness(best_chrom):
            best_chrom = current_best

    x1, x2 = decode(best_chrom)
    print("\n=== Hasil Akhir ===")
    print("Kromosom terbaik:", best_chrom)
    print("x1 =", x1)
    print("x2 =", x2)
    print("Nilai fungsi =", objective(x1, x2))


# Jalankan program
algoritma_genetik()