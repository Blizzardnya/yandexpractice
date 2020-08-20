import pytest

from matrix.main import Matrix


@pytest.mark.parametrize(
    'items,pop_count,expected',
    [
        pytest.param(
            [1, 1, 1, 1], 3, "1 None\nNone None",
            id='pop_several_resizes'
        ),
        pytest.param(
            [1, 1, 1, 1], 1, "1 1 1\nNone None None\nNone None None",
            id='pop_without_resize'
        ),
        pytest.param(
            [1, 2, 3], 1, "1 2\nNone None",
            id='pop_with_resize'
        ),
        pytest.param(
            [1, 1, 1, 1], 0, "1 1 1\n1 None None\nNone None None",
            id='add_item_without_resize'
        ),
        pytest.param(
            [1, 2, 3], 0, "1 2 3\nNone None None\nNone None None",
            id='add_item_extend_non_empty_matrix'
        ),
        pytest.param(
            [1], 0, "1 None\nNone None",
            id='add_item_empty_matrix'
        ),

    ],
)
def test_matrix(items, pop_count, expected):
    matrix = Matrix()
    for item in items:
        matrix.add_item(item)
    for _ in range(pop_count):
        matrix.pop()

    assert str(matrix) == expected


# тесты на проверку исключения, они не вписывается в шаблон,
# где можно передать однотипные параметры как в test_matrix
def test_pop_size_1():
    matrix = Matrix()

    with pytest.raises(IndexError):
        matrix.pop()


def test_add_item_none_value():
    matrix = Matrix()

    with pytest.raises(ValueError):
        matrix.add_item(None)
