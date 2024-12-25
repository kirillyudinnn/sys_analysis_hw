import csv
import sys
from typing import Optional

def fetch_cell_value(file_path: str, row_num: int, col_num: int) -> Optional[str]:
    """
    Извлекает значение из CSV-файла по указанным строке и столбцу.

    :param file_path: Путь к CSV-файлу.
    :param row_num: Индекс строки (начиная с 0).
    :param col_num: Индекс столбца (начиная с 0).
    :return: Значение ячейки или None, если файл не найден или индексы выходят за границы.
    """
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for current_row, row in enumerate(reader):
                if current_row == row_num:
                    return row[col_num] if col_num < len(row) else None
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except IndexError:
        print(f"Error: Row {row_num} or column {col_num} is out of range.")
    return None

def main():
    if len(sys.argv) != 4:
        print("Usage: python task.py <file_path> <row_number> <column_number>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        row_number = int(sys.argv[2])
        column_number = int(sys.argv[3])
    except ValueError:
        print("Error: Row and column numbers must be integers.")
        sys.exit(1)

    value = fetch_cell_value(file_path, row_number, column_number)
    if value is not None:
        print(value)
    else:
        print("No value found at the specified location.")

if __name__ == "__main__":
    main()
