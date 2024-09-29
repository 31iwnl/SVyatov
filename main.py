import numpy as np
import matplotlib.pyplot as plt
import random  # Добавляем импорт для случайного выбора

# Данные о продуктах
products = [
    {'name': 'Куриная грудка', 'price': 150, 'calories': 165, 'proteins': 31, 'carbs': 0},
    {'name': 'Рис', 'price': 60, 'calories': 130, 'proteins': 2.7, 'carbs': 28},
    {'name': 'Брокколи', 'price': 40, 'calories': 55, 'proteins': 3.7, 'carbs': 11.2},
    {'name': 'Яблоко', 'price': 30, 'calories': 52, 'proteins': 0.3, 'carbs': 14},
    {'name': 'Творог', 'price': 100, 'calories': 100, 'proteins': 11, 'carbs': 3.4},
    {'name': 'Картофель', 'price': 20, 'calories': 77, 'proteins': 2, 'carbs': 17},
    {'name': 'Авокадо', 'price': 80, 'calories': 160, 'proteins': 2, 'carbs': 9},
    {'name': 'Киноа', 'price': 120, 'calories': 120, 'proteins': 4.1, 'carbs': 21},
    {'name': 'Лосось', 'price': 300, 'calories': 206, 'proteins': 22, 'carbs': 0},
    {'name': 'Орехи', 'price': 200, 'calories': 607, 'proteins': 20, 'carbs': 21},
]

# Параметры задачи
N = len(products)
k = 10
norms = {'calories': 2200, 'proteins': 70, 'carbs': 100}


# Генерация начальной популяции
def generate_population(size):
    return [np.random.choice(range(N), k, replace=False) for _ in range(size)]


# Оценка фитнеса
def fitness(individual):
    total_price = sum(products[i]['price'] for i in individual)
    total_nutrients = {
        'calories': sum(products[i]['calories'] for i in individual),
        'proteins': sum(products[i]['proteins'] for i in individual),
        'carbs': sum(products[i]['carbs'] for i in individual),
    }

    if (total_nutrients['calories'] < norms['calories'] or
            total_nutrients['proteins'] < norms['proteins'] or
            total_nutrients['carbs'] < norms['carbs']):
        return float('inf')  # Неприемлемый рацион

    return total_price


# Способы скрещивания
def one_point_crossover(parent1, parent2):
    point = np.random.randint(1, k - 1)
    return np.concatenate((parent1[:point], parent2[point:]))


def two_point_crossover(parent1, parent2):
    if k < 3:
        raise ValueError("k должно быть больше 2 для двухточечного скрещивания.")
    point1, point2 = sorted(np.random.choice(range(1, k - 1), 2, replace=False))
    return np.concatenate((parent1[:point1], parent2[point1:point2], parent1[point2:]))


def average_crossover(parent1, parent2):
    return np.array([np.random.choice([parent1[i], parent2[i]]) for i in range(k)])


# Способы мутации
def random_mutation(individual):
    idx = np.random.randint(0, k)
    individual[idx] = np.random.choice(range(N))
    return individual


def inversion_mutation(individual):
    idx1, idx2 = np.random.choice(range(k), 2, replace=False)
    individual[idx1:idx2 + 1] = individual[idx1:idx2 + 1][::-1]
    return individual


def probability_based_mutation(individual, prob=0.1):
    for i in range(k):
        if np.random.rand() < prob:
            individual[i] = np.random.choice(range(N))
    return individual


# Основной алгоритм
def genetic_algorithm(pop_size, generations, crossover_func, mutation_func):
    population = generate_population(pop_size)
    fitness_history = []

    for _ in range(generations):
        population = sorted(population, key=fitness)
        fitness_history.append(fitness(population[0]))

        next_gen = population[:pop_size // 2]

        while len(next_gen) < pop_size:
            # Используем random.sample для выбора родителей
            parents = random.sample(next_gen[:pop_size // 2], 2)
            parent1, parent2 = parents[0], parents[1]
            child = crossover_func(parent1, parent2)
            next_gen.append(mutation_func(child))

        population = next_gen

    return population[0], fitness(population[0]), fitness_history


# Проведение экспериментов
results = {}

crossover_methods = {
    "Одноточечное": one_point_crossover,
    "Двухточечное": two_point_crossover,
    "Среднее": average_crossover
}

mutation_methods = {
    "Случайная": random_mutation,
    "Инверсная": inversion_mutation,
    "На основе вероятности": probability_based_mutation
}

# Основной цикл экспериментов
for crossover_name, crossover_func in crossover_methods.items():
    for mutation_name, mutation_func in mutation_methods.items():
        best_individual, best_price, fitness_history = genetic_algorithm(100, 50, crossover_func, mutation_func)
        best_product_names = [products[i]['name'] for i in best_individual]
        results[(crossover_name, mutation_name)] = (best_price, best_product_names, fitness_history)

# Визуализация результатов
plt.figure(figsize=(12, 8))

for (crossover_name, mutation_name), (best_price, _, fitness_history) in results.items():
    plt.plot(fitness_history, label=f'{crossover_name} + {mutation_name}')

plt.xlabel('Поколение')
plt.ylabel('Цена')
plt.title('Изменение фитнеса в поколениях для различных методов скрещивания и мутации')
plt.legend()
plt.grid()
plt.show()

# Результаты
for (crossover_name, mutation_name), (best_price, best_product_names, _) in results.items():
    products_list = ', '.join(best_product_names)
    print(f"Лучшая цена для {crossover_name} + {mutation_name}: {best_price} (Продукты: {products_list})")
