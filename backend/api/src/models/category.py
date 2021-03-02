from api.src.db import db
import api.src.models as models

class Category:
    __table__ = 'categories'
    columns = ['id', 'name']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}'
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def find_by_name(self, name, cursor):
        category_query = """SELECT * FROM categories WHERE name = %s """
        cursor.execute(category_query, (name,))
        category_record =  cursor.fetchone()
        category = db.build_from_record(self, category_record)
        return category

    @classmethod
    def find_or_create_by_name(self, name, conn, cursor):
        category = self.find_by_name(name, cursor)
        if not category:
            new_category = models.Category()
            new_category.name = name
            db.save(new_category, conn, cursor)
            category = self.find_by_name(name, cursor)
        return category

    def venues(self, cursor):
        venues_query = """SELECT venues.* FROM venues 
        JOIN venue_categories ON venue_categories.venue_id = venues.id 
        WHERE venue_categories.category_id = %s"""
        cursor.execute(venues_query, (self.id,))
        venue_records = cursor.fetchall()
        return db.build_from_records(models.Venue, venue_records)


