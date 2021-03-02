import api.src.db.db as db
import api.src.models as models
class Venue():
    __table__ = 'venues'
    columns = ['id', 'foursquare_id', 'name', 'price',
            'rating', 'likes', 'menu_url']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}' 
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def find_by_foursquare_id(self, foursquare_id, cursor):
        foursquare_query = """SELECT * FROM venues WHERE foursquare_id = %s"""
        cursor.execute(foursquare_query, (foursquare_id,))
        record =  cursor.fetchone()
        return db.build_from_record(models.Venue, record)

    def location(self, cursor):
        location_query = """SELECT * FROM locations WHERE locations.venue_id = %s"""
        cursor.execute(location_query, (self.id,))
        record = cursor.fetchone()
        return db.build_from_record(models.Location, record)

    def categories(self, cursor):
        categories_query = """SELECT categories.* FROM venue_categories 
        JOIN categories ON venue_categories.category_id = categories.id 
        WHERE venue_categories.venue_id = %s"""
        cursor.execute(categories_query, (self.id,))
        venue_records = cursor.fetchall()
        return db.build_from_records(models.Category, venue_records)

    def venue_categories(self, cursor):
        venue_categories_query = """SELECT venue_categories.* FROM venue_categories 
        WHERE venue_categories.venue_id = %s"""
        cursor.execute(venue_categories_query, (self.id,))
        venue_category_records = cursor.fetchall()
        return db.build_from_records(models.VenueCategory, venue_category_records)

    def to_json(self, cursor):
        venue_json = self.__dict__
        location = self.location(cursor)
        categories = self.categories(cursor)
        if location:
            location_dict = {'lon': location.longitude, 'lat': location.latitude, 'address': location.address}
            venue_json['location'] = location_dict
        return venue_json



    @classmethod
    def where_str(self, columns):
        column_mapping = {'city': 'cities.name', 'venue': 'venues.name', 
                'city': 'cities.name', 
                'category': 'categories.name', 
                'state': 'states.name', 'zipcode': 'zipcodes.code', 'rating': 'venues.rating', 'price': 'venues.price'}
        mapped_keys = [column_mapping[column] for column in columns]
        return ' = %s AND '.join(mapped_keys)

    @classmethod
    def join_str(self):
        return """FULL OUTER JOIN locations ON locations.venue_id = venues.id
        FULL OUTER JOIN zipcodes on locations.zipcode_id = zipcodes.id
        FULL OUTER JOIN cities on zipcodes.city_id = cities.id
        FULL OUTER JOIN states on states.id = cities.state_id
        FULL OUTER JOIN venue_categories on venue_categories.venue_id = venues.id
        FULL OUTER JOIN categories on venue_categories.category_id = categories.id"""

    @classmethod
    def where_clause(self, params):
        column_names = params.keys()
        where_str = self.where_str(column_names)
        join_str = self.join_str()
        query_str = f"""SELECT DISTINCT venues.* FROM venues 
        {join_str} WHERE {where_str} = %s """
        # vals = [f'%{val}%'for val in list(params.values())]
        return query_str, list(params.values())

    @classmethod
    def order_by_clause(self, order_by = "", direction = 'DESC'):
        sort_cols = ['price', 'rating', 'likes']
        directions = ['asc', 'desc', '']
        if not order_by: return ""
        elif order_by.lower() not in sort_cols:
            raise KeyError(f'{order_by} not in {sort_cols}')
        elif direction.lower() not in directions:
            raise KeyError(f'{direction} not in {directions}')
        else:
            return f"ORDER BY venues.{order_by} {direction}"

    @classmethod
    def search_clause(self, params):
        order_by = params.pop('order', '')
        direction = params.pop('direction', 'desc')
        where_clause, where_tuple = Venue.where_clause(params)
        order_by_clause = Venue.order_by_clause(order_by, direction)
        combined_clause = where_clause + order_by_clause
        return combined_clause, where_tuple

    @classmethod
    def search(self, params, cursor):
        if not params: return db.find_all(Venue, cursor)
        search_clause, search_tuple = self.search_clause(params)
        cursor.execute(search_clause, search_tuple)
        records = cursor.fetchall()
        return db.build_from_records(Venue, records)

