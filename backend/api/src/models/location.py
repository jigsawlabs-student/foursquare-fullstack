from api.src.db import db
import api.src.models as models

class Location:
    __table__ = 'locations'
    columns = ['id', 'longitude', 'latitude', 'address', 
            'zipcode_id', 'venue_id', 'created_at']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}' 
        for k, v in kwargs.items():
            setattr(self, k, v)


    def venue(self, cursor):
        query_str = "SELECT * FROM venues WHERE id = %s"
        cursor.execute(query_str, (self.venue_id,))
        record = cursor.fetchone()
        return db.build_from_record(models.Venue, record)

    def zipcode(self, cursor):
        query_str = "SELECT * FROM zipcodes WHERE id = %s"
        cursor.execute(query_str, (self.zipcode_id,))
        record = cursor.fetchone()
        return db.build_from_record(models.Zipcode, record)
