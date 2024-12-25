import json
import numpy as np

def load_and_process_clusters(filepath: str):
    """
    Загружает данные кластеров из JSON-файла и преобразует их в список списков.

    :param filepath: Путь к JSON-файлу.
    :return: Список обработанных кластеров и общее количество элементов.
    """
    with open(filepath, 'r') as file:
        clusters_data = json.load(file)

    processed_clusters = [cluster if isinstance(cluster, list) else [cluster] for cluster in clusters_data]
    total_size = sum(len(cluster) for cluster in processed_clusters)

    return processed_clusters, total_size

def create_adjacency_matrix(clusters, total_size):
    """
    Создаёт матрицу смежности на основе приоритета кластеров.

    :param clusters: Список обработанных кластеров.
    :param total_size: Общее количество элементов.
    :return: Матрица смежности.
    """
    adjacency_matrix = np.ones((total_size, total_size), dtype=int)

    for idx, current_cluster in enumerate(clusters):
        preceding_elements = [el for cl in clusters[:idx] for el in cl]
        for elem in current_cluster:
            for prev_elem in preceding_elements:
                adjacency_matrix[elem - 1, prev_elem - 1] = 0

    return adjacency_matrix

def identify_conflicts(matrix):
    """
    Находит конфликтующие пары элементов в матрице смежности.

    :param matrix: Матрица смежности.
    :return: Список конфликтующих пар в строковом формате.
    """
    conflicts = []

    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if matrix[i, j] == 0 and matrix[j, i] == 0:
                conflict_pair = sorted([i + 1, j + 1])
                if conflict_pair not in conflicts:
                    conflicts.append(conflict_pair)

    return str([pair for pair in conflicts])

def process_files(file_path1, file_path2):
    """
    Обрабатывает два JSON-файла кластеров, создаёт матрицы и находит конфликты.

    :param file_path1: Путь к первому JSON-файлу.
    :param file_path2: Путь ко второму JSON-файлу.
    :return: Список конечных кластеров в строковом формате.
    """
    clusters1, size1 = load_and_process_clusters(file_path1)
    clusters2, size2 = load_and_process_clusters(file_path2)

    if size1 != size2:
        raise ValueError("Matrices must have the same size.")

    matrix1 = create_adjacency_matrix(clusters1, size1)
    matrix2 = create_adjacency_matrix(clusters2, size2)

    intersect_matrix = np.multiply(matrix1, matrix2)
    transpose_intersect = np.multiply(matrix1.T, matrix2.T)
    union_matrix = np.maximum(intersect_matrix, transpose_intersect)

    return identify_conflicts(union_matrix)

def main():
    """
    Главная функция для запуска обработки JSON-файлов.
    """
    import sys
    if len(sys.argv) != 3:
        print("Usage: python script.py <file1.json> <file2.json>")
        sys.exit(1)

    file_path1 = sys.argv[1]
    file_path2 = sys.argv[2]

    try:
        result = process_files(file_path1, file_path2)
        print(result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()