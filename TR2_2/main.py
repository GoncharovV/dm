# Заносим в формате теха информацию о путях в графе
# Например, из вершины 1 в вершину 2 можно попасть по a или b
# Из 1 в 3 только по a
# А из 2 в 1 по пустому ребру

EMPTY_PATH = '\\Lambda'
EMPTY_SET = '\\emptyset'

data = {
    '1-2': '(a \\vee b)',
    '2-3': '(a \\vee b)',
    '1-3': 'a',
    '2-1': EMPTY_PATH,
    '1-4': EMPTY_PATH,
    '2-4': EMPTY_PATH,
}


def find_r_value(k: int, i: int, j: int) -> str:
    """
        Рекурсивно находит буквенное значение формулы R с заданными i, j, k на основе данных о графе
        Результат возвращает в формате теха
    """
    if k == 0:
        path = f'{i}-{j}'

        if path in data:
            return data[path]
        else:
            return EMPTY_SET

    if i == k:
        return '(' + find_r_value(k - 1, k, k) + ')^*' + find_r_value(k - 1, k, j)
    elif k == j:
        return find_r_value(k - 1, i, k) + '(' + find_r_value(k - 1, k, k) + ')^*'
    else:
        return find_r_value(k - 1, i, j) + ' \\vee ' + find_r_value(k - 1, i, k) + '(' + find_r_value(k - 1, k, k) + ')^*' + find_r_value(k - 1, k, j)


MAX_K = 2


class R:

    def __init__(self, k: int, i: int, j: int):
        self.i = i
        self.j = j
        self.k = k

    # Перегружаем приведение к строке, чтобы выводить текст сразу для теха
    def __str__(self) -> str:
        i, j, k = str(self.i), str(self.j), str(self.k)

        return 'R^' + k + '_{' + i + j + '}'

    def get_latex_formula(self) -> str:
        """Возвращает 'раскрытую' формулу R'"""
        i, j, k = self.i, self.j, self.k

        formula = ''

        # Разумеется можно было ограничиться только общим случаем
        # Но так как это программа именно для генерации текста в формате теха, то рассмотрим упрощенные случаи

        if i == k:
            formula = f'({R(k - 1, k, k)})^* {R(k - 1, k, j)}'
        elif k == j:
            formula = f'{R(k - 1, i, k)} ({R(k - 1, k, k)})^*'
        else:
            formula = f'{R(k - 1, i, j)} \\vee ' + f'{R(k - 1, i, k)} ({R(k - 1, k, k)})^* ' + f'{R(k - 1, k, j)}'

        # Если формулы не сокрашать, а писать в полном виде, то они быстро становятся слишком громоздкими
        # Самое простое - считать результат только для формул с маленьким k
        formula_value = ' = ' + find_r_value(k, i, j) if k <= MAX_K else ''

        return f'{self} = ' + formula + formula_value


TAB = "\\>"  # Формулы будут помещены внутрь \begin{tabbing} в техе, чтобы было нагляднее, так будем сдвигать строки с большей глубиной рекурсии


def print_formula(r_element: R, indent=0):
    """Рекурсивно выведем формулу, и все входящие в неё подформулы"""
    print(TAB * indent, '$', r_element.get_latex_formula(), '$ \\\\')

    if r_element.k == 1:
        return

    print('\\\\')

    i, j, k = r_element.i, r_element.j, r_element.k

    new_indent = indent + 1

    # Выводим все "подформулы", увеличивая отступ

    if i == k:
        print_formula(R(k - 1, k, k), new_indent)
        print_formula(R(k - 1, k, j), new_indent)
    elif k == j:
        print_formula(R(k - 1, i, k), new_indent)
        print_formula(R(k - 1, k, k), new_indent)
    else:
        print_formula(R(k - 1, i, j), new_indent)
        print_formula(R(k - 1, i, k), new_indent)
        print_formula(R(k - 1, k, k), new_indent)
        print_formula(R(k - 1, k, j), new_indent)

        print('\\\\')


print('\\begin{tabbing}')
print('M \= М \= М \= М \=M \=M \=M \=\kill')

print_formula(R(3, 1, 4))

print('\\end{tabbing}')
