import sqlite3

from core.repositories.sqls import CREATE_MAPPING_TABLE_SQL_QUERY
from core.settings.config import get_config


def create_tables():
    config = get_config()

    with sqlite3.connect(
        database=config.DATABASE_NAME,
    ) as connection:
        cursor = connection.cursor()

        cursor.execute(CREATE_MAPPING_TABLE_SQL_QUERY)
