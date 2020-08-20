from typing import Tuple, Any, Optional, List, Dict

from elasticsearch import Elasticsearch, exceptions
from flask import Flask, jsonify, request

from flask_rest_api.error_messages import gen_int_type_error, gen_negative_int_error, gen_key_type_error

app = Flask('movies_service')
es = Elasticsearch()


def _validate_params(limit: Optional[int], page: Optional[int], sort: str, sort_order: str) -> List[Dict]:
    """
    Валидация параметров запроса
    :param limit: Количество фильмов
    :param page: Страница
    :param sort: Поле для сортировки
    :param sort_order: Направление сортировки
    :return: Списосок ошибок
    """
    error_messages = []

    if sort not in {'id', 'title', 'imdb_rating'}:
        error_messages.append(gen_key_type_error(["query", "sort"]))

    if sort_order not in {'asc', 'desc'}:
        error_messages.append(gen_key_type_error(["query", "sort_order"]))

    if page is not None and page - 1 < 0:
        error_messages.append(gen_negative_int_error(["query", "page"]))

    if limit and limit < 0:
        error_messages.append(gen_negative_int_error(["query", "limit"]))

    return error_messages


@app.route('/api/movies/<movie_id>', methods=['GET'])
def movie_details(movie_id: str) -> Tuple[Any, int]:
    """
    Получение данных об одном фильме
    :param movie_id: Идентификатор фильма
    :return: Информация о фильме
    """
    try:
        movie = es.get_source('movies', movie_id, _source_excludes=['actors_names', 'writers_names'])
    except exceptions.NotFoundError:
        return jsonify({'message': 'Фильм не найден'}), 404

    return jsonify(movie), 200


@app.route('/api/movies', methods=['GET'], strict_slashes=False)
def movies_list() -> Tuple[Any, int]:
    """
    Получения списка фильмов по фильтрам
    :return: Список фильмов
    """
    error_messages = []
    page = None
    limit = None

    try:
        limit = int(request.args.get('limit', 50))
    except ValueError:
        error_messages.append(gen_int_type_error(["query", "limit"]))

    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        error_messages.append(gen_int_type_error(["query", "page"]))

    sort = request.args.get('sort', 'id')
    sort_order = request.args.get('sort_order', 'asc')
    search = request.args.get('search')

    error_messages.extend(_validate_params(limit, page, sort, sort_order))

    if error_messages:
        return jsonify({"detail": error_messages}), 422

    body = {
        "query": {
            "multi_match": {
                "query": search,
                "fuzziness": "auto",
                "fields": [
                    "title^5",
                    "description^4",
                    "genre^3",
                    "actors_names^3",
                    "writers_names^2",
                    "director"
                ]
            }
        }
    }

    movies = es.search(body=body if search else {}, index='movies', size=limit, from_=limit * (page - 1),
                       sort=[f'{sort}:{sort_order}'], _source_includes=['id', 'title', 'imdb_rating'],
                       track_scores=True)
    result = [movie.get('_source') for movie in movies.get('hits').get('hits')]

    return jsonify(result)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
