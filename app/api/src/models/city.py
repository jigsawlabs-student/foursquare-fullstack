from api.src.db import db
import api.src.models as models

class City:
    __table__ = 'cities'
    columns  = ['id', 'name', 'state_id']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}' 
        for k, v in kwargs.items():
            setattr(self, k, v)


    def zipcodes(self, cursor):
        query_str = "SELECT zipcodes.* FROM zipcodes WHERE city_id = %s"
        cursor.execute(query_str, (self.id,))
        records = cursor.fetchall()
        return db.build_from_records(models.Zipcode, records)

    def state(self, cursor):
        query_str = "SELECT states.* FROM states WHERE id = %s"
        cursor.execute(query_str, (self.state_id,))
        record = cursor.fetchone()
        return db.build_from_record(models.State, record)

