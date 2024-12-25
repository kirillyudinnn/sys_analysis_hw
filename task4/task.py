from math import log2

def calculate_counts():
    """
    Вычисляет частоты сочетаний суммы и произведения (counts_ab),
    а также отдельно частоты сумм (counts_a) и произведений (counts_b)
    для всех пар бросков двух шестигранных кубиков.
    """
    counts_ab = {}
    counts_a = {}
    counts_b = {}

    for i in range(1, 7):
        for j in range(1, 7):
            sum_val = i + j
            prod_val = i * j

            # Обновляем counts_ab
            counts_ab[(sum_val, prod_val)] = counts_ab.get((sum_val, prod_val), 0) + 1

            # Обновляем counts_a
            counts_a[sum_val] = counts_a.get(sum_val, 0) + 1

            # Обновляем counts_b
            counts_b[prod_val] = counts_b.get(prod_val, 0) + 1

    return counts_ab, counts_a, counts_b

def calculate_probabilities(counts):
    """
    Преобразует частоты в вероятности.

    :param counts: Словарь частот.
    :return: Словарь вероятностей.
    """
    total_count = sum(counts.values())
    return {key: count / total_count for key, count in counts.items()}

def calculate_entropy(probabilities):
    """
    Вычисляет энтропию по словарю вероятностей.

    :param probabilities: Словарь вероятностей.
    :return: Энтропия.
    """
    return -sum(p * log2(p) for p in probabilities.values() if p > 0)

def round_values(values, precision=2):
    """
    Округляет значения в списке до заданной точности.

    :param values: Список чисел.
    :param precision: Точность округления.
    :return: Список округленных значений.
    """
    return [round(value, precision) for value in values]

def main():
    """
    Основная функция для вычисления энтропий и информации.
    """
    counts_ab, counts_a, counts_b = calculate_counts()

    # Вычисляем вероятности
    probability_ab = calculate_probabilities(counts_ab)
    probability_a = calculate_probabilities(counts_a)
    probability_b = calculate_probabilities(counts_b)

    # Вычисляем энтропии
    entropy_ab = calculate_entropy(probability_ab)
    entropy_a = calculate_entropy(probability_a)
    entropy_b = calculate_entropy(probability_b)

    # Условная энтропия и информация
    entropy_b_given_a = entropy_ab - entropy_a
    information_a_about_b = entropy_b - entropy_b_given_a

    # Возвращаем округленные результаты
    return round_values([entropy_ab, entropy_a, entropy_b, entropy_b_given_a, information_a_about_b])

if __name__ == "__main__":
    print(main())
