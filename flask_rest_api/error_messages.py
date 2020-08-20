from typing import List, Dict, Union


def _gen_error_message_dict(loc: List[str], msg: str, _type: str) -> Dict[str, Union[str, List]]:
    """
    Формирование словаря с сообщение ошибки
    :param loc: Местоположение ошибки
    :param msg: Сообщение
    :param _type: Тип ошибки
    :return: Словарь с сообщением ошибки
    """
    return {
        'loc': loc,
        'msg': msg,
        'type': _type
    }


def gen_int_type_error(loc: List[str]) -> Dict[str, Union[str, List]]:
    """
    Формирование сообщения ошибки при невозможности преобразования значения в int
    :param loc: Местоположение ошибки
    :return: Словарь с сообщением ошибки
    """
    return _gen_error_message_dict(loc, 'value is not a valid integer', 'type_error.integer')


def gen_negative_int_error(loc: List[str]) -> Dict[str, Union[str, List]]:
    """
    Формирование сообщения ошибки при отрицательном значении параметра
    :param loc: Местоположение ошибки
    :return: Словарь с сообщением ошибки
    """
    return _gen_error_message_dict(loc, 'value cannot be negative', 'type_error.integer')


def gen_key_type_error(loc: List[str]) -> Dict[str, Union[str, List]]:
    """
    Формирование сообщения ошибки при передаче неправильного параметра
    :param loc: Местоположение ошибки
    :return: Словарь с сообщением ошибки
    """
    return _gen_error_message_dict(loc, 'value is not valid', 'key_error')
