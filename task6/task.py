import json

def calculate_membership(value, ranges):
    """
    Рассчитывает степень принадлежности для заданного значения по заданным точкам функции.
    """
    for start, end in zip(ranges, ranges[1:]):
        x0, y0 = start
        x1, y1 = end
        if x0 <= value <= x1:
            return y0 + (y1 - y0) * (value - x0) / (x1 - x0)
    return 0

def fuzzify(input_value, fuzzy_sets):
    """
    Преобразует входное значение в степени принадлежности для каждого терма.
    """
    memberships = {term: round(calculate_membership(input_value, points), 2) for term, points in fuzzy_sets.items()}
    print(f"Фаззификация значения {input_value}: {memberships}\n")
    return memberships

def map_rules_to_outputs(input_memberships, rules):
    """
    Применяет правила и возвращает выходные степени принадлежности.
    """
    output_memberships = {}
    for input_term, membership in input_memberships.items():
        output_term = rules.get(input_term)
        if output_term:
            output_memberships[output_term] = max(output_memberships.get(output_term, 0), membership)
    print(f"Результаты применения правил: {output_memberships}\n")
    return output_memberships

def combine_outputs(output_memberships, output_sets):
    """
    Объединяет выходные функции принадлежности с учетом их степени.
    """
    combined_points = []
    for term, membership in output_memberships.items():
        for x, y in output_sets[term]:
            combined_points.append((x, min(membership, y)))
    return combined_points

def defuzzify(aggregated_points):
    """
    Вычисляет центр тяжести для агрегированных точек.
    """
    weighted_sum = sum(x * y for x, y in aggregated_points)
    total_weight = sum(y for _, y in aggregated_points)
    return weighted_sum / total_weight if total_weight else 0

def run_fuzzy_logic(temp_data, reg_data, rules_data, input_temp):
    """
    Выполняет полный цикл обработки: фаззификация, применение правил, агрегация и дефаззификация.
    """
    temp_sets = json.loads(temp_data)
    reg_sets = json.loads(reg_data)
    rules = json.loads(rules_data)

    input_memberships = fuzzify(input_temp, temp_sets)
    output_memberships = map_rules_to_outputs(input_memberships, rules)
    aggregated_points = combine_outputs(output_memberships, reg_sets)
    result = defuzzify(aggregated_points)

    print(f"Результат дефаззификации: {result}\n")
    return result

# Пример данных
temperature_data = """{
    "cold": [[0, 1], [16, 1], [20, 0], [50, 0]],
    "comfortable": [[16, 0], [20, 1], [22, 1], [26, 0]],
    "hot": [[0, 0], [22, 0], [26, 1], [50, 1]]
}"""

regulator_data = """{
    "low": [[0, 1], [6, 1], [10, 0], [20, 0]],
    "medium": [[6, 0], [10, 1], [12, 1], [16, 0]],
    "high": [[0, 0], [12, 0], [16, 1], [20, 1]]
}"""

rule_data = """{
    "cold": "high",
    "comfortable": "medium",
    "hot": "low"
}"""

# Запуск алгоритма
run_fuzzy_logic(temperature_data, regulator_data, rule_data, 20)