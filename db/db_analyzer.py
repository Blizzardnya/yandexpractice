import sqlite3
from textwrap import dedent


if __name__ == '__main__':
    db = sqlite3.connect('db.sqlite')
    c = db.cursor()

    # С какими актёрами работал режиссер Jørgen Lerdam?
    movie_id = c.execute('SELECT id FROM movies WHERE director LIKE ?', ('%Jørgen Lerdam%', )).fetchone()

    actors_q = dedent("""
    SELECT a.name
    FROM movie_actors ma
         LEFT JOIN actors a ON ma.actor_id=a.id
    WHERE movie_id=?    
    """)

    actors = c.execute(actors_q, movie_id).fetchall()
    print(f'Movie id: {movie_id[0]}, actors: {actors}')

    # Кто из актёров снялся в большинстве фильмов?
    actor_q = dedent("""
    SELECT 	name, MAX(fcount)
    FROM (
        SELECT a.name, COUNT(a.name) as fcount
        FROM movie_actors ma
             LEFT JOIN actors a ON ma.actor_id=a.id
        WHERE a.name <> 'N/A'
        GROUP BY a.name)    
    """)

    actor = c.execute(actor_q).fetchone()
    print(f'Actor: {actor[0]}, film count: {actor[1]}')
