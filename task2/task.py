import csv
from collections import defaultdict

def process_hierarchy(input_csv: str) -> str:
    """
    Обрабатывает иерархию из CSV-строки, вычисляет зависимости и возвращает результаты в формате CSV.

    :param input_csv: Строка с CSV-данными (родитель, потомок).
    :return: Строка с результатами в формате CSV.
    """
    child_to_parents = defaultdict(set)
    parent_to_children = defaultdict(set)

    # Чтение CSV-данных
    for line in csv.reader(input_csv.strip().splitlines(), delimiter=','):
        if len(line) < 2:
            continue
        parent, child = line
        parent_to_children[parent].add(child)
        child_to_parents[child].add(parent)

    # Определение корневого узла и листьев
    root = next((node for node in parent_to_children if node not in child_to_parents), None)
    leaves = [node for node in child_to_parents if node not in parent_to_children]

    # Инициализация результатов
    nodes_data = {
        node: {
            'descendants': set(),
            'ancestors': set(),
            'd1': set(),
            'd2': set(),
            'd3': set(),
            'd4': set(),
            'd5': set()
        }
        for node in set(parent_to_children) | set(child_to_parents)
    }

    # Обход в прямом порядке
    if root:
        stack = [root]
        while stack:
            current = stack.pop()
            for child in parent_to_children[current]:
                nodes_data[child]['ancestors'].update(nodes_data[current]['ancestors'] | {current})
                nodes_data[child]['d4'].update(nodes_data[current]['ancestors'])
                nodes_data[child]['d5'].update(nodes_data[current]['descendants'] - {child})
                stack.append(child)

    # Обход в обратном порядке
    reverse_stack = leaves[:]
    while reverse_stack:
        current = reverse_stack.pop()
        for parent in child_to_parents[current]:
            nodes_data[parent]['descendants'].update(nodes_data[current]['descendants'] | {current})
            nodes_data[parent]['d3'].update(nodes_data[current]['descendants'])
            reverse_stack.append(parent)

    # Формирование результата
    fields = ['d1', 'd2', 'd3', 'd4', 'd5']
    result_lines = []
    for node in sorted(nodes_data):
        line = [str(len(nodes_data[node][field])) for field in fields]
        result_lines.append(','.join(line))

    return '\n'.join(result_lines) + '\n'

if __name__ == "__main__":
    sample_csv = """1,2
1,3
3,4
3,5"""
    print(process_hierarchy(sample_csv))