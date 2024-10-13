import numpy as np
import matplotlib.pyplot as plt

# Треугольная функция принадлежности
def triangular_mf(x, a, b, c):
    return np.maximum(0, np.minimum((x - a) / (b - a), (c - x) / (c - b)))

# Функция для отображения информации о нечетком множестве
def display_fuzzy_set_info(name, a, b, c, user_value):
    membership_degree = triangular_mf(user_value, a, b, c)
    print(f"Нечеткое множество: {name}")
    print(f"Параметры: a={a}, b={b}, c={c}")
    print(f"Степень принадлежности объекта {user_value}: {membership_degree:.2f}")

# Задаем параметры нечетких множеств для температуры
temperature_sets = {
    "Холодно": (5, 8, 10),
    "Прохладно": (10, 15, 20),
    "Тепло": (15, 20, 30),
    "Жарко": (25, 35, 40)
}

# Задаем параметры нечетких множеств для влажности
humidity_sets = {
    "Сухо": (5, 15, 40),
    "Умеренно влажно": (30, 40, 60),
    "Влажно": (50, 60, 80),
    "Очень влажно": (70, 90, 100)
}

# Запрашиваем значения для проверки
user_temp = float(input("\nВведите значение температуры для проверки степени принадлежности: "))
user_humidity = float(input("Введите значение влажности для проверки степени принадлежности: "))

# Отображаем информацию о каждом нечетком множестве для температуры
print("\nРезультаты для температуры:")
for name, (a, b, c) in temperature_sets.items():
    display_fuzzy_set_info(name, a, b, c, user_temp)

# Отображаем информацию о каждом нечетком множестве для влажности
print("\nРезультаты для влажности:")
for name, (a, b, c) in humidity_sets.items():
    display_fuzzy_set_info(name, a, b, c, user_humidity)

# Визуализация
x_temp = np.linspace(-5, 45, 500)
x_humidity = np.linspace(-5, 105, 500)

# Визуализация нечетких множеств для температуры
plt.figure(figsize=(12, 6))

# Температура
plt.subplot(1, 2, 1)
for name, (a, b, c) in temperature_sets.items():
    plt.plot(x_temp, triangular_mf(x_temp, a, b, c), label=name)
plt.title("Нечеткие множества для температуры")
plt.xlabel("Температура (°C)")
plt.ylabel("Степень принадлежности")
plt.axvline(user_temp, color='r', linestyle='--', label=f'Проверяемое значение: {user_temp}')
plt.legend()
plt.grid(True)

# Влажность
plt.subplot(1, 2, 2)
for name, (a, b, c) in humidity_sets.items():
    plt.plot(x_humidity, triangular_mf(x_humidity, a, b, c), label=name)
plt.title("Нечеткие множества для влажности")
plt.xlabel("Влажность (%)")
plt.ylabel("Степень принадлежности")
plt.axvline(user_humidity, color='r', linestyle='--', label=f'Проверяемое значение: {user_humidity}')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
