import csv
from math import log2

def compute_entropy(csv_content: str) -> float:
    """
    Рассчитывает энтропию для числовых значений в CSV-данных.

    :param csv_content: Строка с содержимым CSV.
    :return: Рассчитанная энтропия, округленная до одного знака.
    """
    lines = csv_content.strip().split('\n')
    reader = csv.reader(lines)
    data = [list(map(str.strip, row)) for row in reader]

    total_cells = sum(len(row) for row in data)
    entropy = 0.0

    for row in data:
        for item in row:
            try:
                number = int(item)
            except ValueError:
                continue

            if number > 0:
                probability = number / total_cells
                entropy -= probability * log2(probability)

    return round(entropy, 1)

if __name__ == "__main__":
    csv_data = """2,0,2,0,0
0,1,0,0,1
2,1,0,0,1
0,1,0,1,1
0,1,0,1,1"""
    result = compute_entropy(csv_data)
    print(result)   