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
    # membagi panjang chromosom menjadi 2 untuk mendapat x1 dan x2
    half = len(chrom) // 2
    # memisahkan kromosom menjadi x1 dan x2
    x1_bin = chrom[:half]
    x2_bin = chrom[half:]
    # melakukan convert nilai binary ke desimal
    x1 = convert_to_binary(x1_bin, -10, 10)
    x2 = convert_to_binary(x2_bin, -10, 10)
    return x1, x2

def convert_to_binary(chrom, min_val, max_val):
    dec = 0
    # Mengubah biner ke desimal
    for i in range(len(chrom)):
        bit = int(chrom[i])
        power = len(chrom) - i - 1
        dec += bit * (2 ** power)
    # max_bin digunakan untuk membagi hasil konversi mentah dari biner ke desimal tetap dalam batas 
    max_bin = (2 ** len(chrom)) - 1 
    return min_val + (dec / max_bin) * (max_val - min_val)

def objective(x1, x2):
    # exception untuk menjaga jika terjadi error seperti membagi dengan nilai 0
    try:
        return -(math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + (3 / 4) * math.exp(1 - math.sqrt(x1 ** 2)))
    except:
        return float('inf')

def fitness(chrom):
    x1, x2 = decode(chrom)
    obj_value = objective(x1, x2)
    # Mengecek apakah fungsi objektif menghasilkan hasil yang valid
    if obj_value == float('inf') or obj_value == float('-inf'):
        return float('inf')  # Menandakan bahwa solusi ini tidak valid
    return 1 / (1 + obj_value)


def init_population():
    # method untuk inisialisasi populasi
    return [''.join(random.choice('01') for _ in range(CHROM_LENGTH)) for _ in range(POP_SIZE)]

def tournament_selection(pop, tournament_size=TOURNAMENT_SIZE):
    competitors = random.sample(pop, tournament_size)

    # Cari parent1 (fitness terbesar)
    parent1 = competitors[0]
    for comp in competitors[1:]:
        if fitness(comp) > fitness(parent1):  # fitness terbesar
            parent1 = comp

    # Cari parent2 yang berbeda dari parent1
    competitors.remove(parent1)
    parent2 = competitors[0]
    for comp in competitors[1:]:
        if fitness(comp) > fitness(parent2):  # fitness terbesar
            parent2 = comp

    return parent1, parent2
    
def crossover(p1, p2):
    # fungsi untuk crossover

    # Dengan menggunakan probabilitas crossover maka ada kesempatan (70% sesuai inisiasi) melakukan crossover
    if random.random() < PC:

        # Titik potong crossover ada 2 point sehingga dipilih disini
        point1 = random.randint(1, CHROM_LENGTH // 2)
        point2 = random.randint(CHROM_LENGTH // 2, CHROM_LENGTH - 1)

        # Melakukan crossover dengan menukar bagian yang menjadi titik point
        c1 = p1[:point1] + p2[point1:point2] + p1[point2:]
        c2 = p2[:point1] + p1[point1:point2] + p2[point2:]

        return c1, c2
    return p1, p2

def mutate(chrom, PM):
    # fungsi mutasi terjadinya random sesuai dengan Probabilitas mutasi
    mutated_chrom = []  # list untuk menyimpan kromosom yang telah dimutasi
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
    # function untuk sorting
    return sorted(pop, key=fitness)

def get_fitness(chrom):
    # fungsi untuk mendapat fitnes
    return fitness(chrom)

def algoritma_genetik():
    population = init_population()

    print("=== Populasi Awal ===")
    for i, chrom in enumerate(population):
        x1, x2 = decode(chrom)
        print(f"{i+1:2d}. {chrom} -> x1= {x1:.2f}, x2= {x2:.2f}, fitness= {fitness(chrom):.4f}, nilai fungsi= {objective(x1, x2):.4f}")
    print("======================\n")

    print("=== Populasi Awal (Urut berdasarkan fitness) ===")
    population = sorted(population, key=get_fitness, reverse=True)
    for i, chrom in enumerate(population):
        x1, x2 = decode(chrom)
        print(f"{i+1:2d}. {chrom} -> x1= {x1:.2f}, x2= {x2:.2f}, fitness= {fitness(chrom):.4f}")
    print("======================\n")

    # Memilih kromosom terbaik berdasarkan fitness terbesar
    best_chrom = max(population, key=get_fitness)  

    # looping generasi maximum yang dibuat
    for gen in range(GEN_MAX):
        child = []
        attempts = 0
        while len(child) < REPLACEMENT_SIZE and attempts < 10:
            p1, p2 = tournament_selection(population)  # Pastikan p1 dan p2 berbeda
            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1, PM)
            c2 = mutate(c2, PM)

            # Memilih jika fitness anak lebih baik daripada orang tua
            if fitness(c1) < fitness(p1):  # Jika fitness anak 1 lebih buruk, pertahankan parent
                child.append(p1)
            else:
                child.append(c1)

            if len(child) < REPLACEMENT_SIZE and fitness(c2) < fitness(p2):  # Jika fitness anak 2 lebih buruk
                child.append(p2)
            else:
                child.append(c2)
            attempts += 1

        # Gabungkan populasi lama dan child dan hapus dup
        combined_population = population + child
        unique_population = []
        for chrom in combined_population:
            if chrom not in unique_population:
                unique_population.append(chrom)

        # Pilih populasi yang baru, pastikan ukurannya sesuai dengan POP_SIZE
        population = sorted(unique_population, key=get_fitness, reverse=True)[:POP_SIZE]

        while len(population) < POP_SIZE:
            population.append(random.choice(population))  # Tambahkan individu acak jika populasi kurang dari POP_SIZE

        # print generasi parent dan child
        print(f"Generasi {gen + 1}:")
        print(f"  Parent 1: {p1} -> x1= {decode(p1)[0]:.2f}, x2= {decode(p1)[1]:.2f}, fitness= {fitness(p1):.4f}")
        print(f"  Parent 2: {p2} -> x1= {decode(p2)[0]:.2f}, x2= {decode(p2)[1]:.2f}, fitness= {fitness(p2):.4f}")
        print(f"  Child 1 : {c1} -> x1= {decode(c1)[0]:.2f}, x2= {decode(c1)[1]:.2f}, fitness= {fitness(c1):.4f}")
        print(f"  Child 2 : {c2} -> x1= {decode(c2)[0]:.2f}, x2= {decode(c2)[1]:.2f}, fitness= {fitness(c2):.4f}")
        print("")

        # mengecek populasi
        print(f"=== Populasi Generasi {gen + 1} ===")
        for i, chrom in enumerate(population):
            x1, x2 = decode(chrom)
            print(f"{i+1:2d}. {chrom} -> x1= {x1:.2f}, x2= {x2:.2f}, fitness= {fitness(chrom):.4f}, nilai fungsi= {objective(x1, x2):.4f}")
        print("===============================\n")

        # Memilih individu dengan fitness terbaik di setiap generasi
        current_best = max(population, key=get_fitness)  # Memilih berdasarkan fitness terbesar
        if fitness(current_best) > fitness(best_chrom):
            best_chrom = current_best

    # Hasil akhir dari total generasi terbentuk untuk best kromosom
    x1, x2 = decode(best_chrom)
    print("\n=== Hasil Akhir ===")
    print("Kromosom terbaik:", best_chrom)
    print("x1 =", x1)
    print("x2 =", x2)
    print("Nilai fungsi =", objective(x1, x2))  # Outputkan nilai fungsi untuk solusi terbaik

# Jalankan program
algoritma_genetik()