from src import *
class City:
    __table__ = 'cities'
    attributes  = ['id', 'name', 'state_id']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.attributes:
                raise f'{key} not in {self.attributes}' 
        for k, v in kwargs.items():
            setattr(self, k, v)

    def zipcodes(self, cursor):
        query_str = "SELECT zipcodes.* FROM zipcodes WHERE city_id = %s"
        cursor.execute(query_str, (self.id,))
        records = cursor.fetchall()
        return build_from_records(Zipcode, records)

    def state(self, cursor):
        query_str = "SELECT states.* FROM states WHERE id = %s"
        cursor.execute(query_str, (self.state_id,))
        record = cursor.fetchone()
        return build_from_record(State, record)

