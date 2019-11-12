"""
Labour work #2. Levenstein distance.
"""


def generate_edit_matrix(num_rows: int, num_columns: int) -> list:
    if type(num_rows) is not int or type(num_columns) is not int:
        return []
    return [[0] * num_columns for i in range(num_rows)]


def initialize_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int) -> list:
    matrix_modified = list(edit_matrix)
    if type(add_weight) is not int or type(remove_weight) is not int:
        return matrix_modified
    if len(matrix_modified) == 0:
        return []
    for i in range(len(matrix_modified)):  # заполнение первого столбца
        if len(matrix_modified[i]) == 0:  # проверка на пустой элемент
            continue
        matrix_modified[0][0] = 0
        matrix_modified[i][0] = matrix_modified[i-1][0] + remove_weight
    for j in range(len(matrix_modified[0])):  # заполнение первой строки
        matrix_modified[0][0] = 0
        matrix_modified[0][j] = matrix_modified[0][j-1] + add_weight
    return matrix_modified
"""
Labour work #2. Levenshtein distance.
"""

def minimum_value(numbers: tuple) -> int:
    pass


def fill_edit_matrix(edit_matrix: tuple,
                     add_weight: int,
                     remove_weight: int,
                     substitute_weight: int,
                     original_word: str,
                     target_word: str) -> list:

    minimum_value(edit_matrix)
    if type(original_word) is not str or type(target_word) is not str:
        return list(edit_matrix)
    if type(add_weight) is not int or type(remove_weight) is not int or type(substitute_weight) is not int:
        return list(edit_matrix)
    if not edit_matrix:
        return list(edit_matrix)
    for i in range(len(edit_matrix)):
        for j in range(len(edit_matrix[0])):
            if i == 0 or j == 0:
                continue
            option_one = edit_matrix[i-1][j] + remove_weight
            option_two = edit_matrix[i][j-1] + add_weight
            option_three = edit_matrix[i-1][j-1]
            if original_word[i-1] != target_word[j-1]:
                option_three += substitute_weight
            edit_matrix[i][j] = min(option_one, option_two, option_three)
    return list(edit_matrix)


def find_distance(original_word: str, target_word: str, add_weight: int, remove_weight: int,
                  substitute_weight: int) -> int:
    if type(original_word) is not str or type(target_word) is not str:
        return -1
    if type(add_weight) is not int or type(remove_weight) is not int or type(substitute_weight) is not int:
        return -1
    edit_matrix = tuple(generate_edit_matrix(len(original_word) + 1, len(target_word) + 1))
    edit_matrix = tuple(initialize_edit_matrix(edit_matrix, add_weight, remove_weight))
    edit_matrix = fill_edit_matrix(edit_matrix, add_weight, remove_weight, substitute_weight, original_word, target_word)
    return edit_matrix[len(original_word)][len(target_word)]


def save_to_csv(edit_matrix: tuple, path_to_file: str) -> None:
    file = open(path_to_file, 'w')
    for line in edit_matrix:
        row = [str(el) for el in line]
        row = ','.join(row)
        file.write(row + '\n')
    file.close()
    return None


def load_from_csv(path_to_file: str) -> list:
    matrix_to_fill = []
    file = open(path_to_file, 'r')
    matrix_lines = file.readlines()
    for line in matrix_lines:
        row = []
        for i in line.split(','):
            row.append(int(i))
        matrix_to_fill.append(row)
    file.close()
    return list(matrix_to_fill)

