from math import log, ceil
from typing import Optional


class Matrix:
    def __init__(self):
        self.matrix = []
        self.target_scale = 0
        self.target_len = 0

    def matrix_scale(self):
        if self.matrix:
            if len(self.matrix) > 2:
                self.target_scale = ceil(log(len(self.matrix), 2))
            elif len(self.matrix) in (1, 2):
                self.target_scale = 2
            else:
                self.target_scale = 1

            self.target_len = self.target_scale ** 2

    def add_item(self, element: Optional = None):
        """
        Добавляем новый элемент в матрицу.
        Если элемент не умещается в (size - 1) ** 2, то нужно расширить матрицу.
        """
        if element is None:
            raise ValueError

        self.matrix.append(element)
        self.matrix_scale()

        if ((self.target_scale - 1) ** 2 <= len(self.matrix)) and (len(self.matrix) != 1):
            self.target_scale += 1
            self.target_len = self.target_scale ** 2

    def pop(self):
        """
        Удалить последний значащий элемент из массива.
        Если значащих элементов меньше (size - 1) * (size - 2), нужно уменьшить матрицу.
        """
        if (len(self.matrix)) == 1 and (self.matrix[0] is None):
            raise IndexError()

        item = self.matrix.pop()

        if len(self.matrix) <= (self.target_scale - 1) * (self.target_scale - 2):
            self.target_scale -= 1
            self.target_len = self.target_scale ** 2

        return item

    def __repr__(self):
        """
        Метод должен выводить матрицу в виде:
        1 2 3\nNone None None\nNone None None
        То есть, между элементами строки должны быть пробелы, а строки отделены \n
        """
        if not self.matrix:
            return 'None'

        result = []
        new_matrix = self.matrix+[None for _ in range(self.target_len-len(self.matrix))]

        for index in range(len(new_matrix)):
            if (index + 1) % self.target_scale == 0:
                result.append(' '.join(str(item) for item in new_matrix[index+1-self.target_scale: index+1]))

        return '\n'.join(result)


if __name__ == '__main__':
    matrix = Matrix()

    for i in range(4):
        matrix.add_item(i+1)

    matrix.add_item(10)

    print(matrix)

    print(matrix.pop())

    print(matrix)
