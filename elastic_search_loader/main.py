import json
import sqlite3
from textwrap import dedent
from typing import List, Optional

from elasticsearch import Elasticsearch

_conn = sqlite3.connect('../db.sqlite')
_cur = _conn.cursor()


def replace_not_available(value: str) -> Optional[str]:
    """
    Замена значения 'N/A' на None
    :param value: значение для замены
    :return: значение либо None
    """
    if value == 'N/A':
        return None

    return value


def _get_movies() -> List[tuple]:
    """
    Получение всех фильмов из БД
    :return: Все фильмы из БД
    """
    movies = _cur.execute('SELECT id, imdb_rating, genre, title, plot, director, writers FROM movies').fetchall()
    return movies


def _get_actors_by_movie(movie_id: str) -> List[tuple]:
    """
    Получение актёров по фильму
    :param movie_id: Идентификатор фильма
    :return: Список актёров
    """
    actors_q = dedent("""
        SELECT a.id, a.name
        FROM movie_actors ma
             LEFT JOIN actors a ON ma.actor_id=a.id
        WHERE a.name <> 'N/A' and ma.movie_id=?
    """)
    actors = _cur.execute(actors_q, (movie_id, )).fetchall()
    return actors


def _prepare_writers(writers: List[dict]) -> Optional[List[dict]]:
    """
    Подготовка писателей для записи в Elasticsearch
    :param writers: Список писателей
    :return: Отформатированный список писателей
    """
    if not writers:
        return None

    result = []

    for writer in writers:
        writer_name = _cur.execute('SELECT name FROM writers WHERE id=?', (writer.get('id'), )).fetchone()

        if writer_name:
            result.append({'id': writer.get('id'), 'name': writer_name[0]})

    return result


def _prepare_actors(actors: List[tuple]) -> List[dict]:
    """
    Подготовка актёров для записи в Elasticsearch
    :param actors: Список актёров
    :return: Отформатированный список актёров
    """
    result = []

    for actor in actors:
        result.append({'id': actor[0], 'name': actor[1]})

    return result


def prepare_movies() -> List[str]:
    """
    Подготовка фильмов для записи в Elasticsearch
    :return: Отформатированный список фильмов
    """
    result = []
    movies = _get_movies()

    for movie in movies:
        actors = _prepare_actors(_get_actors_by_movie(movie[0]))
        writers = _prepare_writers(json.loads(movie[6])) if movie[6] else None
        prepared_movie = {
            'id': movie[0],
            'imdb_rating': float(movie[1]) if movie[1] != 'N/A' else None,
            'genre': movie[2],
            'title': movie[3],
            'description': replace_not_available(movie[4]),
            'director': replace_not_available(movie[5]),
            'actors_names': ', '.join([actor.get('name') for actor in actors]),
            'writers_names': ', '.join([writer.get('name') for writer in writers]) if writers else None,
            'actors': actors,
            'writers': writers
        }
        result.append(json.dumps({'index': {'_index': 'movies', '_id': movie[0]}}))
        result.append(json.dumps(prepared_movie))

    return result


if __name__ == '__main__':
    es = Elasticsearch()

    movies = prepare_movies()
    es.bulk('\n'.join(movies) + '\n', index='movies')
