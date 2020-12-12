from api.src.db import db
import api.src.models as models

class State:
    __table__ = 'states'
    columns = ['id', 'name']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}' 
        for k, v in kwargs.items():
            setattr(self, k, v)

    def cities(self, cursor):
        query_str = "SELECT cities.* FROM cities WHERE state_id = %s"
        cursor.execute(query_str, (self.id,))
        records = cursor.fetchall()
        return db.build_from_records(models.City, records)

