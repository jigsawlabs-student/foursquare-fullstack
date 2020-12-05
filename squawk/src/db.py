from flask import current_app
from flask import g
import psycopg2


def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(user = 'postgres', password = 'postgres',
            dbname = current_app.config['DATABASE'])
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def drop_records(cursor, conn, table_name):
    cursor.execute(f"DELETE FROM {table_name};")
    conn.commit()

